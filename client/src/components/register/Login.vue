<template>
	<v-container>
		<v-layout row wrap align-center justify-center>
			<v-flex xs12 sm8 lg4 md5>
				<v-card class='login-card'>
					<v-card-title>
						<h1 class='login_title'>Bandueにログイン</h1>
					</v-card-title>

					<v-spacer/>

					<v-card-text>
						<v-layout
							row
							fill-height
							justify-center
							align-center
							v-if='loading'
						>

							<v-progress-circular
								:size='50'
								color='primary'
								indeterminate
							/>
						</v-layout>

						<v-form v-else ref='form' v-model='valid' lazy-validation>
							<v-container>
								<v-text-field
									v-model='credentials.username'
									:counter='70'
									label='メールまたは、ユーザー名'
									maxlenght='70'
									required
								/>

								<v-text-field
									type='password'
									v-model='credentials.password'
									:counter='32'
									label='パスワード'
									maxlength='32'
									required
								/>
							</v-container>
							<v-btn class='pink white--text' :disabled='!valid' @click='login'>ログイン</v-btn>
						</v-form>
					</v-card-text>

					<v-card-text>
						<a href="#">パスワードをお忘れですか?</a>
						<a href="#">アカウントを作成</a>
					</v-card-text>
				</v-card>
			</v-flex>
		</v-layout>
	</v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data: () => ({
    credentials: {},
    valid: true,
    loading: false
  }),
  methods: {
    login () {
      if (this.$refs.form.validate()) {
        this.loading = true
        axios.post('http://192.168.33.12:8000/auth/', this.credentials)
          .then(res => {
            this.$session.start()
            this.session.set('token', res.data.token)
          })
          .catch(e => {
            this.loading = false
          })
      }
    }
  }
}
</script>
