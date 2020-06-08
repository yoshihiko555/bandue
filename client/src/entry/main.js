import Vue from 'vue'
import IsAuth from '@/components/pages/IsAuth.vue'
import Explore from '@/components/pages/Explore.vue'
import Home from '@/components/pages/Home.vue'
import Bbs from '@/components/pages/Bbs.vue'
import Message from '@/components/pages/Message.vue'
import Profile from '@/components/pages/Profile.vue'
import Setting from '@/components/pages/Setting.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
import eventHub from '@/plugins/eventHub'
require('@/static/scss/main.scss')

Vue.config.productionTip = false

Vue.use(VueSession)
Vue.use(eventHub)

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
}).$mount('#main')
