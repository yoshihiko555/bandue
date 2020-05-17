import Vue from 'vue'
import Home from '@/components/pages/Home.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
import eventHub from '@/plugins/eventHub'
import { Common } from '@/static/js/common'
require('@/static/scss/main.scss')

const Com = new Common()

Vue.config.productionTip = false

Vue.use(VueSession)
Vue.use(eventHub)

// TODO:あとで以下のstoreを使って認証管理を行う
// window.state = store.state

Vue.component('home', Home)

new Vue({
  router,
  store,
  vuetify,
  data: {
    isAuth: false,
    lodding: true
  },
  mounted: function () {
    this.$session.start()
    console.log('ログイン状態', this.$session.has('token'))
    this.isAuth = this.$session.has('token')
    this.lodding = false

    if (!this.$session.has('token')) {
        router.push('/signin')
        Com.reload(this.$router)
    }
  },
  methods: {

  }

}).$mount('#home')
