<template>
	<div>
		<div v-for='(tweet, index) in tweetList' :key='`tweet.author-${index}`'>
			<v-card
				flat
				class='tweet_wrap'
			>
				<v-card-title>
					<router-link @click.native='reload()' :to='{ name : "Profile", params : { username: tweet.author}}' class='tweet_author'>{{ tweet.author }}</router-link>
					<span class='ml-8' style='font-size:50%;'>{{ tweet.updated_at }}</span>

					<v-spacer></v-spacer>

					<!-- Tweet編集ボタン -->
					<v-menu bottom left>
						<template v-slot:activator='{ on }'>
							<v-btn
								dark
								icon
								v-on='on'
								color='grey'
								v-show='tweetListFlg != 4'
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
							<v-icon v-if='tweet.isLiked === 0'
							 	class='mr-1 liked'
								color='red lighten-3'
								@click='liked(tweet.id, tweet.isLiked, index)'
								ref='tweet_isLiked'
							>mdi-heart</v-icon>
							<v-icon v-else
							 	class='mr-1 liked'
								color='red lighten-1'
								@click='liked(tweet.id, tweet.isLiked, index)'
								ref='tweet_isLiked'
							>mdi-heart</v-icon>
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

	</div>
</template>

<script>
	import axios from 'axios'
	import { Common } from '@/static/js/common'
	import TweetEdit from '@/components/common/TweetEdit'
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
			TweetEdit
		},
		data: () => ({
			tweetList: {},
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
			selectTweet: {},
		}),
		created () {
			this.$eventHub.$on('create-tweet', this.tweetUpdate)
		},
		mounted: function () {
			console.log('ツイートリストフラグ:', this.tweetListFlg)
			console.log('ユーザーネーム:', this.username)
			console.log('ログインユーザー:', this.$session.get('username'))
			const loginUser = this.$session.get('username')
			const targetUser = (this.username !== undefined) ? this.username : loginUser
			axios.get('http://192.168.33.12:8000/api/tweet/', {
				params: {
					tweetListFlg: this.tweetListFlg,
					targetUser: targetUser,
					loginUser: loginUser
				}
			})
			.then(res => {
				for (var i in res.data) {
					var updatedAt = res.data[i].updated_at.substr(0, 10)
					res.data[i].updated_at = updatedAt
				}
				this.tweetList = res.data
				console.log(this.tweetList)
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

				var JWTToken = this.$session.get('token')
				axios.defaults.xsrfCookieName = 'csrftoken'
				axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
				const targetUrl = (isLiked === 0) ? 'liked/' : 'unLiked/'
				axios({
					method: 'POST',
					url: 'http://192.168.33.12:8000/api/tweet/' + targetUrl,
					data: {
						target_tweet_id : tweetId,
						login_user : this.$session.get('username')
					},
					headers: {
						Authorization: `JWT ${JWTToken}`,
						'Content-Type': 'application/json'
					}
				})
				.then(res => {
					console.log(res)
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
			},

			// TODO 削除前に確認モーダル表示
			showDeleteDialog (tweet) {
				var JWTToken = this.$session.get('token')
				axios.defaults.xsrfCookieName = 'csrftoken'
				axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
				axios({
					method: 'DELETE',
					url: 'http://192.168.33.12:8000/api/tweet/' + tweet.id + '/',
					data: {
						content : tweet.content
					},
					headers: {
						Authorization: `JWT ${JWTToken}`,
						'Content-Type': 'application/json'
					}
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
			},
		}
	}
</script>

<style>
	.tweet_author {
		cursor: pointer;
		color: #333 !important;
		text-decoration: none;
	}
	.liked {
		cursor: pointer;
	}
</style>
