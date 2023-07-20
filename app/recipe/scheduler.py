import copy
import sys
import json
import re
import random

import networkx as nx
import matplotlib.pyplot as plt

# スケジュールの表示
import pandas as pd
import plotly.figure_factory as ff
from plotly import offline

# デバック用
import time
import psutil

from app.recipe.models import Dish, CookingTool

# リソースの種類と洗うのにかかる時間
WT = {
    'pan': 60,
    'knife': 30,
    'board': 100,
    'bowl': 100,
    'pot': 100
}

# 作成されたスケジュール案（デバック用）
counter = 0

# スケジュール用クラス
class Schedule:

    # self.resources        : ユーザの持っているリソース一覧
    # self.schedule         : 各リソースとユーザのスケジュール．リソースをキー，（開始時間，タスク）の配列を値とした辞書
    # self.resources_status : 各リソースの最後の状態．リソースをキー，状態を値とした辞書
    # self.finish_time      : スケジュールの終了時間
    # self.task_timing      : 各タスクの開始時間・終了時間．（時間，タスク，'start' | 'end'）のリスト
    # self.score            : スケジュールのスコア

    def __init__(self, user):
        
        # ユーザの持っているリソースを展開
        obj = CookingTool.objects.get(user=user)
        user_resource = {
            'pan': obj.flying_pan,
            'knife': obj.kitchen_knife,
            'board': obj.cutting_board,
            'bowl': obj.bowl,
            'stove': obj.stove,
            'pot': obj.sauce_pan
        }

        self.resources = []
        for k, v in user_resource.items():

            if v == 1:
                self.resources.append(k)

            elif v > 1:
                self.resources += [k + str(i) for i in range(v)]

        # 各リソースのscheduleの初期化
        tmp = [[] for i in range(len(self.resources) + 1)]
        self.schedule = dict(zip(['user'] + self.resources, tmp))

        # リソースの状態の初期化
        self.resources_status = dict(zip(
            self.resources,
            [None for i in range(len(self.resources))]
        ))

        # スケジュールの終了時間
        self.finish_time = 0
        
        # 各作業の開始と修了
        self.task_timing = []

        # スケジュールの優劣を決めるスコア
        self.score = -1.0

    # タスクを追加する
    def addTask(self, add_task, use_resources):

        # 使用リソース内で最も準備の遅い時間を開始時間にする
        start_time = max([0] + [self.taskFinishTime(x) for x in add_task.condition])
        for resource in use_resources:

            schedule = self.schedule.get(resource)

            if not schedule:
                continue

            st, task = schedule[-1]
            time = st + task.time
            if start_time < time:
                start_time = time

        # その開始時間で連続性を満たすのか確認
        if add_task.previous:
            previous_task_finish = self.taskFinishTime(add_task.previous)
            
            if previous_task_finish < start_time:
                return False

            else:
                start_time = previous_task_finish

        # taskで使うリソースすべてにタスクを挿入
        for resource in use_resources:
            
            self.schedule.get(resource).append((start_time, add_task))
            self.schedule.get(resource).sort(key = lambda x: x[0])

            # リソースの状態を更新
            if (resource != 'user') and ('stove' not in resource):
                self.resources_status[resource] = add_task.status

        # スケジュールの終了時間を更新
        task_finish_time = start_time + add_task.time 
        self.finish_time = task_finish_time if task_finish_time > self.finish_time else self.finish_time

        # タスクの終わりと始まりを記録
        self.task_timing.append((start_time, add_task, 'start'))
        self.task_timing.append((task_finish_time, add_task, 'end'))
        self.task_timing.sort(key = lambda x: x[0])
        
        return True

    # タスクの終了時間
    def taskFinishTime(self, task):
        return [x[0] for x in self.task_timing if (x[1].task_id == task.task_id) and (x[2] == 'end')][0]

    # 洗い物作業の追加
    def insertWash(self, start_time, wash_task):

        for resource in wash_task.resources:
            self.schedule.get(resource).append((start_time, wash_task))
            self.schedule.get(resource).sort(key = lambda x: x[0])

        # リソースの状態を更新
        self.resources_status[wash_task.resources[1]] = None

        # スケジュールの終了時間を更新
        task_finish_time = start_time + wash_task.time
        self.finish_time = task_finish_time if task_finish_time > self.finish_time else self.finish_time

        # タスクの終わりと始まりを記録
        self.task_timing.append((start_time, wash_task, 'start'))
        self.task_timing.append((task_finish_time, wash_task, 'end'))
        self.task_timing.sort(key = lambda x: x[0])
        
    # タスクを現在のスケジュールに追加するときに割り当てるリソースを決定
    def assignResource(self, task):

        assigned = []
        to_wash = []
        for resource in task.resources:

            if resource == 'user':
                assigned += ['user']
                continue
            
            # 直前調理とリソースがかぶっている場合は流用
            if task.previous and (resource in task.previous.resources):
                
                candidate = [x for x in self.resources if resource in x]

                tmp = None
                for x in candidate:
                    if len(self.schedule.get(x)) > 0 and self.schedule.get(x)[-1][1].task_id == task.previous.task_id:
                        tmp = x

                if tmp:
                    assigned.append(tmp)
                    continue
            
            # ユーザが所持しているリソースのうちタスクで使用するリソース
            tmp = [x for x in self.resources if resource in x]

            # 1つしか持ってないならそれを使う
            if len(tmp) == 1:
                assigned += tmp

                # 洗う必要があるかをチェック
                if Schedule.checkNecessityWash(self.resources_status.get(tmp[0]), task.status):
                    to_wash += tmp
                    
            # ２つ以上の候補があるリソース
            else:

                # 終了時間が速い順にソート？
                tmp.sort(key=lambda x: self.getResourceFinalTime(x))
                
                status = [self.resources_status.get(x) for x in tmp]

                # 優先順位１：まだ使ってない
                if None in status:
                    assigned.append(tmp[status.index(None)])
                    continue   

                # 優先順位２：洗い物不要
                checklist = [Schedule.checkNecessityWash(x, task.status) for x in status]
                if False in checklist:
                    assigned.append(tmp[checklist.index(False)])
                    continue

                # 優先順位３：洗い物必要
                # 使い終わるのが早い順に割り当てる
                t = [self.getResourceFinalTime(x) for x in tmp]
                x = tmp[t.index(min(t))]
                assigned.append(x)
                to_wash.append(x)

        return assigned, to_wash

    # 洗う必要があるかどうか        
    def checkNecessityWash(status, task_status):

        if not status:
            return False

        if status == 'meat' and task_status == 'vegetable':
            return True

        elif status == 'seasoning' and task_status != 'seasoning':
            return True

        return False

    # リソースが最後に使用される時間
    def getResourceFinalTime(self, resource):

        if self.schedule.get(resource):
            st, task = self.schedule.get(resource)[-1]
            return st + task.time

        else:
            return 0

    # リソースの空き時間
    def getFreeTime(self, resource):

        ft = []
        start = 0
        for st, task in self.schedule.get(resource):

            # 空き時間の開始から終了までをタプルで格納
            ft.append((start, st)) 

            start = st + task.time

        # 最後のタスク以降はずっと開き
        ft.append((start, sys.maxsize))

        # 間が0秒でないものを返す
        tmp = [(st, end) for st, end in ft if st < end]
        return tmp

    # task_timingをいい感じに並べ替える
    def sortTask(self):

        # 同じ時間のタスクでグルーピング
        grouped = {}
        t = -1
        for time, task, status in self.task_timing:
            if t != time:
                t = time
                grouped[t] = []

            grouped[t].append((time, task, status))

        self.task_timing.clear()

        # 並び替え
        for l in grouped.values():
            tmp = []
            count = -1
            
            for time, task, status in l:

                # 作業終了が最初
                if status == 'end':
                    tmp.insert(0, (time, task, status))
                    count += 1

                # 人手が必要ないタスク
                elif 'user' not in task.resources:
                    tmp.insert(count, (time, task, status))

                else:
                    tmp.append((time, task, status))

            self.task_timing += tmp

    # スケジュールをJSONに変換
    def getJson(self):

            result = []
            t = -1

            for time, task, status in self.task_timing:

                if status == 'end':
                    continue

                if t == time:
                    result.append({
                        "dish_index": task.dish_id,
                        "context": "その間に，" + task.context,
                        "tools": task.resources,
                        "time": task.time
                    })
                    
                else:
                    t = time
                    result.append({
                        "dish_index": task.dish_id,
                        "context": task.context,
                        "tools": task.resources,
                        "time": task.time
                    })

            return result


    # スケジュールを描写（デバック用）
    def plotSchedule(self):

        tasks = []
        task_types = set()
        for resource in ['user'] + self.resources:

            for start, task in self.schedule.get(resource):
                tasks.append({
                    'Task': resource,
                    'Start': start,
                    'Finish': start + task.time,
                    'Name': task.task_id
                })

                task_types.add(task.task_id)

        if not bool(tasks):
            print('There are no tasks.')
            return
        
        df = pd.DataFrame(tasks)

        colors = []
        r = lambda: random.randint(0,255)
        for i in range(len(task_types) + 1):              
            colors.append('#%02X%02X%02X' % (r(),r(),r()))

        fig = ff.create_gantt(
            df,
            colors=colors,
            index_col="Name",
            show_colorbar=True,
            group_tasks=True,
            title="Gantt Chart",
            showgrid_x=True,
            showgrid_y=True,
            height=400,
            width=1200
        )
        
        fig.data = sorted(fig.data, key=lambda x: x['name'])
        fig['layout'].update(legend=dict(traceorder='normal'))
        fig.update_layout(xaxis_type="linear", xaxis_tickmode="linear", xaxis_tick0=0, xaxis_dtick=300)  # 1時間ごとの目盛り

        offline.plot(fig)
        fig.show()

