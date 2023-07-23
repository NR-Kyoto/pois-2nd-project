<template>
  <div>
    <p class="text-h5 font-weight-bold primary--text pt-4">{{ dish_names }}</p>
    <p class="text-h5 font-weight-bold primary--text pt-4">Time Cost:{{ time_min }} 分</p>

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
              <strong>{{ item.context }}</strong>
              <v-col v-for="tool in item.tools">
                <v-icon>mdi-{{ tool }}</v-icon> &nbsp; {{ tool }}
              </v-col>
            </v-col>
          </v-row>
        </v-timeline-item>

        <!-- <v-timeline-item
          color="teal lighten-3"
          small
        >
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>3-4pm</strong>
            </v-col>
            <v-col>
              <strong>Design Stand Up</strong>
              <div class="text-caption mb-2">
                Hangouts
              </div>
              <v-avatar>
                <v-img
                  src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairFrida&accessoriesType=Kurt&hairColor=Red&facialHairType=BeardLight&facialHairColor=BrownDark&clotheType=GraphicShirt&clotheColor=Gray01&graphicType=Skull&eyeType=Wink&eyebrowType=RaisedExcitedNatural&mouthType=Disbelief&skinColor=Brown"
                ></v-img>
              </v-avatar>
              <v-avatar>
                <v-img
                  src="https://avataaars.io/?avatarStyle=Circle&topType=ShortHairFrizzle&accessoriesType=Prescription02&hairColor=Black&facialHairType=MoustacheMagnum&facialHairColor=BrownDark&clotheType=BlazerSweater&clotheColor=Black&eyeType=Default&eyebrowType=FlatNatural&mouthType=Default&skinColor=Tanned"
                ></v-img>
              </v-avatar>
              <v-avatar>
                <v-img
                  src="https://avataaars.io/?avatarStyle=Circle&topType=LongHairMiaWallace&accessoriesType=Sunglasses&hairColor=BlondeGolden&facialHairType=Blank&clotheType=BlazerSweater&eyeType=Surprised&eyebrowType=RaisedExcited&mouthType=Smile&skinColor=Pale"
                ></v-img>
              </v-avatar>
            </v-col>
          </v-row>
        </v-timeline-item>

        <v-timeline-item
          color="pink"
          small
        >
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>12pm</strong>
            </v-col>
            <v-col>
              <strong>Lunch break</strong>
            </v-col>
          </v-row>
        </v-timeline-item>

        <v-timeline-item
          color="teal lighten-3"
          small
        >
          <v-row class="pt-1">
            <v-col cols="3">
              <strong>9-11am</strong>
            </v-col>
            <v-col>
              <strong>Finish Home Screen</strong>
              <div class="text-caption">
                Web App
              </div>
            </v-col>
          </v-row>
        </v-timeline-item> -->
      </v-timeline>
    </div>
</template>

<script>
export default {
  name: "Detail",

  data: () => ({
    dish_names: sessionStorage.getItem('dish_names'),
    procedure: JSON.parse(sessionStorage.getItem('procedure')),
    ingredient: JSON.parse(sessionStorage.getItem('ingredient')),
    time: sessionStorage.getItem('time')
  }),

  computed: {
    time_min: function () {
      return Math.round(this.time/60)
    }
  },

  async created () {

  }
};
</script>