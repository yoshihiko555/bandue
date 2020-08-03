<template>
    <div>
        <v-btn
            icon
            @click='retweetConfirm(tweet)'
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

        <BlockDialog
          @closeModal='closeModal'
          :username='tweet.author'
          :isBlockedDialog='isBlockedDialog'
          :event='"retweet"'
        ></BlockDialog>
    </div>
</template>

<script>
    import RetweetConfirm from '@/components/common/RetweetConfirm'
    import BlockDialog from '@/components/common/BlockDialog'

    export default {
        props: {
            tweet: {
                type: Object,
                required: true
            }
        },

        components: {
            RetweetConfirm,
            BlockDialog,
        },

        data: () => ({
            retweetConfirmDialog: false,
            selectTweet: {},
            isBlocked: false,
            isBlockedDialog: false,
        }),

        created () {
            this.isBlocked = this.tweet.isBlocked
        },

        methods: {
            retweetConfirm (tweet) {
                if (this.isBlocked) {
                    this.isBlockedDialog = true
                    return
                }

                this.retweetConfirmDialog = true
                this.selectTweet = tweet
            },

            closeModal () {
                this.retweetConfirmDialog = false
                this.isBlockedDialog = false
            },

            // リツイートするメソッド
            retweet () {
                (this.tweet.isRetweeted) ? this.tweet.retweet_count-- : this.tweet.retweet_count++

                this.tweet.isRetweeted = !this.tweet.isRetweeted
                this.$axios({
                    method: 'POST',
                    url: '/api/tweet/retweet/',
                    data: {
                        target_tweet_pk : this.tweet.pk
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
