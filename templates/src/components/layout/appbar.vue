<template>
  <div>
    <v-navigation-drawer
        v-if="!$vuetify.breakpoint.smAndUp"
        v-model="drawer"
        :clipped="$vuetify.breakpoint.lgAndUp"
        app
        color="primary"
        dark
    >
      <v-list color="primary" nav>
        <v-list-item
            v-for="(item, i) in btnItems"
            :key="i"
            :href="item.href"
            :target="item.target"
            :to="item.to"
            link
        >
          <v-list-item-content>
            <v-list-item-title>{{ item.text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item
            v-for="(item, i) in barItems"
            :key="i"
            :href="item.href"
            :target="item.target"
            :to="item.to"
            link
        >
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
        :clipped-left="$vuetify.breakpoint.lgAndUp"
        app
        color="#B01616"
        elevate-on-scroll
        flat
    >
      <v-container :class="{ 'px-0': !$vuetify.breakpoint.smAndUp }">
        <v-row
            :no-gutters="!$vuetify.breakpoint.smAndUp"
            align="center"
            justify="space-between"
        >
          <v-col class="d-flex align-center">
            <v-app-bar-nav-icon
                v-if="!$vuetify.breakpoint.mdAndUp"
                @click.stop="drawer = !drawer"
            />
            <v-toolbar-title
                class="font-weight-bold text-h5 primary--text"
                style="cursor: pointer"
                @click="$router.push('/')"
            >
              <v-icon color="primary" large>mdi-pot-steam-outline</v-icon>
              Cook
              <span class="accent--text">SKD</span>
            </v-toolbar-title>
          </v-col>

          <v-col v-if="$vuetify.breakpoint.mdAndUp" cols="6">
            <v-btn
                v-for="(item, i) in barItems"
                :key="i"
                :to="item.to"
                class="text-capitalize"
                exact
                exact-active-class="accent--text"
                text
            >{{ item.title }}
            </v-btn
            >
          </v-col>

          <v-col v-if="!iconActive" class="text-right">
            <v-btn
                v-for="(item, i) in btnItems"
                :key="i"
                :color="item.color"
                :href="item.href"
                :outlined="item.outlined"
                :target="item.target"
                :to="item.to"
                class="ml-3 text-capitalize"
            >
              <v-icon left>{{ item.icon }}</v-icon>
              {{ item.text }}
            </v-btn>
          </v-col>
          <v-col v-if="iconActive" class="text-right">
            <v-btn
                :to="`/authors`"
                class="ml-3 text-capitalize"
            >
              <v-icon left>mdi-account</v-icon>
              {{ username }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-app-bar>
  </div>
</template>

<script>
export default {
  data: () => ({
    drawer: null,
    username: null,
    iconActive: null,
    btnItems: [
      {
        text: "Login",
        to: "/login",
        target: "_black",
        color: "primary",
        icon: "mdi-login",
      },
    ],
    barItems: [
      {
        title: "Home",
        to: "/",
      },
      {
        title: "Search",
        to: "/search",
      },
      {
        title: "Detail",
        to: "/detail",
      }
    ],
  }),
  // computed: {
  //   iconActive() {
  //     return sessionStorage.access;
  //   },
  //   username() {
  //     return sessionStorage.username;
  //   }
  // },
  created() {
    this.username = sessionStorage.getItem('username');
    this.iconActive = sessionStorage.getItem('access');

    window.addEventListener('storage', this.handleStorageChange);
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.handleStorageChange);
  },
  methods: {
    handleStorageChange(event) {
      if (event.key === 'access') {
        this.$forceUpdate();
      }
    }
  }
};
</script>
