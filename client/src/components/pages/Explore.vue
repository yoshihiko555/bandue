<template>
	<v-app>
		<v-container id='explore_wrap'>
			<v-row class="explore_main">
				<v-col cols='6' class="explore_content">
					<img src='@/static/img/explore_img.jpg' alt=''>
				</v-col>
				<v-col cols='6' class="explore_register">
					<v-card
						class='pa-3'
						outlined
					>
						<v-card-title>
							<img src='@/static/img/Logo_Icon&Text.png' alt="logo" width="150">
						</v-card-title>

						<v-alert
							dense
							outlined
							type='error'
							transition='scale-transition'
							v-show='checkAuth'
						>
							<strong>ユーザー名</strong>、または<strong>パスワード</strong>が間違っています。再度入力し直してください。
						</v-alert>

						<v-form ref='form' v-model='valid'>
							<v-text-field
								v-model='credentials.username'
								:rules='rules.username'
								:counter='70'
								maxlength='70'
								label='Mail or UserId'
								required
								clearable
								tabindex='1'
							></v-text-field>

							<v-text-field
								v-model='credentials.password'
								:append-icon='showPassword ? "mdi-eye" : "mdi-eye-off"'
								:rules='rules.password'
								:counter='70'
								:type='showPassword ? "text" : "password"'
								maxlength='70'
								label='Password'
								required
								tabindex='2'
								@click:append='showPassword = !showPassword'
								:class='{icon_hide:isIcon}'
								@keyup='passAction'
								ref='pass'
							></v-text-field>

							<div class="text-center">
								<v-btn
									depressed
									class='teal lighten-4'
									:disabled='!valid'
									@click='signin'
									tabindex='3'
								>SignIn</v-btn>
							</div>
						</v-form>
					</v-card>

					<v-card
						class='pa-3 mt-3 text-center'
						outlined
					>
						<p class='explore_text'>
							アカウントをお持ちでないですか？
							<v-btn
								text
								to='/signup'
								@click='reload'
								color='blue'
							>
								SignUp
							</v-btn>
						</p>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
		<Footer/>
	</v-app>
</template>

<script>
	import Footer from '@/components/common/Footer'
	import { mapState } from 'vuex'
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'Explore',
		components: {
			Footer
		},
		data: () => ({
			valid: true,
			showPassword: false,
			credentials: {},
			isIcon: true,
			rules: {
				username: [
					v => !!v || '必須項目です',
					v => (v && v.length <= 70) || '70文字以内で入力してください'
				],
				password: [
					v => !!v || '必須項目です',
					v => (v && v.length >= 8 && v.length <= 70) || '8文字以上、70文字以内で入力してください'
					// v => //.test(v) || '半角英数字を1文字以上含めてください'		// TODO: 正規表現後で考える
				]
			}
		}),
		created () {
			this.$store.dispatch('auth/refreshAuth')
		},
		computed: {
			...mapState('auth', ['checkAuth'])
		},
		methods: {
			signin () {
				console.log('入力情報', this.credentials)
				this.$store.dispatch('AuthCheckAction', this.credentials)
			},
			reload () {
				Com.reload(this.$router)
			},

 			passAction (e) {
				var keycode = e.keyCode
				var len = this.$refs.pass.computedCounterValue

				// Enter
				if (keycode === 13 && this.valid) {
					this.signin()
				} else {
					if (len !== 0) {
						this.isIcon = false
					} else {
						this.isIcon = true
					}
				}
			}
		}
	}
</script>

<style lang='scss'>
#explore_wrap {
	min-height: calc(100vh - #{$footer}) !important;

	.explore_main {
		margin-top: 100px;

		.explore_content {
			img {
				width: 100%;
			}
		}

		.explore_register {
			.icon_hide {
				.v-icon::before {
					display: none;
				}
			}

			.explore_text {
				margin: 0;
			}
		}
	}

}
</style>
