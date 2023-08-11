import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import Toast, { POSITION } from 'vue-toastification'
import store from './store'
import router from './router'

import 'vue-toastification/dist/index.css'

const app = createApp(App)

app.use(Toast, {
  position: POSITION.BOTTOM_CENTER
})

app.use(router)

app.use(store)

app.mount('#app')

store.dispatch('fetchIpAddress')
