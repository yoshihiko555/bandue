import Vue from 'vue'
import IsAuth from '@/components/pages/IsAuth.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import VueSession from 'vue-session'
import { Common } from '@/static/js/common'
require('@/static/scss/main.scss')

const Com = new Common()
Vue.config.productionTip = false

Vue.use(VueSession)

Vue.component('is-auth', IsAuth)

new Vue({
  router,
  store,
  vuetify,
  data: {

  },
  mounted: function () {
      this.$session.start()
      if (this.$session.has('token')) {
          // HOMEへ
          router.push('/home')
          Com.reload(this.$router)
      } else {
          // 未認証ページへ
          router.push('/explore')
          Com.reload(this.$router)
      }
  },
  methods: {

  }

}).$mount('#isAuth')
