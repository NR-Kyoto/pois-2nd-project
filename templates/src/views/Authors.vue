<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-07-11 17:45:47
 * @FilePath: /pois-2nd-project/giraffe/src/views/Authors.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div>

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
              <v-col>
                  <div>
                      <v-img
                        src="https://www.knt.co.jp/travelguide/kokunai/image/travelguide_043_mv.jpg"
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
                        <v-avatar color="secondary" size="86" class="authors">
                          <v-icon dark size="64">mdi-account</v-icon>
                        </v-avatar>

                        <div
                          class="text-h5 font-weight-bold primary--text pt-4"
                        >
                          {{ username }}
                        </div>

                        <div class="text-body-1 py-4">
                          Kyoto University Inforamtics Student M1
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

                      <div class="d-flex algin-center">
                        <div><h2 class="text-h4 font-weight-bold">Tools</h2></div>
                        <div class="pl-2"><v-btn color="primary">Edit</v-btn></div>
                      </div>
                      
                      <v-divider class="my-4"></v-divider>
                      <v-row cols="6" lg="6" xl="4">
                        <v-col v-for="i in 6" :key="i" cols="6" lg="4" md="6">
                          <v-card>
                            <v-card-text class="text-center">fork</v-card-text>
                          </v-card>
                        </v-col>
                      </v-row>
                      <v-divider class="my-4"></v-divider>

                      <h2 class="text-h4 font-weight-bold">Order Record</h2>
                      <v-divider class="my-4"></v-divider>
                      
                      <v-row cols="12" lg="12" xl="8">
                        <v-col v-for="i in 6" :key="i" cols="12" lg="4" md="6">
                          <v-hover
                            v-slot:default="{ hover }"
                            open-delay="50"
                            close-delay="50"
                          >
                          <v-card
                          flat
                          :color="hover ? 'white' : 'transparent'"
                          :elevation="hover ? 12 : 0"
                          hover
                          >
                            <div>
                              <v-img
                                :aspect-ratio="16 / 9"
                                class="elevation-2"
                                gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                                height="200px"
                                src="https://i.epochtimes.com/assets/uploads/2022/06/id13756674-1101040220271528-600x400.jpg"
                                style="border-radius: 16px"
                              >
                              <v-card-text>
                                <v-btn color="secondary" to="category">Detial</v-btn>
                              </v-card-text>
                            </v-img>
                              <v-card-text>
                                <div class="d-flex align-center">
                                  <v-avatar color="secondary" size="36">
                                  <v-icon dark>mdi-feather</v-icon>
                                  </v-avatar>
                                  <div class="pl-2">Yan Lee · 22 July 2019</div>
                                </div>
                              </v-card-text>
                            </div>
                          </v-card>
                        </v-hover>
                        </v-col>
                      </v-row>
                  </div>
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
  data: () => ({
    username: localStorage.username
  })
};
</script>

<style lang="scss" scoped>
.authors {
  position: relative;
  top: -50px;
  margin-bottom: -50px;
}
</style>
