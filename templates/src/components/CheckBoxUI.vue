<template lang="pug">
.qkb-bot-ui(
  :class="uiClasses"
)
  transition(name="qkb-fadeUp")
    .qkb-board(v-if="botActive")
      .qkb-board-header
        slot(name="header")
          .qkb-board-header__title {{ listTitle }}
      .qkb-board-content(ref="boardContent")
        .qkb-board-content__bubbles(ref="boardBubbles") <div>
          <v-row>
            <v-col v-for="(item, index) in mainData" :key="index" cols="12">
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
      .qkb-board-action
        .qkb-board-action__extra
          button.qkb-action-item.qkb-action-item--send(@click="sendMessage")
            slot(name="sendButton")
            <v-icon>mdi-leaf</v-icon>
  .qkb-bot-bubble
    button.qkb-bubble-btn(
      @click="botToggle"
    )
      slot(name="bubbleButton")
        transition(name="qkb-scaleUp")
          <div v-if="!botActive" class="qkb-bubble-btn-icon">
          <v-icon color="success" size="36">mdi-cart</v-icon>
          </div>
          <div v-if="botActive" class="qkb-bubble-btn-icon">
          <v-icon color="success" size="36">mdi-cart-off</v-icon>
          </div>
  AppStyle(:options="optionsMain")
</template>
<script>
import EventBus from '../../helpers/event-bus'
import Config from '../../config'
import AppStyle from './AppStyle'
import axios from 'axios'

export default {
  name: 'BotkUI',

  components: {
    AppStyle
  },

  props: {

    mainData: {
      type: Array
    },

    isOpen: {
      type: Boolean,
      default: false
    },

    openDelay: {
      type: Number
    },

    listTitle: {
      type: String,
      default: 'Checklist'
    }
  },

  data () {
    return {
      botActive: false,
      defaultOptions: {
        listTitle: 'Checklist',
        colorScheme: '#1b53d0',
        textColor: '#ffffff',
        bubbleBtnSize: 80,
        animation: true,
        boardContentBg: '#fff',
        msgBubbleBgUser: '#4356e0',
        msgBubbleColorUser: '#fff',
        inputDisablePlaceholder: null
      }
    }
  },

  computed: {
    optionsMain () {
      return { ...this.defaultOptions, ...this.options }
    },

    // Add class to bot ui wrapper
    uiClasses () {
      let classes = []

      if (this.optionsMain.animation) {
        classes.push('qkb-bot-ui--animate')
      }

      return classes
    }
  },

  created () {
    if (this.isOpen) {
      if (this.openDelay) {
        setTimeout(this.botOpen, this.openDelay)
      } else {
        this.botToggle()
      }
    }
  },

  watch: {
    mainData: function (newVal) {
      this.$nextTick(() => {
        this.updateScroll()
      })
    }
  },

  mounted () {
    document.addEventListener(Config.EVENT_OPEN, function () {
      this.botOpen()
    })
    document.addEventListener(Config.EVENT_CLOSE, function () {
      this.botClose()
    })
    document.addEventListener(Config.EVENT_TOGGLE, function () {
      this.botToggle()
    })
  },

  beforeDestroy () {
    EventBus.$off('select-button-option')
  },

  methods: {
    botOpen () {
      if (!this.botActive) {
        this.botToggle()
      }
    },

    botClose () {
      if (this.botActive) {
        this.botToggle()
      }
    },

    botToggle () {
      this.botActive = !this.botActive

      if (this.botActive) {
        EventBus.$on('select-button-option', this.selectOption)
        this.$emit('init')
      } else {
        EventBus.$off('select-button-option')
        this.$emit('destroy')
      }
    },

    sendMessage (value) {
      if (this.mainData) {
        const token = localStorage.getItem("access");
        axios.post("http://localhost:8000/merge/", this.mainData, {headers: {'Content-Type': 'application/json;charset=utf-8','Authorization':token, "Access-Control-Allow-Origin": "*",'Access-Control-Allow-Headers': 'Content-Type, Authorization','Access-Control-Allow-Methods': '*',}})
            .then(response => {
            
          });
        this.$emit('msg-send', { text: "Order has been sended!"});
        this.mainData = null
      }
    },

    updateScroll () {
      const contentElm = this.$refs.boardContent
      const offsetHeight = this.$refs.boardBubbles.offsetHeight

      contentElm.scrollTop = offsetHeight
    },
  }
}
</script>

<style src="../scss/_app.scss" lang="scss"></style>