<template>
  <div>
    <v-row>
      <v-col cols="12" lg="12" xl="8">
        <div>
          <div>
            <v-card flat color="transparent">
              <!--v-img
                src="https://cdn.pixabay.com/photo/2020/02/07/20/32/cyprus-4828328_1280.jpg"
                :aspect-ratio="16 / 9"
                gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                style="border-radius: 16px"
              ></v-img-->

              <v-card-text>
<<<<<<< HEAD
                <div class="py-4">
                  <v-alert
                    class="text-h6 text-center"
                    border="left"
                    colored-border
                    color="accent"
                  >
                    Recipe image must be put in this area.
                  </v-alert>
=======
                <div>
                  <v-btn color="secondary">ANIMAL</v-btn>
>>>>>>> b984eab12b950fddc65e1f228c2856401f3a57a0
                </div>

                <!--div>
                  <v-btn color="white">GENRE</v-btn>
                </div-->

                <div class="text-h4 font-weight-bold primary--text pt-4">
                  <h4>Recipe Name</h4>
                </div>

                <div class="text-body-1 py-4">
                  Main ingredients / Cooking time
                </div>

                <div class="d-flex align-center justify-space-between">
                  <div class="d-flex align-center">
                    <v-avatar color="accent" size="36">
                      <v-icon dark>mdi-feather</v-icon>
                    </v-avatar>

                    <div class="pl-2 text-body-1">Contributer name · Posted date</div>
                  </div>

                  <div class="d-flex align-center">
                    <div>
                      <v-chip small color="transparent">
                        <v-icon left>mdi-eye</v-icon>views
                      </v-chip>

                      <v-chip small color="transparent">
                        <v-icon left>mdi-comment-outline</v-icon>comments
                      </v-chip>
                    </div>
                  </div>
                </div>

                <v-divider class="my-4"></v-divider>

                <div class="text-h5 primary--text font-weight-bold">
                  Ingredients
                  <!--p class="text-subtitle-1 primary--text font-weight-medium">
                    List of ingredients must be put in this area. 
                  </p-->
                </div>

                <div class="py-4">
                  <v-alert
                    class="text-h6 text-center"
                    border="left"
                    colored-border
                    color="accent"
                  >
                    List of ingredients must be put in this area.
                  </v-alert>
                </div>

                <div class="text-h5 primary--text font-weight-bold">
                  How to make
                  <!--p class="text-subtitle-1 primary--text font-weight-medium mt-5">
                    List of procedure must be put in this area.
                  </p-->
                </div>

                <div class="py-4">
                  <v-alert
                    class="text-h6 text-center"
                    border="left"
                    colored-border
                    color="accent"
                  >
                    List of procedure must be put in this area.
                  </v-alert>
                </div>

                <!--div class="my-4">
                  <v-row>
                    <v-col cols="6">
                      <v-card>
                        <v-img
                          src="https://cdn.pixabay.com/photo/2015/03/26/09/47/sky-690293_1280.jpg"
                          :aspect-ratio="16 / 9"
                          gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                        ></v-img>
                      </v-card>
                    </v-col>

                    <v-col cols="6">
                      <v-card>
                        <v-img
                          src="https://cdn.pixabay.com/photo/2019/11/01/11/08/landscape-4593909_1280.jpg"
                          :aspect-ratio="16 / 9"
                          gradient="to top, rgba(25,32,72,.4), rgba(25,32,72,.0)"
                        ></v-img>
                      </v-card>
                    </v-col>
                  </v-row>
                </div-->

                <!--div class="text-h5 primary--text font-weight-bold">
                  Nibh tellus molestie nunc non blandit massa enim
                  <div class="text-subtitle-1 primary--text font-weight-medium mt-5">
                    <ul>
                      <li class="my-2">
                        Aliquam purus sit amet luctus venenatis lectus magna fringilla urna. Malesuada bibendum arcu vitae elementum curabitur vitae
                        nunc sed. Urna porttitor rhoncus dolor purus non enim praesent elementum facilisis.
                      </li>

                      <li class="my-2">
                        Proin libero nunc consequat interdum varius. Amet luctus venenatis lectus magna fringillal urna porttitor. Enim tortor at auctor
                        urna nunc id cursus.
                      </li>

                      <li class="my-2">
                        Volutpat maecenas volutpat blandit aliquam. Adipiscing enim eu turpis egestas pretium aenean pharetra magna Morbi leo
                        urna molestie at elementum eu.
                      </li>
                    </ul>

                    <p>
                      Venenatis a condimentum vitae sapien pellentesque habitant morbi tristique senectus. Semper auctor neque vitae tempus. Magnis dis
                      parturient montes nascetur ridiculus mus. A condimentum vitae sapien pellentesque habitant morbi tristique. Duis ut diam quam nulla
                      porttitor.
                    </p>
                  </div>
                </div-->

                <div class="d-flex align-center justify-space-between mt-8">
                  <div>
                    <v-row>
                      <v-col class="flex-shrink-0" cols="auto">
                        <v-chip color="accent">#Animalis</v-chip>
                      </v-col>

                      <v-col class="flex-shrink-0" cols="auto">
                        <v-chip color="accent">#Travel</v-chip>
                      </v-col>

                      <v-col class="flex-shrink-0" cols="auto">
                        <v-chip color="accent">#Birds</v-chip>
                      </v-col>
                    </v-row>
                  </div>

                  <div class="text-h5">
                    Share >
                    <v-btn icon large>
                      <v-icon large color="primary">mdi-facebook</v-icon>
                    </v-btn>

                    <v-btn icon large>
                      <v-icon large color="primary">mdi-twitter</v-icon>
                    </v-btn>

                    <v-btn icon large>
                      <v-icon large color="primary">mdi-linkedin</v-icon>
                    </v-btn>

                    <v-btn icon large>
                      <v-icon large color="primary">mdi-instagram</v-icon>
                    </v-btn>
                  </div>
                </div>

                <v-divider class="my-8"></v-divider>

                <!--div class="my-8">
                  <div class="d-flex align-center">
                    <v-avatar color="accent" size="128">
                      <v-icon dark size="100">mdi-feather</v-icon>
                    </v-avatar>

                    <div class="pl-4">
                      <div class="text-h5 primary--text font-weight-bold">
                        Written by
                        <span class="accent--text">Yan Lee</span>
                      </div>

                      <div class="text-subtitle-1 my-2">
                        Congue mauris rhoncus aenean vel elit. Elit scelerisque mauris pellentesque pulvinar pellentesque habitant. Aliquet nec
                        ullamcorper sit amet risus nullam eget felis.
                      </div>

                      <div class="text-subtitle-1">
                        Get in touch >
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
                    </div>
                  </div>
                </div-->

                <!--div>
                  <v-row justify="space-between">
                    <v-col cols="12" md="6" lg="4">
                      <div class="d-flex align-center">
                        <div>
                          <v-icon>mdi-arrow-left</v-icon>
                        </div>

                        <div class="text-h6 primary--text pl-2">
                          <div class="text-subtitle-1">Previous Post</div>Photos of Jeep models that will change
                          your mood
                        </div>
                      </div>
                    </v-col>

                    <v-col cols="12" md="6" lg="4">
                      <div class="d-flex align-center text-right">
                        <div class="text-h6 primary--text pr-2">
                          <div class="text-subtitle-1">Next Post</div>What do I need to know to start learning
                          JavaScript?
                        </div>

                        <div>
                          <v-icon>mdi-arrow-right</v-icon>
                        </div>
                      </div>
                    </v-col>
                  </v-row>
                </div-->
              </v-card-text>
            </v-card>
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
