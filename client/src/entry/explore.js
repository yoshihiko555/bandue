import Vue from 'vue'
import Explore from '@/components/pages/Explore.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueSession from 'vue-session'
require('@/static/scss/main.scss')

Vue.config.productionTip = false

Vue.use(VueSession)

Vue.component('explore', Explore)

new Vue({
  router,
  store,
  vuetify,
  data: {

  },
  methods: {

  }
}).$mount('#explore')
