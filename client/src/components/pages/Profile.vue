<template>
	<v-app>
		<Header/>
		<div id='profile_wrap' class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6'>
						<v-card
							outlined
                            :dark='this.$store.state.settings.isDark'
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

								<v-card-text class="pt-6 text-h5">
									{{ profileData.username }}
									<span v-if='!isMe'>
										<follow :username='username'></follow>
									</span>
								</v-card-text>
								<v-card-text>
									{{ profileData.introduction }}
								</v-card-text>
								<v-card-text class="text-caption">
									{{ profileData.created_at }}
								</v-card-text>
							</div>

							<div v-if='view == 0'>
								<v-card-text>
									<v-btn
										text
										@click='changeView(1)'
									>
										{{ profileData.followees_count }} Following
									</v-btn>

									<v-btn
										text
										@click='changeView(2)'
									>
										{{ profileData.followers_count }} Followers
									</v-btn>
								</v-card-text>

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
			this.$axios.get('/api/profile/' + this.username)
			.then(res => {
				res.data.created_at = res.data.created_at.substr(0, 10)
				this.profileData = res.data
				this.icon = this.profileData.icon
				this.header = this.profileData.header
				console.log(res)
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
			changeView (cnt) {
				console.log(cnt)
				this.followeesTabModel = cnt
				this.view = cnt
			}
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
