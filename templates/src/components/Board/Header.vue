<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2021-11-04 14:10:22
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 14:08:40
 * @FilePath: /pois-2nd-project/giraffe/src/components/Board/Header.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template lang="pug">
.qkb-board-header
  slot(name="header")
    .qkb-board-header__title {{ listTitle }}
</template>
<script>
export default {
  props: {
    listTitle: {
      type: String,
      default: 'Checklist'
    }
  }
}
</script>
