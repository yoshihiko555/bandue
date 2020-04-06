import Vue from 'vue'
import test from '@/static/js/inclueds'
import SignIn from './SignIn'
import SignUp from './SignUp'
import Header from '../common/Header'
import Footer from '../common/Footer'
import vuetify from '../../plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
require('@/static/scss/main.scss')
// require('@/static/js/inclueds')

Vue.config.productionTip = false

// 以下でグローバルコンポーネントの登録をしている
// 第一引数に名前を指定して、DjangoのHTML側で<signup></signup>でコンポーネントを呼び出す事ができる
Vue.component('signup', SignUp)
Vue.component('signin', SignIn)
Vue.component('my-header', Header)
Vue.component('my-footer', Footer)

new Vue({
	vuetify,
	test
}).$mount('#register')
