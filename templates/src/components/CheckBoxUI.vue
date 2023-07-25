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
                <v-img :aspect-ratio="16 / 9" :src="`http://localhost:8000/${item.dish_image}`">
                  <v-card-text>
                    <v-btn color="primary" v-on:click="deleteCheck(index)">delete</v-btn>
                  </v-card-text>
              </v-img>
              <v-card-text class="text-center">
                <v-icon>mdi-chef-hat</v-icon>&nbsp;{{ item.dish_name }}
                //- <p><v-icon>mdi-food-apple</v-icon>&nbsp;{{ item.manual.ingredient }}</p>
                <v-icon>mdi-timer-alert-outline</v-icon>&nbsp;{{ item.time }} 分
                //- <p><v-icon>mdi-food-fork-drink</v-icon>&nbsp;{{ item.tool }}</p>
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

    recipes: {
      type: Object
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
      },
      message: {}
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

    deleteCheck (index) {
      const i = index
      this.$emit('delete-recipe', i)
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

    async sendMessage () {

      if (this.mainData) {
        const token = sessionStorage.getItem("access");
        const config = {
        headers: { Authorization: `Bearer ${token}` },
        };
        const response = await axios.post("http://localhost:8000/recipe/mergeRecipe/", this.recipes, config)
        this.$emit('msg-send', response);
        this.recipes = null;
        this.mainData = null;
        this.botActive = false;
      }
    },

    updateScroll () {
      const contentElm = this.$refs.boardContent
      // const offsetHeight = this.$refs.boardBubbles.offsetHeight

      // contentElm.scrollTop = offsetHeight
    },
  }
}
</script>

<style src="../scss/_app.scss" lang="scss"></style>
