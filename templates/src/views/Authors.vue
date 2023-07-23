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
                          <v-btn color="primary" v-on:click="openModal">Edit</v-btn>
                          
                         <div id="overlay" v-show="showContent">
                          <div id="content">
                            <v-form ref="form">
                              <v-row cols="6" lg="6" xl="4">
                                <v-text-field
                                    v-model.number="kitchen_knife"
                                    :label="user_tools_name[0]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                                <v-text-field
                                    v-model.number="cutting_board"
                                    :label="user_tools_name[1]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                                <v-text-field
                                    v-model.number="flying_pan"
                                    :label="user_tools_name[2]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                                <v-text-field
                                    v-model.number="sauce_pan"
                                    :label="user_tools_name[3]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                                <v-text-field
                                    v-model.number="bowl"
                                    :label="user_tools_name[4]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                                <v-text-field
                                    v-model.number="stove"
                                    :label="user_tools_name[5]"
                                    type="number"
                                    outlined
                                ></v-text-field>
                              </v-row>
                            </v-form>
                            <v-btn color="primary" v-on:click="editTools">Edit</v-btn>&nbsp;
                            <v-btn v-on:click="closeModal">close</v-btn>
                          </div>
                         </div>
                         
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
    user_tools_name_en: [],
    user_tools_num: [],
    menu_history: [],
    showContent: false,

    kitchen_knife: 0,
    cutting_board: 0,
    flying_pan: 0, 
    sauce_pan: 0,
    bowl: 0,
    stove: 0
  }),
  async created () {
    try {
      const token = sessionStorage.getItem("access");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
      const response1 = await axios.get("http://localhost:8000/recipe/show_cookingtool_info", config)
      this.user_tools_num = Object.values(JSON.parse(response1.data))
      this.user_tools_name_en = Object.keys(JSON.parse(response1.data))

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

        this.kitchen_knife = this.user_tools_num[0]
        this.cutting_board = this.user_tools_num[1]
        this.flying_pan = this.user_tools_num[2]
        this.sauce_pan = this.user_tools_num[3]
        this.bowl = this.user_tools_num[4]
        this.stove = this.user_tools_num[5]
      }
    }catch (error) {
      console.log(error)
    }
  },
  methods: {
    
    openModal: function(){
      this.showContent = true
    },
    closeModal: function(){
      this.showContent = false
    },
    async editTools () {
      
      const token = sessionStorage.getItem("access");
      const config = {
        headers: { Authorization: `Bearer ${token}` },
        };

      const data = {
        kitchen_knife: this.kitchen_knife,
        cutting_board: this.cutting_board,
        flying_pan: this.flying_pan,
        sauce_pan: this.sauce_pan,
        bowl: this.bowl,
        stove: this.stove,
      };
      
      const response = await axios.post("http://localhost:8000/recipe/regist_cookingtool_info/", data, config);
      
      this.showContent = false

      this.$router.go({path: this.$router.currentRoute.path, force: true})
    },

    logout () {
      sessionStorage.clear();
      window.location.href = "/";
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

#overlay{
  /*　要素を重ねた時の順番　*/
  z-index:1;

  /*　画面全体を覆う設定　*/
  position:fixed;
  top:0;
  left:0;
  width:100%;
  height:100%;
  background-color:rgba(0,0,0,0.5);

  /*　画面の中央に要素を表示させる設定　*/
  display: flex;
  align-items: center;
  justify-content: center;
}
#content {
  z-index: 2;
  width: 50%;
  padding: 1em;
  background: #fff;
}
</style>
