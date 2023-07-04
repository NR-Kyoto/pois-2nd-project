<!--
 * @Author: dnimo kuochingcha@gmail.com
 * @Date: 2022-02-11 19:34:46
 * @LastEditors: dnimo kuochingcha@gmail.com
 * @LastEditTime: 2023-07-04 18:09:14
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
          <v-form ref="form">
            <v-text-field
                v-model="Username"
                label="UserName"
                outlined
            ></v-text-field>
            <v-text-field
                v-model="Password"
                label="Password"
                outlined
            ></v-text-field>
          </v-form>
          <div class="text-right">
            <v-btn color="primary" @click='login'>
              Login
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>
<script>
export default {
  data: () => ({
    Username:'',
    Password: '',
    errorMessage:''
  }),

  method: {
    async login () {
try {

  const {tokens} = await axios.post('http://localhost:8000/auth/login', {Username: this.username, Password: this.password});
  localStorage.setItem('access', response.data.access);
  localStorage.setItem('refresh', response.data.refresh);

  this.$router/PushManager('/')

}catch(error) {
  console.error('login failed.');
  console.error(error.response.data)
  this.errorMessage = error.response.data.error;
}
    },
    clearError(){
      this.errorMessage = '';
    }
  }
}
</script>
