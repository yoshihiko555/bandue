<template>
	<v-dialog v-model='tweetDetailDialog' persistent max-width='600px'>
		<v-card>
			<v-card-title>
				<router-link
					@click.native='reload()'
					:to='{ name : "Profile", params : { username: tweet.author}}'
					class='tweet_author z10'
				>{{ tweet.author }}</router-link>
			</v-card-title>

			<v-card-text>
				{{ tweet.content }}
			</v-card-text>

			<v-card-actions>
				<v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
					<v-list-item-title>{{ tag.title }}</v-list-item-title>
				</v-list-item-content>
				
				<v-btn icon>
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

				<v-btn icon>
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
				<v-spacer></v-spacer>
				<v-btn color='teal lighten-4' @click='closeModal'>Close</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'TweetDetail',
		props: ['tweet', 'tweetDetailDialog'],
		data: () => ({
		}),
		methods: {
			closeModal () {
				this.$emit('closeModal')
			},
			reload () {
				Com.reload(this.$router)
			},
		}
	}
</script>

<style lang='scss'>
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
</style>
