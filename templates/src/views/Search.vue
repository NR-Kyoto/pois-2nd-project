<template>
  <div>
    <CheckBoxUI :main-data="dish_name_set" :recipes="recipes" @delete-recipe="deleteCheck" @msg-send="messageSendHandler"/>
    <div class="pt-16"></div>
    <h1>おすすめのレシピ</h1>
    <div class="pt-16"></div>
    <v-row>
      <v-col v-for="item in recommendedRecipes" :key="item.dish_id" cols="12" lg="4" md="6">
        <v-hover
            v-slot:default="{ hover }"
            close-delay="50"
            open-delay="50"
        >
          <div>
            <v-card
                :color="hover ? 'white' : 'transparent'"
                :elevation="hover ? 12 : 0"
                flat
                hover
                to=""
            >
              <v-img
                  :aspect-ratio="16 / 9"
                  class="elevation-2"
                  gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                  height="200px"
                  :src="`http://localhost:8000/${item.dish_image}`"
                  style="border-radius: 16px"
              >
                <v-card-text>
                  <v-btn color="secondary" to="category">More</v-btn>
                </v-card-text>
              </v-img>

              <v-card-text>
                <div class="text-h5 font-weight-bold primary--text">
                {{ item.dish_name }}
                </div>

                <div class="text-body-1 py-4">
                  {{ item.ingredient }}
                </div>

                <div class="d-flex align-center">
                  <div class="mr-auto pl-2"><v-icon>mdi-timer-alert-outline</v-icon>&nbsp;{{ item.time }} 分</div>
                  <div class="p2"><v-btn color="secondary" size="small" @click="hold(item)"><v-icon dark>mdi-plus</v-icon></v-btn></div>
                </div>
              </v-card-text>
            </v-card>
          </div>
        </v-hover>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CheckBoxUI from '../components/CheckBoxUI.vue'
import axios from 'axios'

export default {
  name: "Search",
  components: {
    CheckBoxUI
  },

  data: () => ({
    dish_list: [],
    dish_name_set: [],
    recipes: {"recipes":[]},
    detail_dish_names: [],
    detail_procedure: {},
    detail_ingredient: {},
    detail_all_time: null,
    iconActive: null,
    username: null,
    recommendedRecipes: [] //新たにおすすめレシピを格納するデータ配列を用意
  }),

  async created() {
    this.iconActive = sessionStorage.access;
    this.username = sessionStorage.username;
    try {
      const token = sessionStorage.getItem("access");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
      const response = await axios.get("http://localhost:8000/recipe/getRecipe/", config);
      //console.log(response.data);
      this.dish_list = response.data.dish_list;
      //console.log(this.dish_list)

      // デバッグ用：レシピIDリストを表示
      //const recipeIds = this.dish_list.map((dish) => dish.dish_id);
      //const recipeIds = this.recipes["recipes"];
      //const recipeIds = [1,2]

      //ここでレシピIDリストを作成してAPIに送信する
      //const recipeIds = this.dish_list.map((dish) => dish.dish_id);
      //const recommendResponse = await axios.post("http://localhost:8000/recommend/recommend_recipe/", recipeIds, config);
      this.recommendedRecipes = this.dish_list;

      //const recommendResponse = await axios.post("http://localhost:8000/recommend/recommend_recipe/", recipeIds, config);
      //Vue.set(this, 'recommendedRecipes', recommendResponse.data.dish_list);

      // デバッグ用：おすすめレシピを表示
      //console.log("recommendedRecipes:", this.recommendedRecipes);

    } catch(error) {
      console.error(error)
    }
  },
  methods: {
    async messageSendHandler(value) {
      this.detail_dish_names = value.data.dish_names;
      this.detail_procedure = value.data.procedure;
      this.detail_ingredient = value.data.ingredient;
      this.detail_all_time = value.data.time; 
      sessionStorage.setItem('dish_names', this.detail_dish_names);
      sessionStorage.setItem('procedure', JSON.stringify(this.detail_procedure));
      sessionStorage.setItem('ingredient', JSON.stringify(this.detail_ingredient));
      sessionStorage.setItem('time', this.detail_all_time);
      this.dish_name_set = null;
      this.recipes = null;
      this.$router.push('/detail')
    },

    async hold(input){
      this.dish_name_set.push(input);
      this.recipes["recipes"].push(input.dish_id);
      try {
      // `this.recipes["recipes"]`をそのままレシピIDリストとしてAPIに送信する
      const config = {
        headers: { Authorization: `Bearer ${sessionStorage.getItem("access")}` },
      };
      const recommendResponse = await axios.post("http://localhost:8000/recommend/recommend_recipe/", this.recipes["recipes"], config);
      this.recommendedRecipes = recommendResponse.data.dish_list;

      // デバッグ用：おすすめレシピを表示
      console.log("recommendedRecipes:", this.recommendedRecipes);

    } catch (error) {
      console.error(error);
    }
      //Vue.set(this, 'recommendedRecipes', this.recommendedRecipes.concat(input.recipeIds));
    },

    deleteCheck(i) {
      this.dish_name_set.splice(i, 1);
      this.recipes["recipes"].splice(i, 1);
      //Vue.set(this, 'recommendedRecipes', this.recommendedRecipes.filter(recipe => !this.recipes["recipes"].includes(recipe.dish_id)));
    }
  },
};
</script>

