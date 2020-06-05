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
            retweet () {
                console.log('retweet')
                console.log(this.tweet_id)
                var JWTToken = this.$session.get('token')
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
                const targetUrl = (this.isRetweeted === 0) ? 'retweet' : 'unRetweet'
                axios({
                    method: 'POST',
                    url: 'http://192.168.33.12:8000/api/tweet/' + targetUrl + '/',
                    data: {
                        target_tweet_id : this.tweet_id
                    },
                    headers: {
                        Authorization: `JWT ${JWTToken}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => {
                    console.log(res.data)
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
