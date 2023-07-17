<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 15:45:15
 * @FilePath: /pois-2nd-project/giraffe/src/App.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <v-app>
    <AppBar></AppBar>

    <v-container class="mt-16">
      <router-view></router-view>
    </v-container>

    <BotUI
      :messages="data"
      @msg-send="messageSendHandler"
    ></BotUI>

    <Footer></Footer>
  </v-app>
</template>

<script>
export default {
  name: "App",

  components: {
    AppBar: () => import("@/components/layout/appbar.vue"),
    Footer: () => import("@/components/layout/footer.vue"),
    BotUI: () => import("@/components/BotUI.vue"),
  },
  data () {
    return {
      data: null
    }
  },
  methods: {
    messageSendHandler(value) {
      this.data = value;
    }
  }
};
</script>
