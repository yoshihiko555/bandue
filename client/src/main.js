import Vue from 'vue'
import Index from './Index.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import axios from 'axios'
import VueSession from 'vue-session'
require('@/static/scss/main.scss')

Vue.config.productionTip = false

Vue.use(VueSession)

Vue.component('index', Index)

new Vue({
  router,
  store,
  vuetify,
  data: {
      datas: [],
      isAuth: false
  },
  mounted: function () {
      axios.get('http://192.168.33.12:8000/api/tweet/')
      .then(res => {
          console.log(res)
          this.$session.start()
          console.log('ログイン状態', this.$session.has('token'))
          this.isAuth = this.$session.has('token')
          this.datas = res.data
          console.log(this.datas)
      })
      .catch(e => {
          console.log('エラーが発生しました')
          console.log(e)
      })
  },
  methods: {

  }

}).$mount('#app')
