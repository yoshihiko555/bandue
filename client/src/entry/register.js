import Vue from 'vue'
import RegisterWrap from '@/components/register/RegisterWrap'
import router from '@/router'
import { store, initialState } from '@/store'
import vuetify from '@/plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueSession from 'vue-session'
import http from '@/plugins/http'
require('@/static/scss/main.scss')

Vue.config.productionTip = false
Vue.prototype.$store = store

Vue.use(VueSession)
Vue.use(http)

// window.state = store.state

// 以下でグローバルコンポーネントの登録をしている
// 第一引数に名前を指定して、DjangoのHTML側で<signup></signup>でコンポーネントを呼び出す事ができる
Vue.component('register-wrap', RegisterWrap)

new Vue({
	vuetify,
	router,
	store,
	created () {
		sessionStorage.setItem('initialState', JSON.stringify(initialState))
	}
}).$mount('#register')
