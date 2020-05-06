<template>
	<v-card
		class='pa-3'
		outlined
	>
		<v-card-title class="text-center">
			<h1 class="register_title">BandueにSignInする</h1>
		</v-card-title>

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
			></v-text-field>

			<v-col class='text-center' cols='12'>
				<v-btn
					depressed
					x-large
					class='teal lighten-4'
					:disabled='!valid'
					@click='login'
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
</template>

<script>
	import axios from 'axios'
	import { Common } from '@/static/js/common'

	const Com = new Common()
	export default {
		name: 'signin',
		data: () => ({
			valid: true,
			loading: false,
			showPassword: false,
			credentials: {},
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
		methods: {
			login () {
				console.log(this.credentials)
				axios.post('http://192.168.33.12:8000/auth/', this.credentials)
				.then(res => {
					this.$session.start()
					this.$session.set('token', res.data.token)
					this.$session.set('username', JSON.parse(res.config.data).username)
					this.$router.push('/')
					Com.reload(this.$router)
				})
				.catch(e => {
					console.log(e)
				})
			},

			reload () {
				Com.reload(this.$router)
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
