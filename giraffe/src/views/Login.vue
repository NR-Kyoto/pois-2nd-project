<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-06-20 17:52:06
 * @FilePath: /pois-2nd-project/giraffe/src/views/Login.vue
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
<template>
  <v-row class="d-flex justify-center align-center fill-height" style="min-height: 100vh">
    <v-col cols="12" md="6">
      <v-card class="py-6">
        <v-card-title class="d-flex justify-center">
          <div class="text-h4">
            Login
          </div>
        </v-card-title>
        <v-card-text>
          <v-text-field
              label="UserName"
              outlined
          ></v-text-field>
          <v-text-field
              label="Password"
              outlined
          ></v-text-field>
          <div class="text-right">
            <v-btn color="primary">
              Login
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