# 調理作業（タスク）用クラス
class Task:

    # self.dish_id      : スケジュール上での料理のインデックス
    # self.task_id      : タスクを一意に決める名前
    # self.status       : タスク終了時のリソースの状態
    # self.method       : 調理方法
    # self.resource     : 使用するリソース（機材）の配列
    # self.time         : 調理時間
    # self.condition    : 調理を始めるための条件．Taskのリスト
    # self.previous     : 直前に行うべき調理．Task
    # self.context      : 調理作業の文章

    method_to_resource = dict({
        'cut' : ['user', 'knife', 'board'],
        'stir' : ['pan', 'stove'],
        'stew' : ['pot', 'stove'],
        'mix' : ['user', 'bowl'],
    })

    source_jp = dict({
        'pan': 'フライパン',
        'pot': '鍋',
        'knife': '包丁',
        'board': 'まな板',
        'bowl': 'ボール',
    })

    def __init__(self, data=None, dish_index=0, table=None):

        self.dish_id = dish_index
        self.status = data.get('ingredient')
        self.method = data.get('method')
        self.time = int(data.get('time'))

        if self.method == 'wash':
            self.task_id = 'wash_' + data.get('resources')
            self.resources = ['user', data.get('resources')]
            self.condition = None
            self.previous = None
            self.context = "使った" + Task.source_jp.get(re.findall('[a-z]+', data.get('resources'))[0]) + "を洗う"

        else:
            self.task_id = data.get('id')
            self.previous = table.get(data.get('previous'))
            self.context = data.get('text')

            if self.method == 'other':
                self.resources = self.previous.resources.copy()

            elif self.method == 'leave':
                self.resources = self.previous.resources.copy()

                if 'user' in self.resources:
                    self.resources.remove('user')

                if 'knife' in self.resources:
                    self.resources.remove('knife')

            else:
                self.resources = Task.method_to_resource.get(self.method).copy()

            self.condition = [table.get(x) for x in data.get('condition')] if data.get('condition') else []

    def __str__(self):
        return self.task_id + "<"  + (self.status or "None") + ":" + str(self.time) + ":" + self.method + ":" + str(self.resources) + ">"

