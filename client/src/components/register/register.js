import Vue from 'vue'
import SignIn from './SignIn'
import SignUp from './SignUp'
import Header from '../common/Header'
import Footer from '../common/Footer'
import vuetify from '../../plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'

Vue.config.productionTip = false

// 以下でグローバルコンポーネントの登録をしている
// 第一引数に名前を指定して、DjangoのHTML側で<signup></signup>でコンポーネントを呼び出す事ができる
Vue.component('signup', SignUp)
Vue.component('signin', SignIn)
Vue.component('my-header', Header)
Vue.component('my-footer', Footer)

new Vue({
	vuetify
}).$mount('#register')
