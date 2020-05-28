<template>
	<v-app id='register_wrap'>
		<Header></Header>
		<v-container
			fluid
			class='pa-0'
		>
			<v-row>
				<v-col cols='12' class="pa-0">
					<v-row
						align='center'
						justify='center'
						class='teal darken-4 register_card_wrap'

					>
					<!-- Django側から受け取ったviewの値で表示するコンポーネントを判定
					0 = signup
					1 = signin -->
					<div v-if='view == 0'>
						<!-- TODO : 切替時のアニメーション追加 -->
						<!-- 以下のtransitionでwrapしてあげると、アニメーションの使用が可能になるけど、まだ使い方がよくわからない -->
						<!-- <transition name='fade' mode='out-in'> -->
						<keep-alive>
							<!-- pageメソッドでコンポーネントの切り替え
							子コンポーネントのsignuo-change-viewが発火されたことを確認して、signupViewメソッドが発火
							signupViewメソッドで受け取ったsignUpCntで表示切り替え -->
							<component
								:is='page'
								@signup-change-view='signupView'
								:data='credentials'
							></component>
						</keep-alive>
						<!-- </transition> -->
					</div>

					<div v-else-if='view == 1'>
						<SignIn
							signup-url='this.signupUrl'
						>
						</SignIn>
					</div>

					</v-row>
				</v-col>
			</v-row>
		</v-container>
		<Footer></Footer>
	</v-app>
</template>

<script>
import Header from '../common/Header'
import Footer from '../common/Footer'
import SignUp from './SignUp'
import SignUpConf from './SignUpConfirm'
import SignUpDone from './SignUpDone'
import SignIn from './SignIn'

import { Const } from '@/static/js/const'

const Con = new Const()

export default {
  props: ['view'],
  components: {
    Header,
    Footer,
    SignUp,
    SignUpConf,
    SignUpDone,
    SignIn
  },
  data: () => ({
    signupCnt: 0,
    credentials: {}
  }),
  computed: {
    page () {
      switch (this.signupCnt) {
        case Con.SIGNUP_VIEW:
          return SignUp

        case Con.SIGNUP_CONFRIM_VIEW:
          return SignUpConf

        case Con.SIGNUP_DONE_VIEW:
          return SignUpDone

        default:
          return SignUp
      }
    }
  },
  methods: {
    signupView (currentNo, credentials) {
      this.signupCnt = currentNo
      this.credentials = credentials
    }
  }
}
</script>

<style lang='scss'>
#register_wrap {
	> div {
		min-height: inherit;
	}
	.register_card_wrap {
		height: calc(100vh - #{($header + $footer)});
	}
	.register_title {
		font-size: 28px;
	}
}
</style>
