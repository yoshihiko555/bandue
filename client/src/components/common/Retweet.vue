<template>
    <v-icon v-if='isRetweeted === 0'
        class='mr-1 retweet'
        color='black lighten-1'
        @click='retweet'
        ref='retweet'
    >mdi-heart</v-icon>
    <v-icon v-else
        class='mr-1 retweet'
        color='black lighten-5'
        @click='retweet'
        ref='retweet'
    >mdi-heart</v-icon>
</template>

<script>
    export default {
        props: [
            'tweet_id',
            'isRetweeted'
        ],
        data: () => ({

        }),
        created () {

        },
        methods: {
            retweet (tweetId, isRetweeted, index) {
                console.log('retweet')
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
					console.log(res.data.isRetweeted)
                })
                .catch(e => {
                    console.log(e)
                })
            }
        }

    }

</script>

<style>
    .retweet {
        cursor: pointer;
    }
</style>
