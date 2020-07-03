<template>
  <span v-if='isFollow != null'>
    <v-btn v-if='isFollow'
        class='blue lighten-4 ma-3'
        color='white'
        :height=height
        :width=width
        @click='follow'
    >フォローを外す</v-btn>
    <v-btn v-else
        class='blue lighten-4 ma-3'
        color='white'
        :height=height
        :width=width
        @click='follow'
    >フォローする</v-btn>
  </span>
</template>

<script>
    const IS_FOLLOW = 1
    export default {
        props: ['username', 'height', 'width'],
        data: () => ({
            isFollow: null
        }),
        created () {
            console.log(this.username)
            this.$axios({
                method: 'POST',
                url: '/api/users/isFollow/',
                data: {
                    target_user : this.username
                },
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
                        this.isFollow = false
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
                const targetUrl = (this.isFollow) ? 'unfollow' : 'follow'
                this.$axios({
                    method: 'POST',
                    url: '/api/users/' + targetUrl + '/',
                    data: {
                        target_user : this.username
                    },
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

<style lang='scss'>

</scss>
