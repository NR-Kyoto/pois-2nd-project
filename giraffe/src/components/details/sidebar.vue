<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-20 18:12:18
 * @FilePath: /pois-2nd-project/giraffe/src/components/details/sidebar.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <VueBotUI
  :options="botOptions"
  />
</template>

<script>
import { VueBotUI } from 'vue-bot-ui'

export default {
  name: 'sidebar',
  components: {
    VueBotUI,
  },
  data () {
    return {
      botOptions: {
        botTitle: 'Checklist',
        bubbleBtnSize: 112,
      }
    }
  }
}
</script>