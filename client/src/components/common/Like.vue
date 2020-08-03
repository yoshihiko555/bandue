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

        <BlockDialog
          @closeModal='closeModal'
          :username='tweet.author'
          :isBlockedDialog='isBlockedDialog'
          :event='"like"'
        ></BlockDialog>
    </div>
</template>

<script>
    import BlockDialog from '@/components/common/BlockDialog'

    export default {
        props: {
            tweet: {
                type: Object,
                required: true
            }
        },

        data: () => ({
            isBlocked: false,
            isBlockedDialog: false,
        }),

        components: {
            BlockDialog
        },

        created () {
            this.isBlocked = this.tweet.isBlocked
        },

        methods: {

            // いいねするメソッド
            liked (tweet) {
                if (this.isBlocked) {
                    this.isBlockedDialog = true
                } else {
                    (tweet.isLiked) ? tweet.liked_count-- : tweet.liked_count++
                }
                this.tweet.isLiked = !this.tweet.isLiked

                this.$axios({
                    method: 'POST',
                    url: '/api/tweet/liked/',
                    data: {
                        target_tweet_pk : this.tweet.pk
                    },
                })
                .then(res => {
                    console.log(res)
                })
                .catch(e => {
                    console.log(e)
                })
            },

            closeModal () {
                this.isBlockedDialog = false
            },
        },
    }
</script>

<style>
    .retweet {
        cursor: pointer;
    }
</style>
