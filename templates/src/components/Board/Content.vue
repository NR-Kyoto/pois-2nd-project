<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2021-11-04 14:10:22
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-07-02 18:53:48
 * @FilePath: /pois-2nd-project/giraffe/src/components/Board/Content.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template lang="pug">
.qkb-board-content(ref="boardContent")
  .qkb-board-content__bubbles(
    ref="boardBubbles"
  ) <div>
    <v-row>
      <v-col v-for="item in mainData" :key="i" cols="12">
        <v-card>
          <v-img :aspect-ratio="16 / 9" src="https://i.epochtimes.com/assets/uploads/2022/06/id13756674-1101040220271528-600x400.jpg">
        </v-img>
        <v-card-text class="text-center">
          <p><v-icon>mdi-chef-hat</v-icon>&nbsp;{{ item.dish_name }}</p>
          <p><v-icon>mdi-food-apple</v-icon>&nbsp;{{ item.ingredient }}</p>
          <p><v-icon>mdi-timer-alert-outline</v-icon>&nbsp;{{ item.time }}</p>
          <p><v-icon>mdi-food-fork-drink</v-icon>&nbsp;{{ item.tool }}</p>
        </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>

    //- message-bubble(
    //-   v-for="(item, index) in mainData",
    //-   :key="index",
    //-   :message="item",
    //- )
</template>

<script>

export default {
  components: {
  },

  props: {
    mainData: {
      type: Array,
      required: true
    },
  },

  watch: {
    mainData: function (newVal) {
      this.$nextTick(() => {
        this.updateScroll()
      })
    }
  },

  methods: {
    updateScroll () {
      const contentElm = this.$refs.boardContent
      const offsetHeight = this.$refs.boardBubbles.offsetHeight

      contentElm.scrollTop = offsetHeight
    }
  }
}
</script>
