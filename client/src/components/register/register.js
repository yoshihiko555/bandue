import Vue from 'vue'
import SignIn from './SignIn'
import SignUp from './SignUp'
import Header from '../common/Header'
import Footer from '../common/Footer'
import vuetify from '../../plugins/vuetify'

Vue.config.productionTip = false

Vue.component('signup', SignUp)
Vue.component('signin', SignIn)
Vue.component('my-header', Header)
Vue.component('my-footer', Footer)

new Vue({
	vuetify
}).$mount('#register')
