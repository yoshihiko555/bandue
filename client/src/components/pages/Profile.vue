<template>
	<v-app>
		<Header/>
		<div id='profile_wrap' class="main" v-if='init == false'>
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6'>
						<v-card
							outlined
						>
							<div class="profile_header_wrap">
								<v-img v-if='profileData.header === null' height='200' src='@/static/img/default_header.jpg'></v-img>
								<v-img v-else height='200' :src=header></v-img>
							</div>

							<div class="profile_content_wrap">
								<v-avatar class='profile_icon'>
									<v-img v-if='profileData.icon === null' src='@/static/img/default_icon.jpeg'></v-img>
									<v-img v-else :src=icon></v-img>
								</v-avatar>

								<v-container fluid>
									<v-card-text class="pt-6 text-h5">
										<v-row>
											<v-col
												cols='8'
											>
												{{ profileData.username }}
											<v-icon
												v-if='profileData.isMute'
											>mdi-volume-variant-off</v-icon>
											<v-icon
												v-if='profileData.isBlock'
											>mdi-account-cancel</v-icon>
											</v-col>
										<v-spacer></v-spacer>
										<v-col
											cols='3'
										>
											<span v-if='!isMe && !loading'>
												<follow
												 :username='username'
												 :isBlocked='profileData.isBlocked'
												 :isPrivate='profileData.isPrivate'
												></follow>
											</span>
										</v-col>
									</v-row>
									</v-card-text>
								</v-container>
								<v-card-text>
									{{ profileData.introduction }}
								</v-card-text>
								<v-card-text class="text-caption">
									{{ profileData.created_at }}
								</v-card-text>
							</div>

							<div v-if='view == 0'>
								<v-card-text>
									<v-row>
										<v-col
											cols='3'
										>
											<v-btn
												text
												@click='changeView(1)'
											>
												{{ profileData.followees_count }} Following
											</v-btn>
										</v-col>

										<v-col
											cols='3'
										>
											<v-btn
												text
												@click='changeView(2)'
											>
												{{ profileData.followers_count }} Followers
											</v-btn>
										</v-col>
										<v-spacer></v-spacer>
										<v-col
											cols='1'
										>
											<v-menu v-if='!isMe' bottom left class='z10'>
												<template v-slot:activator='{ on }'>
													<v-btn
														dark
														icon
														v-on='on'
														color='grey'
														class='z10'
													>
														<v-icon>mdi-dots-vertical</v-icon>
													</v-btn>
												</template>

												<v-list>
													<v-list-item
														v-if='profileData.isMute'
														@click='unmute'
													>
														<v-list-item-title>{{ profileData.username }}さんのミュートを解除</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-else
														@click='mute'
													>
														<v-list-item-title>{{ profileData.username }}さんをミュート</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-if='profileData.isBlock'
														@click='unblock'
													>
														<v-list-item-title>{{ profileData.username }}さんのブロックを解除</v-list-item-title>
													</v-list-item>
													<v-list-item
														v-else
														@click='block'
													>
														<v-list-item-title>{{ profileData.username }}さんをブロック</v-list-item-title>
													</v-list-item>
												</v-list>
											</v-menu>

										</v-col>
									</v-row>
								</v-card-text>

								<div v-if='profileData.tweet_limit_level === 0'>
									<v-tabs
										v-model='profileTabModel'
										grow
										class='tweetlist_tab_wrap'
									>
										<v-tab
											v-for='(tab, i) in ProfileTablist'
											:key='i'
											:href='`#tab-${i}`'
										>
											{{ tab }}
										</v-tab>
									</v-tabs>

									<v-tabs-items v-model='profileTabModel'>
										<v-tab-item
											v-for='(tab, i) in ProfileTablist'
											:key='i'
											:value="'tab-' + i"
										>

											<TweetList
												v-if='i != 4'
												:tweet-list-flg=i
												:username='username'
											></TweetList>

											<div v-else>
												BBS
											</div>
										</v-tab-item>
									</v-tabs-items>
								</div>
								<div v-else-if='profileData.tweet_limit_level === 1'>
									<v-card
										class='block_wrap'
									>
										<v-card-title>
											{{ profileData.username }}さんはあなたをブロックしています。
										</v-card-title>
										<v-card-text>
											{{ profileData.username }}さんにブロックされていますが、ツイートを観覧する事は可能です。
										</v-card-text>
											<v-row>
												<v-spacer></v-spacer>
												<v-btn
													text
													align=center
													@click='showTweetList'
												>ツイートを表示しますか？</v-btn>
												<v-spacer></v-spacer>
											</v-row>
										<v-spacer></v-spacer>
									</v-card>
								</div>
								<div v-else-if='profileData.tweet_limit_level === 2'>
									<v-card
										class='private_wrap'
									>
										<v-card-title>
											{{ profileData.username }}さんのツイートは非公開です。
										</v-card-title>
										<v-card-text>
											{{ profileData.username }}さんのツイートを表示するには、フォローしてください。
											<v-spacer></v-spacer>
										</v-card-text>
									</v-card>
								</div>
								<div v-else-if='profileData.tweet_limit_level === 3'>
									<v-card
										class='private_wrap'
									>
										<v-card-title>
											{{ profileData.username }}さんのツイートは非公開です。
										</v-card-title>
										<v-card-text>
											{{ profileData.username }}さんはあなたをブロックしています。
											<v-spacer></v-spacer>
										</v-card-text>
									</v-card>
								</div>

							</div>

							<div v-else>
								<!-- 戻るボタン -->
								<v-btn icon color='indigo' @click='changeView(0)'>
									<v-icon>mdi-arrow-left-thick</v-icon>
								</v-btn>

								<!-- タブSTART -->
								<v-tabs
									v-model='followeesTabModel'
									grow
									class='followeeslist_tab_wrap'
								>
									<v-tab href='#1'>Following {{ profileData.followees_count }}</v-tab>
									<v-tab href='#2'>Follower {{ profileData.followers_count }}</v-tab>
								</v-tabs>

								<v-tabs-items v-model='followeesTabModel'>
									<v-tab-item value="1">
										<!-- フォロー一覧 -->
										<div v-if='profileData.followees_count == 0'>
											フォローがいない
										</div>

										<div v-else v-for='follow in profileData.followees' :key=follow.username>
											<v-card
												flat
												class='followees_wrap'
											>
											<v-card-title>{{ follow.username }}</v-card-title>
											</v-card>
										</div>
									</v-tab-item>

									<v-tab-item value="2">
										<!-- フォロワー一覧 -->
										<div v-if='profileData.followers_count == 0'>
											フォロワーがいない
										</div>
										<div v-else v-for='follower in profileData.followers' :key=follower.username>
											<v-card
												flat
												class='followees_wrap'
											>
												<v-card-title>{{ follower.username }}</v-card-title>
											</v-card>
										</div>
									</v-tab-item>
								</v-tabs-items>
							</div>

						</v-card>
					</v-col>

					<v-col cols='3'>
						<Search/>
					</v-col>
				</v-row>
			</v-container>
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Search from '@/components/common/Search'
	import TweetList from '@/components/common/TweetList'
	import Follow from '@/components/common/Follow'

	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'Profile',
		components: {
			Header,
			Footer,
			Sidebar,
			Search,
			TweetList,
			Follow
		},
		data: () => ({
			profileData: {},
			view: 0,
			followeesTabModel: 1,
			username: '',
			isMe: false,
			profileTabModel: null,
			ProfileTablist: [
				'Tweets',
				'Tweets & replies',
				'Media',
				'Likes',
				'BBS'
			],
			icon: '',
			header: '',
			loading: null,
			init: true,
		}),
		created () {
			const currentPath = this.$route.path
			const pattern = /\/profile\/(.+?)\/.*/
			const result = currentPath.match(pattern)
			this.username = result[1]
			const loginUser = this.$store.state.loginUser
			if (loginUser === this.username) {
				this.isMe = true
			}
		},
		mounted: function () {
			this.loading = true
			this.$axios.get('/api/profile/' + this.username)
			.then(res => {
				res.data.created_at = res.data.created_at.substr(0, 10)
				this.profileData = res.data
				this.icon = this.profileData.icon
				this.header = this.profileData.header
				console.log(res)
				this.loading = false
				this.init = false
			})
			.catch(e => {
				console.log(e)
				this.showErrorPage(e)
			})
		},

		methods: {
			changeView (cnt) {
				console.log(cnt)
				this.followeesTabModel = cnt
				this.view = cnt
			},
			showErrorPage(e) {
				console.log('showErrorPage')
				var response = e.response
				var statusCode = response.status

				if (statusCode === 404) {
					this.$router.push('/404')
					this.reload()
				} else if (statusCode === 403) {
					console.log('認証で拒否された')
				}
			},
			reload() {
				Com.reload(this.$router)
			},
			showTweetList () {
				this.profileData.tweet_limit_level = 0
			},
			mute () {
				this.$axios({
					method: 'POST',
					url: '/api/users/mute/',
					data: {
						target_user : this.profileData.username,
					},
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
				this.profileData.isMute = true
			},
			unmute () {
				this.$axios({
          method: 'POST',
          url: 'api/users/unmute/',
          data: {
            target_user: this.profileData.username,
          }
        })
        .then(res => {
          console.log(res)
        })
        .catch(e => {
          console.log(e)
        })
				this.profileData.isMute = false
			},
			block () {
				this.$axios({
					method: 'POST',
					url: '/api/users/block/',
					data: {
						target_user : this.profileData.username,
					},
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
				this.profileData.isBlock = true
			},
			unblock () {
				this.$axios({
          method: 'POST',
          url: 'api/users/unblock/',
          data: {
            target_user: this.profileData.username
          }
        })
        .then(res => {
          console.log(res)
        })
        .catch(e => {
          console.log(e)
        })
				this.profileData.isBlock = false
			},

		}
	}
</script>

<style lang='scss'>
	#profile_wrap {
		.profile_content_wrap {
			position: relative;

			.profile_icon {
				position: absolute;
				top: -20%;
				left: 5%;
			}
		}

		.tweetlist_tab_wrap {
			border-bottom: solid 1px #ccc !important;
		}

		.followeeslist_tab_wrap {
			border-bottom: solid 1px #ccc !important;
		}
	}
</style>
