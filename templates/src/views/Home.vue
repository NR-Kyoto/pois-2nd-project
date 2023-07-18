<template>
  <div>
    <div>
      <v-card to="detail">
        <v-img
            :aspect-ratio="16 / 9"
            dark
            gradient="to top, rgba(25,32,72,.7), rgba(25,32,72,.0)"
            height="500px"
            src="https://www.ucsfhealth.org/-/media/project/ucsf/ucsf-health/education/hero/top-ten-foods-for-health-2x.jpg"
        >
          <v-card-text class="fill-height d-flex align-end">
            <v-row class="flex-column">
              <!--v-col>
                <v-btn color="secondary" to="category">Travel</v-btn>
              </v-col-->
              <v-col cols="12" lg="8" md="10" xl="7">
                <h2 class="text-h3 font-weight-bold py-3" style="line-height: 1.2">
                  Image of most recommended recipe must be here
                </h2>
              </v-col>
              <v-col class="d-flex align-center">
                <!--v-avatar class="elevation-4" color="secondary">
                  <v-icon large>mdi-feather</v-icon>
                </v-avatar-->

                <div class="text-h6 pl-2">Contributer name · Posted date</div>
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
            <h2 class="text-h4 font-weight-bold pb-4">Recommended For You</h2>

            <v-row>
              <v-col v-for="(item, index) in recommended" :key="index" cols="12" lg="4" md="6">
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
                          src="https://cdn.pixabay.com/photo/2020/12/23/14/41/forest-5855196_1280.jpg"
                          style="border-radius: 16px"
                      >
                      <div class="text-h5 font-weight-bold white--text text-center">
                          Recipe image must be here
                      </div>
                        <!--v-card-text>
                          <v-btn color="secondary" to="category">TIPS</v-btn>
                        </v-card-text-->
                      </v-img>

                      <v-card-text>
                        <div class="text-h5 font-weight-bold primary--text">
                        {{ item.dish_name }}
                        </div>

                        <div class="text-body-1 py-4">
                          {{ item.ingredient }}
                        </div>

                        <div class="d-flex align-center">
                          <v-avatar color="secondary" size="36">
                            <v-icon dark>mdi-food-fork-drink</v-icon>
                          </v-avatar>
                          <div class="mr-auto pl-2">{{ item.tool }}</div>
                          <div class="p2"><v-btn color="secondary" size="small"><v-icon dark>mdi-plus</v-icon></v-btn></div>
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
    <CheckBoxUI :main-data="data" @msg-send="messageSendHandler"/>
  </div>
</template>

<script>
import CheckBoxUI from '../components/CheckBoxUI.vue'
export default {
  name: "Home",
  components: {
    CheckBoxUI,
  },

  data () {
    return {
      data: [
        {"dish_name": "鯖の塩焼き","ingredient": ["鯖","塩","大根"], "time": 2, "tool": "fork"},
        {"dish_name": "鯖の塩焼き"}
        ],
      recommended: [
        {"dish_name": "鯖の塩焼き","ingredient": ["鯖","塩","大根"], "time": 2, "tool": "fork"},
        {"dish_name": "鯖の塩焼き","ingredient": ["鯖","塩","大根"], "time": 2, "tool": "fork"}
      ],
      Message: null
    }
  },

  methods: {
    messageSendHandler(value) {
      this.Message=value
    }
  },
};
</script>
