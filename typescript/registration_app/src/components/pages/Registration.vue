<script setup lang="ts">
import { ref } from "vue"
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

const first = ref("");
const last = ref("");
const username = ref("");
const email = ref("");
const password = ref("");

async function onRegister(e: any) {
  try {
    await store.dispatch("registerUser", {
        first: first.value,
        last: last.value,
        username: username.value,
        email: email.value,
        password: password.value,
    })
    router.push("/profile")
  } catch(error) {
    return;
  }
}

function onNavigateToLogin() {
  router.push("/")
}

</script>

<template>
  <main>
    <header>
      <h2>Registration</h2>
    </header>
    <form @submit.prevent="onRegister">
      <label for="first">First Name</label>
      <input v-model="first" name="first" type="text" placeholder="Enter first name" required/>

      <label for="last">Last Name</label>
      <input v-model="last" name="last" type="text" placeholder="Enter last name" requied/>

      <label for="username">Username</label>
      <input v-model="username" name="username" type="text" placeholder="Enter username" required/>

      <label for="email">Email</label>
      <input v-model="email" name="email" type="email" placeholder="Enter email" required/>

      <label for="password">Password</label>
      <input v-model="password" name="password" type="password" placeholder="Enter password" required minlength="6"/>

      <button type="submit" class="registerbtn">Register</button>
    </form>
    <button @click="onNavigateToLogin" class="loginbtn">Go to Login Page</button>
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
  background-color: #04AA6D;
  color: white;
  padding: 16px 20px;
  margin: 8px 0;
  border: none;
  cursor: pointer;
  width: 100%;
  opacity: 0.9;
}

button:hover {
  opacity:1;
}

.loginbtn {
  background-color: #107AB0;
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