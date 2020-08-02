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

				<reply :tweet=tweet></reply>
				<retweet :tweet=tweet></retweet>
				<like :tweet=tweet></like>

				<v-spacer></v-spacer>
				<v-btn color='teal lighten-4' @click='closeModal'>Close</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
	import { Common } from '@/static/js/common'
	import Reply from '@/components/common/Reply'
	import Retweet from '@/components/common/Retweet'
	import Like from '@/components/common/Like'

	const Com = new Common()

	export default {
		name: 'TweetDetail',
		props: ['tweet', 'tweetDetailDialog'],
		data: () => ({
		}),
		components: {
			Reply,
			Retweet,
			Like,
		},
		methods: {
			closeModal () {
				this.$emit('closeModal')
			},
			reload () {
				// Com.reload(this.$router)
			},
		}
	}
</script>

<style lang='scss'>
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
</style>
