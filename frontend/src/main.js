import Vue from 'vue'
import { BootstrapVue, IconsPlugin, SpinnerPlugin } from 'bootstrap-vue'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import axios from 'axios'
import titleMixin from './mixins/titleMixin'

// DEV
//const baseURL = 'http://localhost:8001';

// TEST
const baseURL = 'https://pdf.db.rv.ua';

// PROD
// const baseURL = 'https://pdf.db.rv.ua';

axios.defaults.baseURL = baseURL;

Vue.config.productionTip = false

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(SpinnerPlugin)
Vue.mixin(titleMixin)

new Vue({
  render: h => h(App),
}).$mount('#app')
