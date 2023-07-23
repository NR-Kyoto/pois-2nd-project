<template>
  <div>
    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div>

            <v-row>
              <v-col>
                  <div>
                      <v-card-text class="text-center mt-15">
                        <v-avatar color="secondary" size="86" class="authors">
                          <v-icon dark size="64">mdi-account</v-icon>
                        </v-avatar>

                        <div
                          class="text-h5 font-weight-bold primary--text pt-4"
                        >
                          {{ username }}
                        </div>

                        <div class="text-body-1 py-4">
                          Kyoto University Inforamtics Student M1
                        </div>

                        <div>
                          <v-btn
                              class="flex-grow-1"
                              height="40"
                              variant="tonal"
                              @click="logout"
                            >
                              logout
                            </v-btn>
                        </div>
                      </v-card-text>

                      <div class="d-flex algin-center">
                        <div><h2 class="text-h4 font-weight-bold">Tools</h2></div>
                        <div class="pl-2">
                          <v-btn color="primary">Edit</v-btn>

                        </div>
                      </div>
                      
                      <v-divider class="my-4"></v-divider>
                      <v-row cols="6" lg="6" xl="4">
                        <v-col v-for="i in 6" :key="i" cols="6" lg="4" md="6">
                          <v-card>
                            <v-card-text class="text-center"><h3>{{ user_tools_name[i-1] }} {{ user_tools_num[i-1] }}</h3></v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                      <v-divider class="my-4"></v-divider>

                      <h2 class="text-h4 font-weight-bold">履歴</h2>
                      <v-divider class="my-4"></v-divider>
                      
                      <v-row cols="12" lg="12" xl="8">
                        <v-col v-for="item in menu_history.slice(0, Math.min(menu_history.length, 6))" cols="12" lg="4" md="6">
                          <v-hover
                            v-slot:default="{ hover }"
                            open-delay="50"
                            close-delay="50"
                          >
                          <v-card
                          flat
                          :color="hover ? 'white' : 'transparent'"
                          :elevation="hover ? 12 : 0"
                          hover
                          >
                            <div>
                              <v-img
                                :aspect-ratio="16 / 9"
                                class="elevation-2"
                                gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                                height="200px"
                                :src="item.url"
                                style="border-radius: 16px"
                              >
                              <v-card-text>
                                <v-btn color="secondary" @click="sendMessage(item.ids)">Make</v-btn>
                              </v-card-text>
                            </v-img>
                              <v-card-text>
                                <div class="d-flex align-center">
                                  <div class="pl-2">
                                    <li v-for="name in item.dish_names">{{ name }}</li>
                                  </div>
                                </div>
                              </v-card-text>
                            </div>
                          </v-card>
                        </v-hover>
                        </v-col>
                      </v-row>
                  </div>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Category",
  data: () => ({
    username: sessionStorage.username,
    user_tools_name: ['包丁', 'まな板', 'フライパン', '鍋', 'ボール', 'コンロ'],
    user_tools_num: [],
    menu_history: [],
  }),
  async created () {
    try {
      const token = sessionStorage.getItem("access");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
      const response1 = await axios.get("http://localhost:8000/recipe/show_cookingtool_info", config)
      this.user_tools_num = Object.values(JSON.parse(response1.data))

      const response2 = await axios.get("http://localhost:8000/recipe/show_menu_history", config)
      this.menu_history = JSON.parse(response2.data)
      
      for (let i = 0; i < this.menu_history.length; i++) {
        let ids = []
        for (let j = 0; j < this.menu_history[i].dish_names.length; j++) {
          let response3 = await axios.post("http://localhost:8000/recipe/search_dish/", {search_str: this.menu_history[i].dish_names[j]}, config)
          
          let datas = JSON.parse(response3.data)
          if (j == 0) this.menu_history[i].url = datas[0].img_url
          ids.push(datas[0].id)
        }

        this.menu_history[i].ids = ids
      }
    }catch (error) {
      console.log(error)
    }
  },
  methods: {
    logout () {
      sessionStorage.clear();
      this.$router.push('/')
    },
    async sendMessage (id_list) {
      if (id_list.lenght != 0) {
        const token = sessionStorage.getItem("access");
        const config = {
          headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.post("http://localhost:8000/recipe/mergeRecipe/", {recipes: id_list}, config)
        this.$router.push('/detail')
      }
    },
  }
};
</script>

<style lang="scss" scoped>
.authors {
  position: relative;
  top: -50px;
  margin-bottom: -50px;
}
</style>
