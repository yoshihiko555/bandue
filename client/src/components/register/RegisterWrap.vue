<template>
	<v-app id='register_wrap'>
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
					<div v-if='view == 0'>
							<keep-alive>
								<SignUp
									v-if='signupCnt === 0'
									@signup-change-view='signupView'
								>
								</SignUp>
								<SignUpConf
									v-else-if='signupCnt === 1'
									@signup-change-view='signupView'
									:data='credentials'
								></SignUpConf>
								<SignUpDone
									v-else-if='signupCnt === 2'
								>
								</SignUpDone>
							</keep-alive>
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
	</v-app>
</template>

<script>
	import SignUp from './SignUp'
	import SignUpConf from './SignUpConfirm'
	import SignUpDone from './SignUpDone'
	import SignIn from './SignIn'

	export default {
		props: ['data', 'view', 'signupUrl'],
		components: {
			SignUp,
			SignUpConf,
			SignUpDone,
			SignIn
		},
		data: () => ({
			signupCnt: 0,
			credentials: {}
		}),
		created: function () {
			console.log(this.signupUrl)
		},
		methods: {
			signupView (currentNo, credentials) {
				this.signupCnt = currentNo
				this.credentials = credentials
				console.log(this.credentials)
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
