<template>
    <div>
        <v-btn
            icon
            @click='liked(tweet)'
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
    </div>
</template>

<script>
    export default {
        props: {
            tweet: {
                type: Object,
                required: true
            }
        },
        data: () => ({

        }),
        created () {

        },
        methods: {
          liked (tweet) {
    				if (tweet.isLiked) {
    					tweet.liked_count--
    				} else {
    					tweet.liked_count++
    				}
            tweet.isLiked = !tweet.isLiked

    				const targetUrl = 'liked'
    				this.$axios({
    					method: 'POST',
    					url: '/api/tweet/' + targetUrl + '/',
    					data: {
    						target_tweet_pk : tweet.pk
    					},
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
    .retweet {
        cursor: pointer;
    }
</style>
