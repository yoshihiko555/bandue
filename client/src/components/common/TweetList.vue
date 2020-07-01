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
						<v-img :src='tweet.userIcon'></v-img>
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

				<div>
					<img :src='tweet.images' width="100">
				</div>
				<v-card-actions>
					<v-list-item>
						<v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
							<v-list-item-title>{{ tag.title }}</v-list-item-title>
						</v-list-item-content>

						<v-row
							align='center'
							justify='end'
						>
							<retweet :tweet=tweet :index=index></retweet>
							<like :tweet=tweet :index=index></like>
						</v-row>
					</v-list-item>
				</v-card-actions>
			</v-card>
		</div>

		<div v-if='nextPage != null && tweetLoading'>
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

	</div>
</template>

<script>
	import TweetEdit from '@/components/common/TweetEdit'
	import TweetDetail from '@/components/common/TweetDetail'
	import Retweet from '@/components/common/Retweet'
	import Like from '@/components/common/Like'
	import Loading from '@/components/common/Loading'
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
			Retweet,
			Like,
			Loading,
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
			tweet: {},
			nextPage: null,
			scrollY: 0,
			scrollMax: 0,
			tweetLoading: true,
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
				console.log(res.data.next)
				for (var i in res.data.results) {
					var updatedAt = res.data.results[i].updated_at.substr(0, 10)
					res.data.results[i].updated_at = updatedAt
				}
				this.tweetList = res.data.results
				console.log('ツイート一覧',this.tweetList)
				this.nextPage = res.data.next
				this.tweetLoading = false
			})
			.catch(e => {
				console.log(e)
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
