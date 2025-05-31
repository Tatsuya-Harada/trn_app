import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
//import router from './router'
import router from './router/index';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css';
import BootstrapVue3 from 'bootstrap-vue-3';

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(BootstrapVue3);
app.mount('#app')