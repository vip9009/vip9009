import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import '@fontsource/lato/400.css'
import '@fontsource/lato/700.css'
import '@fontsource/lato/900.css'
import './assets/styles/main.css'

createApp(App).use(router).mount('#app')
