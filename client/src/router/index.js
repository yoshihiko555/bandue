import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import SignUp from '@/components/register/SignUp.vue'
import SignIn from '@/components/register/SignIn.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
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
  }

]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
