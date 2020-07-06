import Vue from 'vue'
import IsAuth from '@/components/pages/IsAuth.vue'
import Explore from '@/components/pages/Explore.vue'
import Home from '@/components/pages/Home.vue'
import Bbs from '@/components/pages/Bbs.vue'
import Message from '@/components/pages/Message.vue'
import Info from '@/components/pages/Info.vue'
import Profile from '@/components/pages/Profile.vue'
import Setting from '@/components/pages/Setting.vue'
import PageNotFound from '@/components/pages/PageNotFound.vue'
import router from '@/router'
import { store, initialState } from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
import eventHub from '@/plugins/eventHub'
import http from '@/plugins/http'
import truncate from '@/filters/truncate'
require('@/static/scss/main.scss')

Vue.config.productionTip = false
Vue.prototype.$store = store
// Vue.prototype.$vuetify = vuetify

Vue.use(VueSession)
Vue.use(eventHub)
Vue.use(http)

Vue.component('is-auth', IsAuth)
Vue.component('explore', Explore)
Vue.component('home', Home)
Vue.component('bbs', Bbs)
Vue.component('message', Message)
Vue.component('info', Info)
Vue.component('profile', Profile)
Vue.component('setting', Setting)
Vue.component('page-not-found', PageNotFound)

new Vue({
  router,
  store,
  vuetify,
  created () {
      sessionStorage.setItem('initialState', JSON.stringify(initialState))
      this.$vuetify.theme.isDark = this.$store.state.settings.isDark
  },
  computed: {
	  isDark () {
		  return this.$store.getters['settings/getIsDark']
	  }
  },
  watch: {
	  isDark (val, old) {
		  this.$vuetify.theme.isDark = val
	  }
  }

}).$mount('#main')
