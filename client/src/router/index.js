import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '@/components/register/SignUp.vue'
import SignIn from '@/components/register/SignIn.vue'
import Home from '@/components/pages/Home.vue'
import Profile from '@/components/pages/Profile.vue'
import Bbs from '@/components/pages/Bbs.vue'
import Info from '@/components/pages/Info.vue'
import Message from '@/components/pages/Message.vue'
import Setting from '@/components/pages/Setting.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUp
    },
    {
        path: '/signin',
        name: 'SignIn',
        component: SignIn
    },
    {
        path: '/profile/:username',
        name: 'Profile',
        component: Profile
    },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
