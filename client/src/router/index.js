import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUpWrap from '@/components/register/SignUpWrap.vue'
import SignIn from '@/components/register/SignIn.vue'
import IsAuth from '@/components/pages/IsAuth.vue'
import Home from '@/components/pages/Home.vue'
import Explore from '@/components/pages/Explore.vue'
import Profile from '@/components/pages/Profile.vue'
import Bbs from '@/components/pages/Bbs.vue'
import Info from '@/components/pages/Info.vue'
import Message from '@/components/pages/Message.vue'
import Setting from '@/components/pages/Setting.vue'
import PageNotFound from '@/components/pages/PageNotFound.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'IsAuth',
        component: IsAuth
    },
    {
        path: '/explore',
        name: 'Explore',
        component: Explore
    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/bbs',
        name: 'Bbs',
        component: Bbs
    },
    {
        path: '/message',
        name: 'Message',
        component: Message
    },
    {
        path: '/info',
        name: 'Info',
        component: Info
    },
    {
        path: '/profile/:username/',
        name: 'Profile',
        component: Profile
    },
    {
        path: '/setting',
        name: 'Setting',
        component: Setting
    },
    {
        path: '/404',
        name: 'PageNotFound',
        component: PageNotFound
    },
    {
        path: '/signup',
        name: 'SignUp',
        component: SignUpWrap
    },
    {
        path: '/signin',
        name: 'SignIn',
        component: SignIn
    },
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
