import _ctypes
import copy
import sys
from bisect import insort
import gc

import networkx as nx

# リソースのサンプルデータ
resources = [
    {
        'user' : 'user1',
        'resource' : ['pan', 'pan2', 'knife', 'board', 'bowl']
    }
]

# リソースの種類と洗うのにかかる時間
WT = {
    'pan': 60,
    'knife': 30,
    'board': 100,
    'bowl': 100
}

# 調理作業のサンプルデータ
hamburger_recipe = []
soup_recipe = []

# 洗い物タスク　TODO ユーザごと
wash_tasks = []

# 最適なスケジュール　TODO　ユーザごと
optimal_schedule = Schedule('user1')

# タスクグラフ　TODO　ユーザごと
recipe_graph = nx.DiGraph()

# スケジュール用クラス
# 各リソースにtaskの開始時間とタスクidが順番に格納される
class Schedule:
    def __init__(self, user):
        
        self.resources = ['pan', 'pan2', 'knife', 'board', 'bowl'] # temp

        # scheduleの初期化
        tasks = [[] for i in range(len(self.resources) + 1)]
        self.schedule = dict(zip(['user'] + self.resources, tasks))

        # リソースの状態の初期化
        self.resources_status = dict(zip(self.resources, [None for i in range(len(key))]))

        # スケジュールの終了時間
        self.finish_time = 0
        
        # 各作業の開始と修了
        self.task_timing = []

    # タスクを追加する
    def addTask(self, task):

        # 使用リソース内で最も準備の遅い時間を開始時間にする
        start_time = 0
        for resource in task.resources:
            st, task_id = self.schedule.get(resource)[-1]
            time = st + _ctypes.PyObj_FromPtr(task_id).time
            if time > start_time:
                start_time = time

        # その開始時間で連続性を満たすのか確認
        if not task.previous:
            just_tasks = [_ctypes.PyObj_FromPtr(task_id) for time, task_id, status in self.task_timing if time == start_time and status = 'end']

            if task.previous not in just_tasks:
                return False

        # taskで使うリソースすべてにタスクを挿入
        for resource in task.resources:
            insort(self.schedule.get(resource), (start_time, task.id), key = lambda x: x[0])

            # リソースの状態を更新
            self.resources_status.get(resource) = task.status

        # スケジュールの終了時間を更新
        task_finish_time = start_time + task.time 
        self.finish_time = task_finish_time if task_finish_time > self.finish_time else self.finish_time

        # タスクの終わりと始まりを記録
        insort(self.task_timing, (start_time, task.id, 'start'), key = lambda x: x[0])
        insort(self.task_timing, (task_finish_time, task.id, 'end'), key = lambda x: x[0])

        return True

    # 洗い物作業の追加
    def insertWash(self, start_time, resource):
        wash_task = wash_tasks.get(resource)

        insort(self.schedule.get('user'), (start_time, wash_task), key = lambda x: x[0])
        insort(self.schedule.get(resource), (start_time, wash_task), key = lambda x: x[0])

        # リソースの状態を更新
        self.resources_status.get(resource) = None

        # スケジュールの終了時間を更新
        task_finish_time = start_time + WT.get(resource)
        self.finish_time = task_finish_time if task_finish_time > self.finish_time else self.finish_time

        # タスクの終わりと始まりを記録
        insort(self.task_timing, (start_time, task.id, 'start'), key = lambda x: x[0])
        insort(self.task_timing, (task_finish_time, task.id, 'end'), key = lambda x: x[0])

    # taskで必要なリソースの状態を返す
    def getResourceStatus(self, task=None):

        if task:
            return [(k, v) for k, v in resources_status if k in task.resources]

        return resources_status

    def checkOverlap(self):
        return

    # リソースの空き時間
    def getFreeTime(self, resource):

        ft = []
        start = 0
        for st, task_id in self.schedule.get(resource):

            task = _ctypes.PyObj_FromPtr(task_id) # taskオブジェクトを取得

            # 空き時間の開始から終了までをタプルで格納
            ft.append((start, st)) 

            start = st + task_id.time

        # 最後のタスク以降はずっと開き
        ft.append((start, sys.maxsize))

        # 間が0秒でないものを返す
        return [(st, end) for st, end in ft if st != end]

    # リソースが最後に使用される時間
    def getFinalTime(self, resource):
        st, task_id = self.schedule.get(resource)[-1]
        return st + _ctypes.PyObj_FromPtr(task_id).time

class Task:
    method_to_resource = dict{
        'cut' : ['user', 'knife', 'board'],
        'grill' : ['user', 'pan'],
        'boil' : ['pot']
    }

    ingredient_to_status = dict{
        'chicken': 'meat',
        'pork': 'meat',
        'beef': 'meat',
        'soy sauce': 'seasoning',
        'onion': 'vegetable'
    }

    def __init__(self, ingredient=None, amount=None, method='wash', resources=None, time=0, condition=None, previous=None):
        self.id = id(self)
        self.graph_index = 0
        self.ingredient = ingredient
        self.amount = amount
        self.method = method

        # リソースが未入力なら自動補完
        self.resources = Task.method_to_resource.get(method) if resources else ['user', resources]
        self.time = time
        self.status = Task.ingredient_to_status.get(ingredient)
        self.condition = condition
        self.previous = previous


