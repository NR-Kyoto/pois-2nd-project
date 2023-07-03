<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2021-11-04 14:10:22
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-27 18:11:43
 * @FilePath: /pois-2nd-project/giraffe/src/components/Board/Action.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template lang="pug">
.qkb-board-action
  .qkb-board-action__extra
    slot(name="actions")
    button.qkb-action-item.qkb-action-item--send(@click="sendMessage")
      slot(name="sendButton")
      <span>Confirm</span>
</template>
<script>

export default {
  components: {

  },

  props: {

  },

  data () {
    return {
      messageText: null
    }
  },

  computed: {

    // TODO: sending

  },

  mounted () {
    this.$refs.qkbMessageInput.focus()
  },

  methods: {
    sendMessage () {
      if (this.messageText) {
        this.$emit('msg-send', { text: this.messageText })
        this.messageText = null
      }
    }
  }
}
</script>
