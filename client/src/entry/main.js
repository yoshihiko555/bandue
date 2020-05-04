import Vue from 'vue'
import Index from '@/components/pages/Index.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
require('@/static/scss/main.scss')

Vue.config.productionTip = false

Vue.use(VueSession)

// TODO:あとで以下のstoreを使って認証管理を行う
// window.state = store.state

Vue.component('index', Index)

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
  },
  methods: {

  }

}).$mount('#app')