# 探索木の作成
# E : 実行可能な作業集合
# F : 終了した作業集合
# P : 探索のノードのスケジュール
# unassigned_tasks : 未割当のタスク集合
def recursive(E, F, P, unassigned_tasks):

    # # 枝刈りをすべきか
    # if isBounded(P):
    #     return

    # 実行可能な作業がある
    if E:

        # 前処理（並び替え）
        
        for i, task in enumerate(E):

            # taskをPに追加
            continuity, added_P = Recstruct(P, task)

            # 連続性が満たされるなら
            if continuity:
                new_E = E.copy()
                new_F = F.copy()
                new_unassigned_tasks
                new_E.pop(i) # 実行可能な作業から削除
                new_F.append(task) # 終了した作業に追加
                AddExecutableTask(new_E, new_F, new_unassigned_tasks) # taskを終了することにより実行可能になる作業を追加
                recursive(new_E, new_F, added_P, new_unassigned_tasks)

    else:
        AddCleanUpTask(P) # 最後の洗い物を行う

        # より優れたスケジュールなら入れ替え
        if P.finish_time < optimal_schedule.finish_time: 
            optimal_schedule = P.copy()

# TODO　よくわからん
def isBounded(P, F):

    # まだ割り当てられてない頂点による部分グラフ
    graph = nx.subgraph(recipe_graph, [task.id for task in F])

    # クリティカルパスを取得
    critical_path = nx.dag_longest_path(graph, weight='weight')
    critical_edges = zip(critical_path, critical_path[1:])

    time = 0
    for x, y in critical_edges:
        time += recipe_graph[x]['time']
        time += recipe_graph[x][y]['weight']

    # 現在最良のスケジュールより遅いなら枝刈り
    if optimal_schedule.finish_time < P.finish_time + time:
        return True

    return False

# 作業の並列化と制約チェック
# P : 生成済みスケジュール
# task : 調理作業
def recstruct(P, task):

    new_schedule = P.copy() # TODO deepcopy?

    # Pの最終状態でのリソースの状態を取得
    resources = new_schedule.getResourceStatus(task)

    # 洗う必要のあるリソースを取得
    need_wash_resources = [k for k, v in resources if (not v) and (v != task.status)]

    if need_wash_resources:

        # 洗う必要のあるリソースを時間でソート
        source_wt = [(resource, WT.get(resource)) for resource in need_wash_resources]
        source_wt.sort(key = lambda x : x[1], reverse=True)

        # ユーザとリソースの空き時間から洗い物を挿入できるか？
        for resource, _ in source_wt:
            insertWashFreeTime(new_schedule, resource)

    # 連続性を確認しながら調理作業を実施
    continuity = new_schedule.addTask(task)

    return continuity, new_schedule

def insertWashFreeTime(schedule, resource):

    # ユーザの空き時間
    user_ft = schedule.getFreeTime('user')

    # リソースの最終使用時間
    final_time = schedule.getFinalTime(resource)
    
    # 洗う時間
    wt = WT.get(resource)

    # 空き時間のうち洗い物ができる時間
    valid_time = []
    span = []
    for st, end in user_ft:
        if st > final_time and end - st > wt:
            valid_time.append(st, end)
            span.append(end - st)

        elif end > final_time and end - final_time > wt:
            valid_time.append(final_time, end)
            span.append(end - final_time)

    # 利用可能な空き時間のうち最も短いところで洗う
    vest_index = index(min(span))
    schedule.insertWash(valid_time[vest_index][0], resource)


# taskが終了することにより実行可能になる作業を集合に追加する
# E : 実行可能な作業集合
# F : 終了した作業集合
def addExecutableTask(E, F, unassigned_tasks):

    for (i, task) in enumerate(unassigned_tasks):

        # taskの終了条件すべてが終了した作業に含まれるか
        if set(task.condition).issubset(F):
            E.append(tasks) # 実行可能作業集合に追加
            unassigned_tasks.pop(i) # 未割当の作業から削除

def addCleanUpTask(P):

    resources_status = getResourceStatus()

    for k, v in resources_status:

        if v:
            insertWashFreeTime(P, k)

def recipeToGraph(recipe):

    # グラフ内で使用されるインデックスを設定
    for task in recipe:
        recipe_graph.add_node(task.id, time=task.time)

    for i, task in enumerate(recipe):

        # 終わらせておく必要のある手順があるなら，そこからエッジを生成
        if task.condition:
            edges = [(cond_task.id, task.id, 0) for cond_task in task.condition]

            # オーバーヘッドを計算
            for x, y, z in edges:
                wash_resource = (set(x.resources) & set(y.resources))
                wash_resource.discard('user')
                z = sum([WT.get(resource) for resource in wash_resource])

            recipe_graph.add_weighted_edges_from(edges)

        # なければスタートノードから直接エッジをつなぐ
        else:
            recipe_graph.add_edge(0, task.graph_index, weight=0)

    # 終端ノードにつなぐ
    for node in recipe_graph.nodes():
        successor = recipe_graph.successors(node)

        # 出エッジが一つもないノードを終端ノードとつなぐ
        if not successor:
            recipe_graph.add_edge(node, 1, weight=sum([WT.get(resource) for resource in _ctypes.PyObj_FromPtr(node).resources]))

    # 非巡回グラフ化の確認
    return nx._ctypes.PyObj_FromPtr(recipe_graph)
    
if __name__ == "__main__":
    print(set([i for i in range(3)]).issubset([i for i in range(5)]))

    E = [] # 実行可能な作業集合
    F = [] # 終了した作業に追加
    unassigned_tasks = hamburger_recipe + soup_recipe

    # 最初に実行できる作業
    addExecutableTask(E, F, unassigned_tasks)

    # スケジュールと洗い物タスクをインスタンス化    
    schedule = Schedule('user1')
    wash_tasks = [Task(resources=[resource]) for resource in schedule.resources]

    # 探索の開始
    recursive(E, F, schedule, unassigned_tasks)
