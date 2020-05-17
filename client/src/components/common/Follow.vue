<template>
    <v-btn v-if='isNotFollow'
        class='teal lighten-4 ma-3'
        @click='follow'
    >フォローする</v-btn>
    <v-btn v-else
        class='teal lighten-4 ma-3'
        @click='unfollow'
    >フォローを外す</v-btn>
</template>

<script>
    import axios from 'axios'

    const IS_NOT_FOLLOW = 0
    const IS_FOLLOW = 1

    export default {
        props: ['username'],
        data: () => ({
            isNotFollow: true
        }),
        created () {
            // フォローしてるか確認して返り値でisNotFollowを切り替え
            // isNotFollow = true ... フォローしてない。「フォロー」
            // isNotFollow = false ... 既にフォローしてる。「フォローを外す」
            
            console.log('Profileから渡されてる?')
            console.log(this.username)
            var JWTToken = this.$session.get('token')
            axios.defaults.xsrfCookieName = 'csrftoken'
            axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
            axios({
                method: 'POST',
                url: 'http://192.168.33.12:8000/api/users/isFollow/',
                data: {
                    target_user : this.username
                },
                headers: {
                    Authorization: `JWT ${JWTToken}`,
                    'Content-Type': 'application/json'
                }
            })
            .then(res => {
                console.log(res.data)
                const status = res.data.status
                const isFollow = res.data.isFollow
                if (status === 'success') {
                    if (isFollow === IS_FOLLOW) {
                        this.isNotFollow = false
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
                console.log('follow発動')
                var JWTToken = this.$session.get('token')
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
                axios({
                    method: 'POST',
                    url: 'http://192.168.33.12:8000/api/users/follow/',
                    data: {
                        target_user : this.username
                    },
                    headers: {
                        Authorization: `JWT ${JWTToken}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => {
                    console.log(res.data)
                    const status = res.data.status
                    const isFollow = res.data.isFollow
                    if (status === 'success' && isFollow === IS_FOLLOW) {
                        this.isNotFollow = false
                    }
                })
                .catch(e => {
                    console.log(e)
                })
            },
            unfollow () {
                console.log('follow解除')
                var JWTToken = this.$session.get('token')
                axios.defaults.xsrfCookieName = 'csrftoken'
                axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
                axios({
                    method: 'POST',
                    url: 'http://192.168.33.12:8000/api/users/unfollow/',
                    data: {
                        target_user : this.username
                    },
                    headers: {
                        Authorization: `JWT ${JWTToken}`,
                        'Content-Type': 'application/json'
                    }
                })
                .then(res => {
                    console.log(res.data)
                    const status = res.data.status
                    const isFollow = res.data.isFollow
                    if (status === 'success' && isFollow === IS_NOT_FOLLOW) {
                        this.isNotFollow = true
                    }
                })
                .catch(e => {
                    console.log(e)
                })
            }
        }
    }
</script>
