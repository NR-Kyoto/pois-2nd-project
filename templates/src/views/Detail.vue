<template>
  <div>
    <p class="text-h5 font-weight-bold primary--text pt-4">Time Cost:{{ time_min }} 分</p>
    <v-row cols="6" lg="6" xl="4">
      <v-col v-for="(name,i) in dish_names" key="i">
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
            <v-img
                :aspect-ratio="16 / 9"
                class="elevation-2"
                gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                height="200px"
                :src="img_url[i]"
                style="border-radius: 16px"
            >
            </v-img>
            <v-card-text>
                <div class="text-h6 pl-2">
                  <div class="pl-2">{{ name }}</div>
                </div>
              </v-card-text>
          </v-card>
        </v-hover>
      </v-col>
    </v-row>
  <v-timeline
        align-top
        dense
        v-for="item in procedure"
      >
        <v-timeline-item
          color="pink"
          small
        >
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>{{ item.time }} 秒</strong>
            </v-col>
            <v-col>
              <p><strong>{{ item.context }}</strong></p>
              <li v-if="item.dish_index">{{ dish_names[item.dish_index-1] }}</li>
              <v-col v-for="tool in item.tools">
                <v-icon>mdi-{{ tool }}</v-icon> &nbsp; {{ tool }}
              </v-col>
            </v-col>
          </v-row>
        </v-timeline-item>
      </v-timeline>
    </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Detail",

  data: () => ({
    dish_names: sessionStorage.getItem('dish_names').split(','),
    procedure: JSON.parse(sessionStorage.getItem('procedure')),
    ingredient: JSON.parse(sessionStorage.getItem('ingredient')),
    time: sessionStorage.getItem('time'),
    img_url: []
  }),

  computed: {
    time_min: function () {
      return Math.round(this.time/60)
    }
  },

  async created () {
    const token = sessionStorage.getItem("access");
    const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
    for (let i = 0; i < this.dish_names.length; i++) {
      const response3 = await axios.post("http://localhost:8000/recipe/search_dish/", {search_str: this.dish_names[i]}, config);
      let datas = JSON.parse(response3.data);
      this.img_url.push(datas[0].img_url)
      console.log(this.img_url)
    }
  }
};
</script>