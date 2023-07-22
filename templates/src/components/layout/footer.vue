<template>
  <div>
    <v-card absolute app color="primary" dark flat>
      <v-container>
        <v-row align="start">
          <v-col cols="12" md="3">
            <h4 class="text-h5 font-weight-bold">
              Team 9
            </h4>
            <p class="text-body-1">
              CookSKD
            </p>
            <p class="text-body-1">
              食べたいものを作って食べて健康に
            </p>
          </v-col>

          <v-col cols="12" md="3">
            <v-list color="transparent" flat>
              <v-subheader class="text-h6">HeroUI</v-subheader>
              <v-list-item-group color="primary">
                <v-list-item
                    v-for="(item, i) in Pois"
                    :key="i"
                    :href="item.href"
                    dense
                    target="_black"
                >
                  <v-list-item-content>
                    <v-list-item-title
                        class="text-body-1"
                        v-text="item.text"
                    ></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>

          <v-col cols="12" md="3">
            <v-list color="transparent" flat>
              <v-subheader class="text-h6">Pois</v-subheader>
              <v-list-item-group color="primary">
                <v-list-item
                    v-for="(item, i) in shock"
                    :key="i"
                    :href="item.href"
                    dense
                    target="_black"
                >
                  <v-list-item-content>
                    <v-list-item-title
                        class="text-body-1"
                        v-text="item.text"
                    ></v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
        </v-row>

        <div class="text-center mt-6">
          Copyright &copy;
          <a
              class="white--text"
              href="https://www.soc.i.kyoto-u.ac.jp/"
              rel="noopener noreferrer"
              target="_blank"
          >Kyoto University Social informatics</a
          >
          {{ new Date().getFullYear() }}. All rights reserved.
        </div>
      </v-container>
    </v-card>
  </div>
</template>

<script>
export default {
  data: () => ({
    Pois: [
      {
        text: "Github Doc.",
        href: "https://github.com/NR-Kyoto/pois-2nd-project",
      },
      {
        text: "Themes",
        href: "https://heroui.net/",
      },
    ],
    shock: [
      {
        text: "Download",
        href: "https://github.com/NR-Kyoto/pois-2nd-project",
      },
      {
        text: "Issues",
        href: "https://github.com/NR-Kyoto/pois-2nd-project/issues",
      },
      {
        text: "LICENSE",
        href: "https://github.com/NR-Kyoto/pois-2nd-project/",
      },
    ],
  }),
};
</script>
