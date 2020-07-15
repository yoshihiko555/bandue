<template>
	<v-app>
		<Header/>
		<div class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6' class="px-0">
						<div v-if='infoList.length != 0 && initLoading === false'>
							<div v-for='(info, index) in infoList' :key='`infoList-${index}`' class='info_area'>
								<v-card
									flat
									class='info_wrap'
									ref='info_ref'
									@click='InfoDetail(info, index)'
								>
									<v-card-title
										class='info_title'
									>
										<div v-if='info.event === "Liked"'>
											<v-icon
												color='red lighten-1'
											>mdi-heart</v-icon>
										</div>
										<div v-else-if='info.event === "Retweet"'>
											<v-icon
												color='grey lighten-1'
											>mdi-repeat</v-icon>
										</div>
										<v-avatar
										 	v-else
											class='infomation_icon'
										>
											<v-img v-if='info.send_user.icon === null' src='@/static/img/default_icon.jpeg'></v-img>
											<v-img v-else :src=icon></v-img>
										</v-avatar>
									</v-card-title>

									<v-card-text
										class='info_text'
									>
										{{ info.infomation }}
									</v-card-text>
								</v-card>
							</div>
						</div>
						<div v-else>

							<div v-if='initLoading === true'>
								<Loading></Loading>
							</div>

							<div v-else>
								<v-card
									flat
								>お知らせはありません。
								</v-card>
							</div>

						</div>
					</v-col>
					<v-col cols='3'>
						<Search/>
					</v-col>
				</v-row>
			</v-container>
		</div>
		<Footer/>

		<TweetDetail
			@closeModal='closeModal'
			:tweetDetailDialog='tweetDetailDialog'
			:tweet='selectTweet'
		></TweetDetail>

	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Search from '@/components/common/Search'
	import TweetDetail from '@/components/common/TweetDetail'
	import Loading from '@/components/common/Loading'
	import { Common } from '@/static/js/common'
	import { Const } from '@/static/js/const'

	const Com = new Common()
	const Con = new Const()

	export default {
		name: 'Message',
		components: {
			Header,
			Footer,
			Sidebar,
			Search,
			TweetDetail,
			Loading,
		},
		data: () => ({
			infoList: [],
			readedInfoPk: [],
			tweetDetailDialog: false,
			selectTweet: {},
			initLoading: true,
		}),
		created () {

		},
		mounted: function () {

			this.$axios.get('/api/info/')
			.then(res => {
				this.infoList = res.data.results
				this.initLoading = false
			})
			.catch(e => {
				console.log(e)
				this.initLoading = false
			})

			this.readInfo()

		},
		methods: {
			readInfo () {
				this.$axios.get('/api/info/readInfo/')
				.then(res => {
					this.$eventHub.$emit('cntZeroInfo', 'Info')
				})
				.catch(e => {
					console.log(e)
				})
			},

			InfoDetail (info, index) {
				var event = info.event
				if (Con.PROFILE_EVENT.includes(event)) {
					var username = info.send_user.username
					this.$router.push('/profile/' + username)
					Com.reload(this.$router)
				} else if (Con.TWEET_EVENT.includes(event)) {
					this.showTweetDetail(info.target_tweet_info)
				} else {
					console.log('それ以外。メッセージとか？')
				}
			},

			closeModal () {
				this.tweetDetailDialog = false
			},

			showTweetDetail (tweet) {
				this.tweetDetailDialog = true
				this.selectTweet = tweet
			}
		}
	}
</script>

<style lang='scss'>
	.info_wrap {
		border-radius: 0 !important;
		border-bottom: solid 0.5px #ccc !important;
		cursor: pointer;
	}

</style>
