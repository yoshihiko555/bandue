import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistedstate from 'vuex-persistedstate'
import router from '@/router'
import { Common } from '@/static/js/common'
const Com = new Common()

Vue.use(Vuex)

// 初期値設定
export const initialState = {
    isAuth: false,
    token: '',
    loginUser: '',
}

export const store = new Vuex.Store({
  state: initialState,
  mutations: {
      // 認証成功後のデータを設定
      setToken: function (state, payload) {
          console.log('認証データの設定', payload)
          state.isAuth = true
          state.token = payload.res.token
          state.loginUser = payload.req.username
      },
      // 認証データの初期化
      initState: function (state) {
          console.log('認証状態初期化')
          Object.assign(state, JSON.parse(sessionStorage.getItem('initialState')))
      }
  },
  actions: {
      // 認証チェック
      AuthCheckAction: function (ctx, kwargs) {
          Vue.prototype.$axios({
              method: 'POST',
              url: 'auth/',
              data: kwargs
          })
          .then(res => {
              console.log(res)
              this.commit('setToken', { res: res.data, req: res.requestData })
              router.push('/')
              Com.reload(router)
          })
          .catch(e => {
              console.log(e)
          })
      }
  },
  modules: {
  },
  // 認証データの保存先をセッションに設定
  plugins: [VuexPersistedstate({storage: window.sessionStorage})]
})
