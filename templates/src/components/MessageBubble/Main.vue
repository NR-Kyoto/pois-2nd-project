<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2021-11-04 14:10:22
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 15:36:34
 * @FilePath: /pois-2nd-project/giraffe/src/components/MessageBubble/Main.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template lang="pug">
.qkb-msg-bubble(:class="bubbleClass")
  //- .qkb-msg-avatar(v-if="message.agent === 'bot'")
  //-   .qkb-msg-avatar__img &nbsp;
  component(
    v-if="componentType",
    :is="componentType",
    :main-data="message"
  )
  .qkb-msg-bubble__time(v-if="message.createdAt")
    | {{ message.createdAt }}
</template>
<script>
import SingleText from './SingleText'
import ButtonOptions from './ButtonOptions'

export default {
  components: {
    SingleText,
    ButtonOptions
  },

  props: {
    message: {
      type: Object
    }
  },

  computed: {
    bubbleClass () {
      return this.message.agent === 'bot'
        ? 'qkb-msg-bubble--bot'
        : 'qkb-msg-bubble--user'
    },

    // Define the message type and return the specific component
    componentType () {
      let type = ''

      switch (this.message.type) {
        case 'button':
          type = 'ButtonOptions'
          break
        default:
          type = 'SingleText'
      }

      return type
    }
  }
}
</script>
