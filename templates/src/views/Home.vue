<template>
  <div>
    <CheckBoxUI :main-data="dish_name_set" :recipes="recipes" @delete-recipe="deleteCheck" @msg-send="messageSendHandler"/>
    <div>
      <v-card to="detail">
        <v-img
            :aspect-ratio="16 / 9"
            dark
            gradient="to top, rgba(25,32,72,.7), rgba(25,32,72,.0)"
            height="300px"
            src="https://www.ucsfhealth.org/-/media/project/ucsf/ucsf-health/education/hero/top-ten-foods-for-health-2x.jpg"
        >
          <v-card-text class="fill-height d-flex align-end">
            <v-row class="flex-column">
              <v-col cols="12" lg="10" md="10" xl="7">
                <h2 class="text-h3 py-3" style="line-height: 1.2">
                  食べたいものを作って食べて健康に
                </h2>
              </v-col>
              <v-col class="d-flex align-center">
                <!--v-avatar class="elevation-4" color="secondary">
                  <v-icon large>mdi-feather</v-icon>
                </v-avatar-->

                <div class="text-h6 pl-2">Create By Team 9</div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-img>
      </v-card>
    </div>

    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div class="pt-16">
            <h2 class="text-h4 font-weight-bold pb-4">レシピ一覧</h2>

            <v-row>
              <v-col v-for="item in dish_list" :key="item.dish_id" cols="12" lg="4" md="6">
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
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import CheckBoxUI from '../components/CheckBoxUI.vue'
import axios from 'axios'

export default {
  name: "Home",
  components: {
    CheckBoxUI,
  },

  data () {
    return {
      dish_list: [],
      dish_name_set: [],
      recipes: {"recipes":[]},
      detail_dish_names: [],
      detail_procedure: {},
      detail_ingredient: {},
      detail_all_time: null,
      iconActive: null,
      username: null,
    };
  },

  async created() {
    this.iconActive = sessionStorage.access;
    this.username = sessionStorage.username;
    try {
      const token = sessionStorage.getItem("access");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
      const response = await axios.get("http://localhost:8000/recipe/getRecipe/", config);
      this.dish_list = response.data.dish_list;
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

    hold(input){
      this.dish_name_set.push(input);
      this.recipes["recipes"].push(input.dish_id);
    },

    deleteCheck(i) {
      this.dish_name_set.splice(i, 1);
      this.recipes["recipes"].splice(i, 1);
    }
  },
};
</script>
