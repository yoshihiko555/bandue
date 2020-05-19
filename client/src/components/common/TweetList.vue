<template>
	<div>
		<div v-for='tweet in tweetList' :key='tweet.author'>
			<v-card
				flat
				class='tweet_wrap'
			>
				<v-card-title>
					<router-link @click.native="reload()" :to="{ name : 'Profile', params : { username: tweet.author}}" class="tweet_author">{{ tweet.author }}</router-link>
					<span class='ml-8' style="font-size:50%;">{{ tweet.updated_at }}</span>
				</v-card-title>

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
							<v-icon class='mr-1' color='red lighten-1'>mdi-heart</v-icon>
							<span class='mr-2'>{{ tweet.liked }}</span>
						</v-row>
					</v-list-item>
				</v-card-actions>
			</v-card>
		</div>
	</div>
</template>

<script>
	import axios from 'axios'
	import { Common } from '@/static/js/common'
	const Com = new Common()
	export default {
		name: 'TweetList',
		props: {
			tweetListFlg: {
				type: Number,
				required: true
			}
		},
		data: () => ({
			tweetList: {},
		}),
		created () {
			this.$eventHub.$on('create-tweet', this.tweetUpdate)
		},
		mounted: function () {
			console.log(this.$el)
			console.log('ツイートリストフラグ:', this.tweetListFlg)
			axios.get('http://192.168.33.12:8000/api/tweet/', {
				params: {tweetListFlg: this.tweetListFlg}
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
				this.tweetList = res.data
			},
			showProfile (username) {
				this.reload()
			},
			reload() {
				Com.reload(this.$router)
			}
		}
	}
</script>

<style>
	.tweet_author {
		cursor: pointer;
		color: #333 !important;
		text-decoration: none;
	}
</style>
