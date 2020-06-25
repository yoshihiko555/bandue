<template>
	<div class="acount_card_wrap">
		<v-card
			tile
			outlined
		>
			<v-card-title class='acount_title_wrap'>{{ profileData.username }}</v-card-title>

			<v-form class='acount_form_wrap'>
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
							<v-card-text>Introduction</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-textarea
								v-model='profileData.introduction'
								:value="profileData.introduction"
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

					<!-- 住所 -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Address</v-card-text>
						</v-col>
						<v-col cols='8'>
							<v-text-field
								v-model='profileData.address'
								:counter='70'
								maxlength='70'
								:value="profileData.address"
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
								@click='userUpdate'
							>
							更新
							</v-btn>
							<v-btn
								class='red ma-1 white--text'
								@click='userDelete'
							>
							削除
							</v-btn>
						</v-col>
					</v-row>
				</v-container>
			</v-form>
		</v-card>
	</div>
</template>

<script>
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'AcountSetting',
		data: () => ({
			profileData: {},

		}),

		mounted: function () {
			const loginUser = this.$store.state.loginUser
			this.$axios.get('/api/profile/' + loginUser + '/')
			.then(res => {
				this.profileData = res.data
				console.log(res)
			})
			.catch(e => {
				console.log(e.response)
			})
		},

		methods: {
			userUpdate () {
			  console.log(this.profileData)
				this.$axios({
					method: 'PUT',
					url: '/api/profile/' + this.profileData.id + '/',
					data: this.profileData,
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
			},
			userDelete () {
			  this.$axios({
			    method: 'DELETE',
			    url: '/api/profile/' + this.profileData.id + '/',
			  })
				.then(res => {
					console.log(res)
          this.$store.commit('initState')
				  this.$router.push('/')
				  Com.reload(this.$router)
				})
				.catch(e => {
					console.log(e)
				})
			}
		}
	}
</script>

<style lang='scss'>
  .acount_card_wrap {
      height: 750px;
    >div {
      height: 100%;

      .acount_title_wrap {
        height: 10%;
      }

      .acount_form_wrap {
        height: 90%;
        overflow: auto;

        &::-webkit-scrollbar {
          width:7px;
        }

        &::-webkit-scrollbar-thumb {
          background-color: #cacaca;
          border-radius: 5px;
        }

        &::-webkit-scrollbar-track {
          background: rgba(100,100,100, 0);
        }
      }
    }
  }
</style>
