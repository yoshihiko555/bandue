<template>
	<div>
		<div v-for='(tweet, index) in tweetList' :key='`tweet.author-${index}`'>
			<v-card
				flat
				class='tweet_wrap'
				@click.self.native='showTweetDetail(tweet)'
			>
				<v-card-title>
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

					<v-spacer></v-spacer>

					<!-- Tweet編集ボタン -->
					<v-menu bottom left class='z10'>
						<template v-slot:activator='{ on }'>
							<v-btn
								dark
								icon
								v-on='on'
								color='grey'
								v-show='tweetListFlg != 4'
								class='z10'
							>
								<v-icon>mdi-dots-vertical</v-icon>
							</v-btn>
						</template>

						<v-list>
							<v-list-item
								v-for='(item, i) in kebabMenu'
								:key='i'
								@click='tweetEditMethods(i, tweet)'
							>
								<v-list-item-title :class='item.color'>{{ item.title }}</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</v-card-title>

				<!-- 内容 -->
				<v-card-text>
					{{ tweet.content }}
				</v-card-text>

				<v-card-actions>
					<v-list-item>
						<v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
							<v-list-item-title>{{ tag.title }}</v-list-item-title>
						</v-list-item-content>

						<v-row
							align='center'
							justify='end'
						>
							<v-btn
								icon
								@click='retweet(tweet.id, tweet.isRetweeted, index)'
								class='z10'
							>
								<v-icon v-if='!tweet.isRetweeted'
									color='black lighten-5'
									ref='tweet_retweet'
								>mdi-repeat</v-icon>
								<v-icon v-else
									color='green lighten-1'
									ref='tweet_retweet'
								>mdi-repeat</v-icon>
							</v-btn>
							<span class='mr-2' ref='tweet_retweet_count'>{{ tweet.retweet_count }}</span>

							<v-btn
								icon
								@click='liked(tweet.id, tweet.isLiked, index)'
								class='z10'
							>
								<v-icon v-if='!tweet.isLiked'
									color='red lighten-3'
									ref='tweet_isLiked'
								>mdi-heart</v-icon>
								<v-icon v-else
									color='red lighten-1'
									ref='tweet_isLiked'
								>mdi-heart</v-icon>
							</v-btn>
							<span class='mr-2' ref='tweet_isLikedCount'>{{ tweet.liked_count }}</span>
						</v-row>
					</v-list-item>
				</v-card-actions>
			</v-card>
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

	</div>
</template>

<script>
	import TweetEdit from '@/components/common/TweetEdit'
	import TweetDetail from '@/components/common/TweetDetail'
	import { Common } from '@/static/js/common'

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
			tweetEditDialog: false,
			tweetDeleteDialog: false,
			tweetDetailDialog: false,
			selectTweet: {},
		}),
		created () {
			this.$eventHub.$on('create-tweet', this.tweetUpdate)
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
				for (var i in res.data) {
					var updatedAt = res.data[i].updated_at.substr(0, 10)
					res.data[i].updated_at = updatedAt
				}
				this.tweetList = res.data
				console.log('ツイート一覧',this.tweetList)
			})
			.catch(e => {
				console.log(e)
			})
		},
		methods: {
			tweetUpdate (res) {
				console.log('tweet更新')
				for (var i in res.data) {
					var updatedAt = res.data[i].updated_at.substr(0, 10)
					res.data[i].updated_at = updatedAt
				}
				this.tweetList = res.data
				console.log(this.tweetList)
			},
			reload () {
				Com.reload(this.$router)
			},
			liked (tweetId, isLiked, index) {
				let targetValue = parseInt(this.$refs.tweet_isLikedCount[index].textContent)

				for (let i in this.$refs.tweet_isLiked[index].$el.classList) {
					// console.log(this.$refs.tweet_isLiked[index].$el.classList[i])
					let className = this.$refs.tweet_isLiked[index].$el.classList[i]
					if (className === 'text--lighten-1') {
						this.$refs.tweet_isLiked[index].$el.classList.remove(className)
						this.$refs.tweet_isLiked[index].$el.classList.add('text--lighten-3')
						targetValue = targetValue - 1
					} else if (className === 'text--lighten-3') {
						this.$refs.tweet_isLiked[index].$el.classList.remove(className)
						this.$refs.tweet_isLiked[index].$el.classList.add('text--lighten-1')
						targetValue = targetValue + 1
					}
				}

				this.$refs.tweet_isLikedCount[index].textContent = targetValue

				const targetUrl = 'liked'
				this.$axios({
					method: 'POST',
					url: '/api/tweet/' + targetUrl + '/',
					data: {
						target_tweet_id : tweetId
					},
				})
				.then(res => {
					console.log(res)
					console.log(res.data.isLiked)
					// ここでツイートのisLikedを変えてあげる必要あり
					// isLikedはres.data.isLikedで取れる
				})
				.catch(e => {
					console.log(e)
				})
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
			},

			// TODO 削除前に確認モーダル表示
			showDeleteDialog (tweet) {
				this.$axios({
					method: 'DELETE',
					url: '/api/tweet/' + tweet.id + '/',
				})
				.then(res => {
					console.log(res)
					this.tweetList = res.data
				})
				.catch(e => {
					console.log(e)
				})
			},
			retweet (tweetId, isRetweeted, index) {
				console.log('retweet')

				let targetValue = parseInt(this.$refs.tweet_retweet_count[index].textContent)

				for (let i in this.$refs.tweet_retweet[index].$el.classList) {
					console.log(this.$refs.tweet_retweet[index].$el.classList[i])
					let className = this.$refs.tweet_retweet[index].$el.classList[i]
					if (className === 'text--lighten-1') {
						this.$refs.tweet_retweet[index].$el.classList.remove(className)
						this.$refs.tweet_retweet[index].$el.classList.add('text--lighten-3')
						this.$refs.tweet_retweet[index].$el.classList.add('black--text')
						targetValue = targetValue - 1
					} else if (className === 'text--lighten-5') {
						this.$refs.tweet_retweet[index].$el.classList.remove(className)
						this.$refs.tweet_retweet[index].$el.classList.add('text--lighten-1')
						this.$refs.tweet_retweet[index].$el.classList.add('green--text')
						targetValue = targetValue + 1
					}
				}

				this.$refs.tweet_retweet_count[index].textContent = targetValue

                const targetUrl = 'retweet'
                this.$axios({
                    method: 'POST',
                    url: '/api/tweet/' + targetUrl + '/',
                    data: {
                        target_tweet_id : tweetId
                    },
                })
                .then(res => {
                    console.log(res.data)
                })
                .catch(e => {
                    console.log(e)
                })
            },
			showTweetDetail (tweet) {
				this.tweetDetailDialog = true
				this.selectTweet = tweet
			}

		}
	}
</script>

<style lang='scss'>
	.tweet_wrap {
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

		.tweet_author {
			color: #333 !important;
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
	}

</style>
