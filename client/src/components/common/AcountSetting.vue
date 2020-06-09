<template>
	<div class="">
		<v-card
			tile
			outlined
		>
			<v-card-title>{{ profileData.username }}</v-card-title>

			<v-form>
				<v-container>
					<!-- ユーザー名 -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Username</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-text-field
								v-model='profileData.username'
								:counter='70'
								maxlength='70'
								:value="profileData.username"
							>
							</v-text-field>
						</v-col>
					</v-row>

					<!-- 自己紹介 -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Instroduction</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-textarea
								v-model='profileData.instroduction'
								:value="profileData.instroduction"
							>
							</v-textarea>
						</v-col>
					</v-row>

					<!-- メールアドレス -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>E-Mail</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-text-field
								v-model='profileData.email'
								:counter='70'
								maxlength='70'
								:value="profileData.email"
							>
							</v-text-field>
						</v-col>
					</v-row>

					<!-- パスワード -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Password</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-text-field
								type='password'
								:counter='70'
								maxlength='70'
								placeholder='CurrentPassword'
								color='grey'
							>
							</v-text-field>
							<v-text-field
								type='password'
								:counter='70'
								maxlength='70'
								placeholder='NewPassword'
							>
							</v-text-field>
							<v-text-field
								type='password'
								:counter='70'
								maxlength='70'
								placeholder='ConfirmPassword'
							>
							</v-text-field>
						</v-col>
					</v-row>

					<v-row>
						<v-col cols='8' offset='4'>
							<v-btn
								class='teal lighten-4 ma-1'
								@click='update'
							>
							更新
							</v-btn>
						</v-col>
					</v-row>
				</v-container>
			</v-form>
		</v-card>
	</div>
</template>

<script>
	import axios from 'axios'

	export default {
		name: 'AcountSetting',
		data: () => ({
			profileData: {},

		}),

		mounted: function () {
			const loginUser = this.$store.state.loginUser
			axios.get('http://192.168.33.12:8000/api/profile/' + loginUser)
			.then(res => {
				this.profileData = res.data
				console.log(res)
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
			update () {
				console.log(this.profileData)
			}
		}
	}
</script>
