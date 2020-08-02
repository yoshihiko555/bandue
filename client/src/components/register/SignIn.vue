<template>
    <v-app id='signin_wrap'>
        <Header/>
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
                        <v-card
                            class='pa-3 signin_wrap'
                            outlined
                            width=400
                        >
                            <v-card-title class="text-center">
                                <h1 class="register_title">BandueにSignInする</h1>
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

                                <v-col class='text-center' cols='12'>
                                    <v-btn
                                        depressed
                                        x-large
                                        class='teal lighten-4'
                                        :disabled='!valid'
                                        @click='signin'
                                        tabindex='3'
                                    >SignIn</v-btn>
                                </v-col>

                                <v-row>

                                    <v-col class='text-center' cols='6'>
                                        <v-btn
                                            href='#'
                                        >パスワードを<br>お忘れですか？</v-btn>
                                    </v-col>
                                    <v-col class='text-center' cols='6'>
                                        <v-btn
                                            to='/signup'
                                            @click='reload'
                                        >SignUp</v-btn>
                                    </v-col>
                                </v-row>
                            </v-form>
                        </v-card>
                    </v-row>
                </v-col>
            </v-row>
        </v-container>
        <Footer/>
    </v-app>
</template>

<script>
    import Header from '../common/Header'
    import Footer from '../common/Footer'

	import { mapState } from 'vuex'
    import { Common } from '@/static/js/common'

	const Com = new Common()
	export default {
        name: 'signin',
        components: {
            Header,
            Footer,
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
				// Com.reload(this.$router)
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
#signin_wrap {
	> div {
		min-height: inherit;
	}
	.register_card_wrap {
		height: calc(100vh - #{($header + $footer)});

		.signin_wrap {
			.icon_hide {
				.v-icon::before {
					display: none;
				}
			}
		}
	}
	.register_title {
		font-size: 28px;
	}
}
</style>
