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

						<v-card
							class='pa-3'
							outlined
						>
							<v-card-title>
								<h1 class="register_title">BandueにSignUpする</h1>
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
									:rules='rules.username'
									:counter='70'
									maxlength='70'
									label='Mail or UserId'
									:id='id'
									required
									clear-icon='✕'
									clearable
								></v-text-field>

								<v-text-field
									v-model='credentials.password'
									:rules='rules.password'
									:counter='70'
									maxlength='70'
									label='Password'
									required
									clear-icon='✕'
									clearable
								></v-text-field>

								<v-col class='text-center' cols='12'>
									<v-btn
										depressed
										x-large
										class='teal lighten-4'
										:disabled='!valid'
										@click='login'
									>SignUp</v-btn>
								</v-col>
							</v-form>

						</v-card>
					</v-row>
				</v-col>
			</v-row>
		</v-container>
	</v-app>
</template>

<script>
	import axios from 'axios'
	export default {
		props: ['id'],
		data: () => ({
			valid: true,
			loading: false,
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
				// test()
				axios.post('http://192.168.33.12/auth/', this.credentials)
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
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
