<template lang="pug">
.qkb-board-action
  .qkb-board-action__extra
    slot(name="actions")
    button.qkb-action-item.qkb-action-item--send(@click="sendMessage")
      slot(name="sendButton")
      <v-icon>mdi-leaf</v-icon>
</template>
<script>
import axios from "axios";

export default {
  components: {

  },

  props: {

  },

  data () {
    return {
      messageJson: {
        "recipes": []
      }
    }
  },

  computed: {

    // TODO: sending
    
  },

  mounted () {
  },

  methods: {
    sendMessage () {
      if (this.messageJson) {
        const token = localStorage.getItem("access");
        axios.post("http://localhost:8000/merge/", this.messageJson, {headers: {'Content-Type': 'application/json;charset=utf-8','token':token, "Access-Control-Allow-Origin": "*"}})
            .then(response => {
            
          });
        this.$emit('msg-send', { text: "Order has been sended!"});
        this.messageJson = null
      }
    }
  }
}
</script>
