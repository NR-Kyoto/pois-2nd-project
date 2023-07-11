<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-20 17:51:10
 * @FilePath: /pois-2nd-project/giraffe/src/views/Authors.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div>
            <div class="my-8">
              <h2 class="text-h2 font-weight-bold">User name must be here</h2>
            </div>

            <div class="my-4">
              <h2 class="text-h4 font-weight-bold">Environment</h2>
            </div>

            <div class="py-4">
                  <v-alert
                    class="text-h3 font-weight-bold text-center"
                    border="left"
                    colored-border
                    color="accent"
                    style="line-height: 1.5;"
                  >
                    ? knives<br>
                    ? cutting boards<br>
                    ? stoves<br>
                  </v-alert>
              </div>

            <div class="my-4">
              <h2 class="text-h4 font-weight-bold">History</h2>
            </div>

            <!--v-divider class="my-4"></v-divider-->

            <v-row>
              <v-col cols="12" md="6" v-for="i in 8" :key="i">
                <v-hover
                  v-slot:default="{ hover }"
                  open-delay="50"
                  close-delay="50"
                >
                  <div>
                    <v-card
                      flat
                      :color="hover ? 'white' : 'transparent'"
                      :elevation="hover ? 12 : 0"
                      hover
                    >
                      <v-img
                        src="https://cdn.pixabay.com/photo/2021/01/30/20/04/sheltie-5965187_1280.jpg"
                        :aspect-ratio="16 / 9"
                        gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                        height="300px"
                        class="elevation-2"
                        style="border-radius: 16px"
                      >
                        <div class="text-h5 font-weight-bold white--text text-center">
                          Recipe image must be here
                        </div>
                      </v-img>

                      <v-card-text class="text-center">
                        <!--v-avatar color="secondary" size="86" class="authors">
                          <v-icon dark size="64">mdi-feather</v-icon>
                        </v-avatar-->

                        <div
                          class="text-h5 font-weight-bold primary--text pt-4"
                        >
                          Recipe title must be here
                        </div>

                        <div class="text-body-1 py-4">
                          Main ingredients/Cooking time
                        </div>

                        <div>
                          <v-btn icon>
                            <v-icon>mdi-facebook</v-icon>
                          </v-btn>

                          <v-btn icon>
                            <v-icon>mdi-twitter</v-icon>
                          </v-btn>

                          <v-btn icon>
                            <v-icon>mdi-youtube</v-icon>
                          </v-btn>

                          <v-btn icon>
                            <v-icon>mdi-instagram</v-icon>
                          </v-btn>
                        </div>
                      </v-card-text>
                    </v-card>
                  </div>
                </v-hover>
              </v-col>
            </v-row>
          </div>
        </div>
      </v-col>

      <v-col>
        <div>
          <siderbar />
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  name: "Category",
};
</script>

<style lang="scss" scoped>
.authors {
  position: relative;
  top: -50px;
  margin-bottom: -50px;
}
</style>
