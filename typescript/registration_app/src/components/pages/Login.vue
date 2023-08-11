<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const username = ref('')
const password = ref('')

async function onLogin(e: any) {
  try {
    await store.dispatch('loginUser', {
      username: username.value,
      password: password.value
    })
    router.push('/profile')
  } catch (error) {
    return
  }
}

function onNavigateToRegister() {
  router.push('/register')
}
</script>

<template>
  <main>
    <header>
      <h2>Login</h2>
    </header>
    <form @submit.prevent="onLogin">
      <label for="username">Username or Email</label>
      <input
        v-model="username"
        name="username"
        type="text"
        placeholder="Enter username or email here"
      />

      <label for="password">Password</label>
      <input v-model="password" name="password" type="password" placeholder="Enter password" />

      <button type="submit" class="loginbtn">Login</button>
    </form>
    <button @click="onNavigateToRegister" class="registerbtn">Go to Registration Page</button>
  </main>
</template>

<style scoped>
input {
  width: 100%;
  padding: 15px;
  margin: 5px 0 22px 0;
  display: inline-block;
  border: none;
  background: #f1f1f1;
}

button {
  background-color: #04aa6d;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

button:hover {
  opacity: 1;
}

.registerbtn {
  background-color: #107ab0;
}

main {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 60vw;
}

header {
  margin-bottom: 15px;
}
</style>