# スケジューリング用クラス
# ユーザ毎にインスタンス化することで複数アクセスを可能にする
class RecipeScheduler:

    # self.user
    # self.all_tasks        : すべてのタスクについてidをキー，インスタンスを値とする辞書
    # self.optimal_schedule : 最適なスケジュール．Schedule
    # self.wash_tasks       : 洗い物タスクのインスタンス．リソースをキー，インスタンスを値とする辞書
    # self.recipe_graph     : レシピを表す有向グラフ．
    # self.best_finish_time : 最速の終了時間

    # self.start_time       : 計算の開始時間（強制終了用）
    # self.limit_time       : 計算の最大時間

    # self.result_json      : フロントに渡すJSON

    def __init__(self, user, dishes, limit_time=60):

        # ユーザ
        self.user = user

        self.all_tasks = dict()
        dish_names = []
        ingredients = []
        for i, dish in enumerate(dishes):

            try:
                obj = Dish.objects.get(dish_id=dish)

            except Dish.DoesNotExist:
                raise ValueError("Invalid Dish")
            
            time = 0
            for task in obj.manual.get('procedure'):
                instaced = Task(data=task, dish_index=i+1, table=self.all_tasks)
                self.all_tasks[instaced.task_id] = instaced
                time += instaced.time

            dish_name = obj.dish_name
            dish_names.append(dish_name)
            ingredients.append(obj.manual.get('ingredient'))

            print("%s : %d sec" % (dish_name, time))

        # 最適なスケジュール
        self.optimal_schedule = Schedule(self.user)
        self.optimal_schedule.finish_time = sys.maxsize

        # 洗い物タスク
        wash_resources = [x for x in self.optimal_schedule.resources if 'stove' not in x]

        self.wash_tasks = dict()
        for resource in wash_resources:
            self.wash_tasks[resource] = Task(data={
                "method": "wash",
                "time": WT.get(re.findall('[a-z]+', resource)[0]),
                "resources": resource
            })

        # タスクグラフ
        self.recipe_graph = self.recipeToGraph()

        if not self.recipe_graph:
            print('Recipe is invalid')
            raise ValueError("cannot make graph")

        # 探索済みの中で最速の終了時間
        self.best_finish_time = sys.maxsize

        # 計算時間の制限
        self.start_time = 0
        self.limit_time = limit_time

        # 結果を格納する
        self.result_json = dict({
            "time": 0,
            "dish_names": dish_names,
            "procedure": [],
            "ingredient": ingredients
        })

    def recipeToGraph(self):

        graph = nx.DiGraph()

        # グラフ内で使用されるインデックスを設定
        graph.add_node(0)
        graph.add_node(1)
        for task in self.all_tasks.values():
            graph.add_node(task.task_id, task=task)

        for i, task in enumerate(self.all_tasks.values()):

            # 終わらせておく必要のある手順があるなら，そこからエッジを生成
            if task.condition:
                comb = [(cond_task, task) for cond_task in task.condition]
                edges = []

                # オーバーヘッドを計算
                for x, y in comb:
                    wash_resource = (set(x.resources) & set(y.resources))
                    wash_resource.discard('user')
                    wash_resource.discard('stove')

                    t = sum([WT.get(resource) for resource in wash_resource])
                    
                    edges.append((x.task_id, y.task_id, t))
                    
                graph.add_weighted_edges_from(edges)

            # なければスタートノードから直接エッジをつなぐ
            else:
                graph.add_edge(0, task.task_id, weight=0)

        # 終端ノードにつなぐ
        for node in graph.nodes():
            successor = list(graph.successors(node))

            # 出エッジが一つもないノードを終端ノードとつなぐ
            if not successor and node != 0 and node != 1:
                w = sum([WT.get(resource) for resource in nx.get_node_attributes(graph, 'task')[node].resources if WT.get(resource)])
                graph.add_edge(node, 1, weight=w)

        # 非巡回グラフ化の確認
        if not nx.is_directed_acyclic_graph(graph):
            return None

        plt.clf()
        nx.draw_circular(graph, with_labels = True)
        plt.show()
        plt.savefig("graph.png")

        return graph

    # レシピの組み立て
    def scheduling(self):
        
        E = [] # 実行可能な作業集合
        F = [] # 終了した作業集合

        unassigned_tasks = list(self.all_tasks.values()) # 未割当（実行可能ではない）のタスク

        # 最初に実行できる作業
        unassigned_tasks = RecipeScheduler.addExecutableTask(E, F, unassigned_tasks)

        schedule = Schedule(self.user)
        
        # 時間計測開始
        self.start_time = time.time()

        # 探索の開始
        self.recursive(E, F, schedule, unassigned_tasks)

        # 時間計測終了
        time_end = time.time()

        print(time_end - self.start_time)

        # いい感じに並べ替え
        self.optimal_schedule.sortTask()

        self.result_json["time"] = self.optimal_schedule.finish_time
        self.result_json["procedure"] = self.optimal_schedule.getJson()

        return self.result_json
    
    # taskが終了することにより実行可能になる作業を集合に追加する
    def addExecutableTask(E, F, unassigned_tasks):

        tmp = []
        for task in unassigned_tasks:

            # taskの終了条件すべてが終了した作業に含まれるか
            if set(task.condition).issubset(F):
                E.append(task) # 実行可能作業集合に追加
                
            else:
                tmp.append(task)

        return tmp

    # 探索木の作成
    # E : 実行可能な作業集合
    # F : 終了した作業集合
    # P : 探索のノードのスケジュール
    # unassigned_tasks : 未割当のタスク集合
    def recursive(self, E, F, P, unassigned_tasks):

        # 計算時間を制限
        if time.time() - self.start_time > self.limit_time:
            return

        # 枝刈りをすべきか
        if self.isBounded(P, E + unassigned_tasks):
            return

        # 実行可能な作業がある
        if E:

            # 前処理（並び替え）
            
            for i, task in enumerate(E):

                # taskをPに追加
                continuity, added_P = self.recstruct(P, task)
                
                # 連続性が満たされるなら
                if continuity:
                    new_E = E.copy()
                    new_F = F.copy()

                    new_F.append(new_E.pop(i)) # 終了した作業に追加

                    new_unassigned_tasks = RecipeScheduler.addExecutableTask(new_E, new_F, unassigned_tasks) # taskを終了することにより実行可能になる作業を追加
                    
                    self.recursive(new_E, new_F, added_P, new_unassigned_tasks)

                # ?
                else:
                    return

        else:

            self.addCleanUpTask(P) # 最後の洗い物を行う

            # より優れたスケジュールなら入れ替え
            if P.finish_time < self.best_finish_time + 180:
                
                # スコア算出
                self.setScheduleScore(P)

                if P.score > self.optimal_schedule.score:
                # if P.finish_time < self.optimal_schedule.finish_time:
                
                    global counter
                    counter += 1
                    print("counter : %d (%d sec)" % (counter, P.finish_time))
                    self.optimal_schedule = copy.deepcopy(P)
                    self.optimal_schedule.plotSchedule()

            if self.best_finish_time > P.finish_time:
                self.best_finish_time = P.finish_time

    # 枝刈りをするかどうか
    def isBounded(self, P, S):

        # まだ割り当てられてない頂点による部分グラフ
        graph = nx.subgraph(self.recipe_graph, [task.task_id for task in S])

        # クリティカルパスを取得
        critical_path = nx.dag_longest_path(graph, weight='weight')
        critical_edges = zip(critical_path, critical_path[1:])

        time = 0
        for x, y in critical_edges:
            time += nx.get_node_attributes(graph, 'task')[x].time
            time += nx.get_edge_attributes(graph, 'weight')[(x, y)]

        # 現在最良のスケジュールより遅いなら枝刈り
        if self.optimal_schedule.finish_time < P.finish_time + time:
            return True

        return False
    
    def setScheduleScore(self, schedule):

        # 洗い物のまとまり具合
        wash_task = [(time, task, status) for time, task, status in schedule.task_timing if ('wash' in task.task_id)]
        wash_task_num = len(wash_task) / 2

        count = 0
        for x, y in zip(wash_task, wash_task[1:]):
            if x[2] == 'end' and y[2] == 'start':
                if x[0] == y[0]:
                    count += 1

        wash_score = count / wash_task_num

        # 最終工程が最後の方にあるのか？
        last_nodes = list(self.recipe_graph.predecessors(1))
        leave_time = [schedule.finish_time - time for time, task, status in schedule.task_timing if (task.task_id in last_nodes) and (status == "end") and (task.method in ["stir", "stew"])]
        time_score = 1 / (1 + sum(leave_time))

        score = (wash_score + time_score * 300) / 301
        # score = (wash_score + time_score * 500) / 501

        schedule.score = score

    # 作業の並列化と制約チェック
    def recstruct(self, P, task):

        new_schedule = copy.deepcopy(P)

        # リソースの割り当て
        resources, need_wash_resources = new_schedule.assignResource(task)

        if need_wash_resources:

            # 洗う必要のあるリソースを時間でソート
            source_wt = [(resource, self.wash_tasks.get(resource).time) for resource in need_wash_resources]
            source_wt.sort(key = lambda x : x[1], reverse=True)

            # ユーザとリソースの空き時間から洗い物を挿入
            for resource, _ in source_wt:
                self.insertWashFreeTime(new_schedule, resource)

        # 連続性を確認しながら調理作業を実施
        continuity = new_schedule.addTask(task, resources)

        return continuity, new_schedule

    # スケジュールの最後に洗い物を行う
    def addCleanUpTask(self, P):

        for k, v in P.resources_status.items():

            if v:
                self.insertWashFreeTime(P, k)

    def insertWashFreeTime(self, schedule, resource):

        # ユーザの空き時間
        user_ft = schedule.getFreeTime('user')

        # リソースの最終使用時間
        final_time = schedule.getResourceFinalTime(resource)
        
        # 洗う時間
        wt = self.wash_tasks.get(resource).time

        # 空き時間のうち洗い物ができる時間
        valid_time = []
        span = []
        for st, end in user_ft:
            if st > final_time:
                if end - st > wt:
                    valid_time.append((st, end))
                    span.append(end - st)

            elif end > final_time:
                if end - final_time > wt:
                    valid_time.append((final_time, end))
                    span.append(end - final_time)

        # 利用可能な空き時間のうち最も短いところで洗う
        best_index = span.index(min(span))
        schedule.insertWash(valid_time[best_index][0], self.wash_tasks.get(resource))



# if __name__ == "__main__":
    
#     scheduler = RecipeScheduler(['Hamburger', 'ConsommeSoup'])
#     # scheduler = RecipeScheduler(['Hamburger'])
#     scheduler.scheduling()