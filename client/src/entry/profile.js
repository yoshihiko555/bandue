import Vue from 'vue'
import Profile from '@/components/pages/Profile.vue'
import router from '@/router'
import store from '@/store'
import vuetify from '@/plugins/vuetify'
import 'vuetify/dist/vuetify.min.css'
import VueSession from 'vue-session'
import eventHub from '@/plugins/eventHub'
require('@/static/scss/main.scss')

Vue.config.productionTip = false

Vue.use(VueSession)
Vue.use(eventHub)

Vue.component('profile', Profile)

new Vue({
	vuetify,
	router,
	store,
	data: {

	},
	methods: {

	}
}).$mount('#profile')
