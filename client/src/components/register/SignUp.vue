<template>
	<v-card
		class='pa-3 signup_wrap'
		outlined
	>
		<v-card-title>
			<h1 class="register_title" val='Testデータ'>BandueにSignUpする</h1>
		</v-card-title>

		<!-- v-model='valid'で、入力項目のvalidationがすべてOKになったらtrueになる。
		それまではvalidはfalse -->
		<v-form ref='form' v-model='valid'>
			<!-- v-modelでデータとの紐付け
			:rulesでscript内で設定したValidationとの紐付け
			:idでpropsで親コンポーネント側からデータを紐付ける
			今回の場合の親コンポーネントは、Djangoテンプレート側 -->
			<v-text-field
				v-model='credentials.username'
				:rules='usernameValidation'
				:counter='70'
				maxlength='70'
				label='UserName'
				required
				clearable
				tabindex='1'
				:loading='loading'
			></v-text-field>

			<v-text-field
				v-model='credentials.email'
				:rules='rules.email'
				:counter='70'
				maxlength='70'
				label='Mail'
				required
				clearable
				tabindex='2'
			></v-text-field>

			<v-text-field
				v-model='credentials.password'
				:append-icon='showPassword ? "mdi-eye" : "mdi-eye-off"'
				:type='showPassword ? "text" : "password"'
				:rules='rules.password'
				:counter='70'
				maxlength='70'
				label='Password'
				required
				tabindex='3'
				@click:append='showPassword = !showPassword'
				:class='{icon_hide:isIcon}'
				@keyup='passAction'
				ref='pass'
			></v-text-field>

			<v-col class='text-center' cols='12'>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-1'
					:disabled='!valid'
					@click='confirm'
					tabindex='4'
				>次へ</v-btn>
			</v-col>
		</v-form>
	</v-card>
</template>

<script>
	import _ from 'lodash'
	import axios from 'axios'
	import { Const } from '@/static/js/const'

	const Con = new Const()

	export default {
		name: 'signup',
		data: () => ({
			valid: true,
			loading: false,
			credentials: {},
			showPassword: false,
			isIcon: true,
			isUserDuplication: true,
			diff: false,
			rules: {
				// username: [
					// v => !!v || '必須項目です',
					// v => (v && v.length <= 70) || '70文字以内で入力してください',
					// v => this.isUserDuplication || '既に登録済みのユーザーです',
				// ],
				email: [
					v => !!v || '必須項目です',
				],
				password: [
					v => !!v || '必須項目です',
					v => (v && v.length >= 8 && v.length <= 70) || '8文字以上、70文字以内で入力してください'
					// v => //.test(v) || '半角英数字を1文字以上含めてください'		// TODO: 正規表現後で考える
				]
			},
		}),
		watch: {
			'credentials.username': function (val) {
				if (val !== '' && val !== null) {
					this.loading = true
					this.checkUsername(val)
				}
			}
		},
		computed: {
			usernameValidation () {
				const rules = []
				rules.push(v => !!v || '必須項目です')
				rules.push(v => (v && v.length <= 70) || '70文字以内で入力してください')
				if (!this.isUserDuplication) {
					rules.push(v => false || '既に登録済みのユーザーです')
				}
				return rules
			}
		},
		methods: {
			confirm () {
				this.$emit('signup-change-view', Con.SIGNUP_CONFRIM_VIEW, this.credentials)
			},

			passAction (e) {
				var keycode = e.keyCode
				var len = this.$refs.pass.computedCounterValue

				// Enter
				if (keycode === 13 && this.valid) {
					console.log('Enterで送信')
					this.confirm()
				} else {
					if (len !== 0) {
						this.isIcon = false
					} else {
						this.isIcon = true
					}
				}
			},
			// イベントの間引き処理(イベント発火の１秒後にajaxが飛ぶ)
			checkUsername: _.debounce(function checkUsername(val) {
				axios({
					methods: 'GET',
					url: 'http://192.168.33.12:8000/api/users/checkUserDuplication/',
					params: {
						username: val
					}
				})
				.then(res => {
					console.log(res.data)
					this.isUserDuplication = res.data.result
					this.loading = false
				})
				.catch(e => {
					console.log(e)
					this.loading = false
				})
			}, 1000),
		}
	}
</script>

<style lang='scss'>
.signup_wrap{
	.icon_hide {
		.v-icon::before {
			display: none;
		}
	}
}
</style>
