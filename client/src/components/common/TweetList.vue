<template>
	<div>
		<div v-for='(tweet, index) in tweetList' :key='`tweet.author-${index}`'>
			<v-card
				flat
				class='tweet_wrap'
				@click.self.native='showTweetDetail(tweet)'
			>
				<v-card-title>
					<v-avatar>
						<v-img v-if='tweet.userIcon !== "/media/"' :src='tweet.userIcon'></v-img>
						<v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
					</v-avatar>
					<router-link
						@click.native='reload()'
						:to='{ name : "Profile", params : { username: tweet.author}}'
						class='tweet_author z10'
					>{{ tweet.author }}</router-link>
					<span class='ml-8' style='font-size:50%;'>{{ tweet.updated_at }}</span>
					<span v-if='tweet.isRetweeted'>
						<v-icon
							class='mr-1 retweet'
							color='green lighten-1'
						>mdi-repeat</v-icon>
						リツイート済み
					</span>
					<span
						v-else-if='tweet.followees_in_retweet_users.length != 0'
						class='followees_in_retweet_users'
					>
						<v-icon
							class='mr-1 retweet'
							color='green lighten-1'
						>mdi-repeat</v-icon>
						{{ tweet.followees_in_retweet_users[0].username }} さんがリツイート
					</span>
					<span
						v-else-if='tweet.followees_in_retweet_users.length == 0
						 && tweet.followees_in_liked.length != 0'
						class='followees_in_liked'
					>
						<v-icon v-if='!tweet.isLiked'
								color='red lighten-3'
								ref='tweet_isLiked'
						>mdi-heart</v-icon>
						{{ tweet.followees_in_liked[0].username }} さんがいいねしました
					</span>

					<v-spacer></v-spacer>

					<span class='created_time'>
						{{ tweet.created_time }}
					</span>

					<!-- Tweet編集ボタン -->
					<div v-if='tweetListFlg === 4 ||
							tweetListFlg != 4 && tweet.isMyself'>
						<v-menu bottom left class='z10'>
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

							<v-list
								v-if='tweet.isMyself'
							>
								<v-list-item
									v-for='(item, i) in kebabMenu'
									:key='i'
									@click='tweetEditMethods(i, tweet)'
								>
									<v-list-item-title :class='item.color'>{{ item.title }}</v-list-item-title>
								</v-list-item>
							</v-list>

							<v-list
								v-else
							>
								<v-list-item
									v-if='tweet.isFollow'
									@click='tweetUserUnFollow(tweet)'
								>
									<v-list-item-title>UnFollow</v-list-item-title>
								</v-list-item>
								<v-list-item
									v-else
									@click='tweetUserFollow(tweet)'
								>
									<v-list-item-title>Follow</v-list-item-title>
								</v-list-item>
								<v-list-item
									v-for='(item, i) in tweetUserMenu'
									:key='i'
									@click='tweetUserMethod(i, tweet)'
								>
									<v-list-item-title :class='item.color'>{{ item.title }}</v-list-item-title>
								</v-list-item>
							</v-list>
						</v-menu>
					</div>
				</v-card-title>
				<!-- 内容 -->
				<v-card-text>
					{{ tweet.content }}
				</v-card-text>

				<div>
					<img :src='tweet.images' width="100">
				</div>
				<v-container>
					<v-row>
						<div
							v-if='tweet.reply_count != 0
								|| tweet.isReply === true'
							class='reply_wrap'
						>
							<div
								v-if='tweet.isRetweet'
							>
								<v-btn
									text
									color='primary'
									class='reply_text z10'
									@click='showReplyDetail(tweet)'
								>このスレッドを表示</v-btn>
							</div>
							<div
								v-else
							>
								<v-avatar
									size='34'
									class='reply_img'
								>
									<v-img src='@/static/img/default_icon.jpeg'></v-img>
								</v-avatar>
								<v-btn
									text
									color='primary'
									class='reply_text z10'
									@click='showReplyDetail(tweet)'
								>このスレッドを表示</v-btn>
							</div>
						</div>
						<v-spacer></v-spacer>
						<v-card-actions>
							<v-list-item>
								<v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
									<v-list-item-title>{{ tag.title }}</v-list-item-title>
								</v-list-item-content>
								<v-row
									align='center'
									justify='end'
								>
									<reply
										:tweet=tweet
									></reply>
									<retweet
										:tweet=tweet
									></retweet>
									<like
										:tweet=tweet
									></like>
								</v-row>
							</v-list-item>
						</v-card-actions>
					</v-row>
				</v-container>
			</v-card>
		</div>

		<div v-if='nextPage != null && tweetLoading || initLoading === true'>
			<Loading></Loading>
		</div>

		<!-- モーダル設定 -->
		<TweetEdit
			@closeModal='closeModal'
			:tweetEditDialog='tweetEditDialog'
			:tweet='selectTweet'
		></TweetEdit>

		<TweetDetail
			@closeModal='closeModal'
			:tweetDetailDialog='tweetDetailDialog'
			:tweet='selectTweet'
		></TweetDetail>

		<ReplyDetail
			@closeModal='closeModal'
			:replyDetailDialog='replyDetailDialog'
			:tweet='selectTweet'
		></ReplyDetail>

	</div>
