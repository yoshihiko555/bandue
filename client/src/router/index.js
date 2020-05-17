import Vue from 'vue'
import VueRouter from 'vue-router'
import SignUp from '@/components/register/SignUp.vue'
import SignIn from '@/components/register/SignIn.vue'
import Profile from '@/components/pages/Profile.vue'

Vue.use(VueRouter)

const routes = [
  // 試しに定義してみたけど、あまり関係なさそう
  // そもそもルーティングはDjangoで行っているから
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
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
