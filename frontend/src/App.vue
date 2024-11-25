<template>
  <div id="app">
    <h1>Qwizzo AI com TypeScript</h1>

    <!-- Formulário de login -->
    <div>
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="handleLogin">Login</button>
    </div>

    <!-- Mostrar a mensagem de acesso protegido -->
    <div v-if="message">
      <p>{{ message }}</p>
    </div>

    <!-- Botão para acessar a rota protegida -->
    <div v-if="token">
      <button @click="getProtectedData">Acessar Rota Protegida</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { login, getProtectedData } from './authService';  

interface Data {
  username: string;
  password: string;
  token: string;
  message: string;
}

export default defineComponent({
  name: 'App',
  data(): Data {
    return {
      username: '',
      password: '',
      token: localStorage.getItem('token') || '',  
      message: ''  
    };
  },
  methods: {
    async handleLogin(): Promise<void> {
  try {
    const token = await login(this.username, this.password);
    this.token = token;
    localStorage.setItem('token', token);
    this.message = 'Login bem-sucedido!';
  } catch (error) {
    this.message = 'Erro no login';
  }
},

    // Função para acessar a rota protegida
    async getProtectedData(): Promise<void> {
      try {
        const data = await getProtectedData();  // Obtém os dados da rota protegida
        this.message = `Mensagem: ${data.message}`;  // Atualiza a mensagem com a resposta da API
      } catch (error) {
        this.message = 'Erro ao acessar a rota protegida';
      }
    }
  }
});
</script>

<style scoped>
input {
  margin: 5px;
}

button {
  margin-top: 10px;
}
</style>
