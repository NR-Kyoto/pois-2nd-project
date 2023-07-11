<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-07-11 16:23:03
 * @FilePath: /pois-2nd-project/giraffe/src/views/Authors.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <div>
    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div>

            <v-row>
              <v-col>
                  <div>
                      <v-img
                        src="https://cdn.pixabay.com/photo/2021/01/30/20/04/sheltie-5965187_1280.jpg"
                        :aspect-ratio="16 / 9"
                        gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                        height="300px"
                        class="elevation-2"
                        style="border-radius: 16px"
                      ></v-img>

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
                      
                      <h2 class="text-h4 font-weight-bold pb-4">Order Record</h2>
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
                                src="https://cdn.pixabay.com/photo/2020/12/23/14/41/forest-5855196_1280.jpg"
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
