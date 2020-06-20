<template>
    <div>
        <v-btn
            icon
            @click='retweetConfirm(tweet, index)'
            class='z10'
        >
            <v-icon v-if='!tweet.isRetweeted'
                color='grey lighten-1'
            >mdi-repeat</v-icon>
            <v-icon v-else
                color='green lighten-1'
            >mdi-repeat</v-icon>
        </v-btn>
        <span class='mr-2' ref='tweet_retweet_count'>{{ tweet.retweet_count }}</span>

        <RetweetConfirm
            @closeModal='closeModal'
            @retweet='retweet'
            :retweetConfirmDialog='retweetConfirmDialog'
            :tweet='selectTweet'
        ></RetweetConfirm>
    </div>
</template>

<script>
    import RetweetConfirm from '@/components/common/RetweetConfirm'

    export default {
        props: {
            tweet: {
                type: Object,
                required: true
            },
            index: {
                type: Number,
                required: true
            }
        },
        components: {
            RetweetConfirm,
        },
        data: () => ({
            retweetConfirmDialog: false,
            selectTweet: {},
        }),
        methods: {
            retweetConfirm (tweet, index) {
                this.retweetConfirmDialog = true
                this.selectTweet = tweet
            },
            closeModal () {
                this.retweetConfirmDialog = false
            },
            retweet () {
				console.log('retweet')
                let tweet = this.selectTweet

                if (tweet.isRetweeted) {
                    tweet.retweet_count--
                } else {
                    tweet.retweet_count++
                }
                tweet.isRetweeted = !tweet.isRetweeted

                const targetUrl = 'retweet'
                this.$axios({
                    method: 'POST',
                    url: '/api/tweet/' + targetUrl + '/',
                    data: {
                        target_tweet_id : tweet.id
                    },
                })
                .then(res => {
                    console.log(res.data)
                })
                .catch(e => {
                    console.log(e)
                })
                this.retweetConfirmDialog = false
                this.selectTweet = {}
            },
        }
    }

</script>

<style>
    .retweet {
        cursor: pointer;
    }
</style>
