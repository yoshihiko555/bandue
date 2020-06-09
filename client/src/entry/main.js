import Vue from 'vue'
import IsAuth from '@/components/pages/IsAuth.vue'
import Explore from '@/components/pages/Explore.vue'
import Home from '@/components/pages/Home.vue'
import Bbs from '@/components/pages/Bbs.vue'
import Message from '@/components/pages/Message.vue'
import Profile from '@/components/pages/Profile.vue'
import Setting from '@/components/pages/Setting.vue'
import router from '@/router'
import { store, initialState } from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
import eventHub from '@/plugins/eventHub'
import http from '@/plugins/http'
require('@/static/scss/main.scss')

Vue.config.productionTip = false
Vue.prototype.$store = store

Vue.use(VueSession)
Vue.use(eventHub)
Vue.use(http)

// TODO:あとで以下のstoreを使って認証管理を行う
// window.state = store.state

Vue.component('is-auth', IsAuth)
Vue.component('explore', Explore)
Vue.component('home', Home)
Vue.component('bbs', Bbs)
Vue.component('message', Message)
Vue.component('profile', Profile)
Vue.component('setting', Setting)

new Vue({
  router,
  store,
  vuetify,
  created () {
      console.log('認証情報：', Vue.prototype.$store.state)
      sessionStorage.setItem('initialState', JSON.stringify(initialState))
  }
}).$mount('#main')
