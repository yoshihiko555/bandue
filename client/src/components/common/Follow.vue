<template>
    <v-btn v-if='isFollow'
        class='teal lighten-4 ma-3'
        @click='follow'
    >フォローを外す</v-btn>
    <v-btn v-else
        class='teal lighten-4 ma-3'
        @click='follow'
    >フォローする</v-btn>
</template>

<script>
    import axios from 'axios'

    const IS_NOT_FOLLOW = 0
    const IS_FOLLOW = 1

    export default {
        props: ['username'],
        data: () => ({
            isFollow: false
        }),
        created () {
            console.log(this.username)
            // var JWTToken = this.$session.get('token')
            // axios.defaults.xsrfCookieName = 'csrftoken'
            // axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            this.$axios({
                method: 'POST',
                url: 'api/users/isFollow/',
                data: {
                    target_user : this.username
                },
                // headers: {
                //     Authorization: `JWT ${JWTToken}`,
                //     'Content-Type': 'application/json'
                // }
            })
            .then(res => {
                console.log(res.data)
                const status = res.data.status
                const isFollow = res.data.isFollow
                if (status === 'success') {
                    if (isFollow === IS_FOLLOW) {
                        this.isFollow = true
                        console.log('既にフォローしてる')
                    } else {
                        console.log('まだフォローしてない')
                    }
                }
            })
            .catch(e => {
                console.log(e)
            })
        },
        methods: {
            follow () {
                console.log('followMethod')
                // var JWTToken = this.$session.get('token')
                // axios.defaults.xsrfCookieName = 'csrftoken'
                // axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
                const targetUrl = (this.isFollow) ? 'unfollow' : 'follow'
                this.$axios({
                    method: 'POST',
                    url: 'api/users/' + targetUrl + '/',
                    data: {
                        target_user : this.username
                    },
                    // headers: {
                    //     Authorization: `JWT ${JWTToken}`,
                    //     'Content-Type': 'application/json'
                    // }
                })
                .then(res => {
                    console.log(res.data)
                    const status = res.data.status
                    const isFollow = res.data.isFollow
                    if (status === 'success') {
                        this.isFollow = isFollow === IS_FOLLOW
                    }
                })
                .catch(e => {
                    console.log(e)
                })
            }
        }
    }
</script>
