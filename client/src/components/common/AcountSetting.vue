<template>
	<div class="acount_card_wrap">
		<v-card
			tile
			outlined
		>
			<v-card-title class='acount_title_wrap'>{{ profileData.username }}</v-card-title>

			<v-form class='acount_form_wrap'>
				<v-container>
					<!-- ヘッダー -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Header</v-card-text>
						</v-col>
						<v-col cols='8'>
							<div class="acount_header_wrap">
								<div class="acount_header_image">
									<v-img v-show='!showHeader' src='@/static/img/default_header.jpg' alt="header"></v-img>
									<v-img v-show='showHeader' :src="previewHeader" alt="header"></v-img>
								</div>
								<v-file-input
									hide-input
									class='acount_header_input_btn ma-0'
									ref='header'
									accept="image/*"
									prepend-icon="mdi-camera-enhance-outline"
									@change='inputHeader'
								>
								</v-file-input>
								<v-btn
									icon
									class='acount_delete_btn ma-1'
									@click='deleteHeader'
								>
									<v-icon color='white'>mdi-close</v-icon>
								</v-btn>
							</div>
						</v-col>
					</v-row>

					<!-- アイコン -->
					<v-row>
						<v-col cols='4'>
							<v-card-text>Icon</v-card-text>
						</v-col>
						<v-col cols='8'>
							<div class="acount_icon_wrap">
								<v-avatar class="acount_icon_image">
									<v-img v-show='!showIcon' src='@/static/img/default_icon.jpeg' alt="icon"></v-img>
									<v-img v-show='showIcon' :src="previewIcon" alt="icon"></v-img>
								</v-avatar>
								<v-file-input
									hide-input
									class='acount_icon_input_btn ma-0'
									ref='icon'
									accept="image/*"
									prepend-icon="mdi-camera-enhance-outline"
									@change='inputIcon'
								>
								</v-file-input>
							</div>
						</v-col>
					</v-row>

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
	const reader = new FileReader()

	export default {
		name: 'AcountSetting',
		data: () => ({
			profileData: {},
			header: null,
			previewHeader: '',
			showHeader: false,
			icon: null,
			previewIcon: '',
			showIcon: false,
		}),

		mounted: function () {
			const loginUser = this.$store.state.loginUser
			this.$axios.get('/api/profile/' + loginUser + '/')
			.then(res => {
				this.profileData = res.data
				if (this.profileData.header !== null) {
					this.previewHeader = this.profileData.header
					this.showHeader = true
				}
				if (this.profileData.icon !== null) {
					this.previewIcon = this.profileData.icon
					this.showIcon = true
				}
				console.log(res)
			})
			.catch(e => {
				console.log(e.response)
			})
		},

		methods: {
			userUpdate () {
				var sendData = new FormData()
				if (this.header !== null) sendData.append('header', this.header)
				if (this.icon !== null) sendData.append('icon', this.icon)
				sendData.append('username', this.profileData.username)
				sendData.append('email', this.profileData.email)
				sendData.append('introduction', this.profileData.introduction)
				sendData.append('address', this.profileData.address)
				sendData.append('password', this.profileData.password)

				this.$axios({
					method: 'PUT',
					url: '/api/profile/' + this.profileData.id + '/',
					data: sendData,
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
					// Com.reload(this.$router)
				})
				.catch(e => {
					console.log(e)
				})
			},
			inputHeader (e) {
				reader.readAsDataURL(e)
				reader.onload = e => {
					this.previewHeader = e.target.result
				}
				this.header = e
				this.showHeader = true
			},
			deleteHeader () {
				this.header = null
				this.previewHeader = ''
				this.$refs.header.lazyValue = ''
				this.showHeader = false
			},
			inputIcon (e) {
				reader.readAsDataURL(e)
				reader.onload = e => {
					this.previewIcon = e.target.result
				}
				this.icon = e
				this.showIcon = true
			},
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

		.acount_header_wrap {
			position: relative;
			.acount_header_image {
				width: 100%;

				&::after {
					content: '';
					width: 100%;
					height: 100%;
					position: absolute;
					top: 0%;
					left: 0%;
					background-color: #636363b3;
				}
			}

			.acount_header_input_btn {
				position: absolute;
				top: 50%;
				left: 40%;
				-ms-transform: translate(-50%,-50%);
				-webkit-transform: translate(-50%,-50%);
				transform: translate(-50%,-50%);

				button {
					font-size: 30px;
					color: #d4d4d4;
				}
			}

			.acount_delete_btn {
				position: absolute;
				top: 50%;
				right: 25%;
				-ms-transform: translate(-50%,-50%);
				-webkit-transform: translate(-50%,-50%);
				transform: translate(-50%,-50%);

				i {
					font-size: 30px;
					color: #d4d4d4 !important;
				}
			}

		}

		.acount_icon_wrap {
			position: relative;

			.acount_icon_image {
				width: 70px !important;
				height: 70px !important;
			}

			.acount_icon_input_btn {
				position: absolute;
				top: 50%;
				left: 30%;
				-ms-transform: translate(-50%,-50%);
				-webkit-transform: translate(-50%,-50%);
				transform: translate(-50%,-50%);
			}
		}

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
