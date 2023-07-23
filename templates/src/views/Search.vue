<template>
  <div>
    <div class="pt-16"></div>
    <!-- 検索フォーム -->
    <v-text-field
      v-model="searchKeyword"
      label="何が食べたい？"
      outlined
      class="mb-4"
    >
    </v-text-field>

    <v-btn color="primary" @click="searchRecipes">検索</v-btn>

    <div class="pt-16"></div>
    <!-- 検索結果表示 -->
    <div v-if="recommendRecipes.length > 0">
      <h2>おすすめレシピ</h2>
      <v-card v-for="recipe in recommendRecipes" :key="recipe.id">
        <v-img
          :aspect-ratio="16 / 9"
          class="elevation-2"
          gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
          height="200px"
          :src="recipe.image"
          style="border-radius: 16px"
        >
        <v-card-text>
          <v-btn color="secondary" to="category">More</v-btn>
        </v-card-text>
        </v-img>

        <v-card-text>
          <div class="text-h5 font-weight-bold primary--text">
            {{ recipe.dish.name }}
          </div>

          <!-- 材料の表示 -->
          <div class="text-body-1 py-4">
            {{ recipe.ingredients }}
          </div>

          <div class="d-flex align-center">
            <div class="mr-auto pl-2">
              <v-icon>mdi-timer-alert-outline</v-icon>&nbsp;{{ recipe.time }} 分
            </div>
            <div class="p2">
              <v-btn color="secondary" size="small" @click="hold(recipe)"
              ><v-icon dark>mdi-plus</v-icon></v-btn
              >
            </div>
          </div>
        </v-card-text>
      </v-card>
    </div>
    <div v-else>
      <p>該当するレシピが見つかりません。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "Search",
  data() {
    return {
      searchKeyword: "", // 検索キーワードを保持するデータ
      recipes: [], // 全てのレシピデータ
      recommendRecipes: [], // おすすめレシピの結果を格納する配列
    };
  },
  methods: {
    async getRecommendations() {
      try {
        // ここでバックエンドのAPIエンドポイントにリクエストを送信 
        const response = await axios.get("/api/recommend_recipe/", {
          params: { keyword: this.searchKeyword },
        });

        // レスポンスからおすすめレシピの情報を取得してデータを更新
        this.recommendRecipes = response.data;
      } catch (error) {
        console.error(error);
      }
    },

    searchRecipes(){
      // 検索フォームの入力が変更されたら、推薦レシピを取得する関数を呼び出す
      this.getRecommendations();
    },
  },
};
</script>

