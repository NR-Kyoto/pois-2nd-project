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
                v-model="username"
                label="UserName"
                outlined
            ></v-text-field>
            <v-text-field
                type="password"
                v-model="password"
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
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:8000/login/', {
          username: this.username,
          password: this.password,
        });

        window.sessionStorage.setItem('access', response.data.access);
        sessionStorage.setItem('refresh', response.data.refresh);
        sessionStorage.setItem('username', this.username)

        window.location.href = "/";
      } catch (error) {
        console.error('Login failed.');
        console.error(error.response.data);
        this.errorMessage = error.response.data.error || 'ログインに失敗しました';
      }
    },
    clearError() {
      this.errorMessage = '';
    },
  },
};
</script>