</template>

<script>
	import TweetEdit from '@/components/common/TweetEdit'
	import TweetDetail from '@/components/common/TweetDetail'
	import Reply from '@/components/common/Reply'
	import Retweet from '@/components/common/Retweet'
	import Like from '@/components/common/Like'
	import Loading from '@/components/common/Loading'
	import ReplyDetail from '@/components/common/ReplyDetail'
  import { Common } from '@/static/js/common'
  import { mapState } from 'vuex'

	const Com = new Common()

	export default {
		name: 'TweetList',
		props: {
			tweetListFlg: {
				type: Number,
				required: true
			},
			username: {
				type: String,
				required: false
			}
		},
		components: {
			TweetEdit,
			TweetDetail,
			Reply,
			Retweet,
			Like,
			Loading,
			ReplyDetail,
		},
		data: () => ({
			tweetList: [],
			kebabMenu: [
				{
					title: 'Edit',
					color: '',
				},
				{
					title: 'Delete',
					color: 'red--text',
				}
			],
			tweetUserMenu: [
				{
					title: 'Mute',
					color: '',
				},
				{
					title: 'Block',
					color: 'red--text'
				},
			],
			tweetEditDialog: false,
			tweetDeleteDialog: false,
			tweetDetailDialog: false,
			selectTweet: {},
			tweet: {},
			nextPage: null,
			scrollY: 0,
			scrollMax: 0,
			initLoading: true,
      tweetLoading: true,
			replyDetailDialog: false,
		}),
		created () {
			this.$eventHub.$on('create-tweet', this.tweetUpdate)
      window.addEventListener('scroll', this.handleScroll)
    },
		mounted: function () {
			console.log('ツイートリストフラグ:', this.tweetListFlg)
			console.log('ユーザーネーム:', this.username)
			console.log('ログインユーザー:', this.$store.state.loginUser)
			const loginUser = this.$store.state.loginUser
			const targetUser = (this.username !== undefined) ? this.username : loginUser
			this.$axios.get('api/tweet/', {
				params: {
					tweetListFlg: this.tweetListFlg,
					targetUser: targetUser,
				}
			})
			.then(res => {
				for (var i in res.data.results) {
					var updatedAt = res.data.results[i].updated_at.substr(0, 10)
					res.data.results[i].updated_at = updatedAt
				}
				this.tweetList = res.data.results
				console.log('ツイート一覧',this.tweetList)
				this.nextPage = res.data.next
				this.tweetLoading = false
				if (this.initLoading === true) this.initLoading = false
			})
			.catch(e => {
				console.log(e)
				this.initLoading = false
			})
		},
		methods: {
			tweetUpdate (res) {
				console.log('tweet更新')
				console.log(res.data)
				var updatedAt = res.data.updated_at.substr(0, 10)
				res.data.updated_at = updatedAt
				this.tweetList.unshift(res.data)
				console.log(this.tweetList)
			},
			reload () {
				Com.reload(this.$router)
			},
			tweetEditMethods (i, tweet) {
				const methodsList = [
					this.showTweetEdit,
					this.showDeleteDialog,
				]

				if (methodsList[i] !== '') {
					methodsList[i](tweet)
				}
			},
			showTweetEdit (tweet) {
				this.tweetEditDialog = true
				this.selectTweet = tweet
			},

			closeModal () {
				this.tweetEditDialog = false
				this.tweetDetailDialog = false
				this.replyDetailDialog = false
			},
			// TODO 削除前に確認モーダル表示
			showDeleteDialog (tweet) {
				this.$axios({
					method: 'DELETE',
					url: '/api/tweet/' + tweet.pk + '/',
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data
				})
				.catch(e => {
					console.log(e)
				})
			},
			showTweetDetail (tweet) {
				this.tweetDetailDialog = true
				this.selectTweet = tweet
			},
			next () {
				if (this.nextPage !== null) {
					console.log('ツイートリストフラグ:', this.tweetListFlg)
					console.log('ユーザーネーム:', this.username)
					console.log('ログインユーザー:', this.$store.state.loginUser)
					const loginUser = this.$store.state.loginUser
					const targetUser = (this.username !== undefined) ? this.username : loginUser
					this.$axios.get(this.nextPage)
					.then(res => {
						console.log(res.data.next)

						for (var i in res.data.results) {
							var updatedAt = res.data.results[i].updated_at.substr(0, 10)
							res.data.results[i].updated_at = updatedAt
							this.tweetList.push(res.data.results[i])
						}
						console.log('ツイート一覧',this.tweetList)

						this.nextPage = res.data.next
						this.scrollMax = document.body.scrollHeight - window.innerHeight
						this.tweetLoading = false
					})
					.catch(e => {
						console.log(e)
					})
				}
			},
			handleScroll () {
				this.scrollY = window.scrollY
				this.scrollMax = document.body.scrollHeight - window.innerHeight

				if (this.scrollY / this.scrollMax >= 0.99 && !this.tweetLoading) {
					if (this.nextPage != null) {
						this.tweetLoading = true
						this.next()
					}
				}
			},
			showReplyDetail (tweet) {
				console.log('showReplyDetail')
				this.replyDetailDialog = true
				this.selectTweet = tweet
			},
			tweetUserFollow (tweet) {
				console.log('tweetUserFollow')
				this.$axios({
					method: 'POST',
					url: '/api/users/follow/',
					data: {
						target_user : tweet.author,
						isTweetList : true,
					},
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data.results
				})
				.catch(e => {
					console.log(e)
				})
			},
			tweetUserUnFollow (tweet) {
				this.$axios({
					method: 'POST',
					url: '/api/users/unfollow/',
					data: {
						target_user : tweet.author,
						isTweetList : true,
					},
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data.results
				})
				.catch(e => {
					console.log(e)
				})
			},
			mute (tweet) {
				this.$axios({
					method: 'POST',
					url: '/api/users/mute/',
					data: {
						target_user : tweet.author,
					},
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data.results
				})
				.catch(e => {
					console.log(e)
				})
			},
			block (tweet) {
				this.$axios({
					method: 'POST',
					url: '/api/users/block/',
					data: {
						target_user : tweet.author,
					},
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data.results
				})
				.catch(e => {
					console.log(e)
				})
			},
			tweetUserMethod (i, tweet) {
				let tweetUserMethodList = [
					this.mute,
					this.block,
				]
				tweetUserMethodList[i](tweet)
			},
		}
	}
</script>

<style lang='scss'>
	.tweet_wrap {
		border-radius: 0 !important;
		border-bottom: solid 1px #ccc !important;
		cursor: pointer;
		&::after {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			height: 100%;
			z-index: 0;
		}

		.reply_wrap {
			padding-left: 20px;
			position: relative;
			top: 20px;
		}

		.tweet_author {
			color: $default-color !important;
			text-decoration: none;
			position: relative;

			&::after {
				position: absolute;
				bottom: 0;
				left: 0;
				content: '';
				width: 100%;
				height: 2px;
				background: #333;
				transform: scale(0, 1);
				transform-origin: center top;
				transition: transform .3s;
			}

			&:hover {
				&::after {
					transform: scale(1, 1);
				}
			}
		}

		.created_time {
			font-size: 14px;
		}
	}

</style>
