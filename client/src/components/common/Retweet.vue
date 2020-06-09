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
    import axios from 'axios'

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
                // var JWTToken = this.$session.get('token')
                // axios.defaults.xsrfCookieName = 'csrftoken'
                // axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
                const targetUrl = 'retweet'
                axios({
                    method: 'POST',
                    url: 'api/tweet/' + targetUrl + '/',
                    data: {
                        target_tweet_id : tweetId
                    },
                    // headers: {
                    //     Authorization: `JWT ${JWTToken}`,
                    //     'Content-Type': 'application/json'
                    // }
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
