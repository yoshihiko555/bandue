<template>
    <span>
        <span v-if='profileData.isSendFollowRequest'>
            <v-btn
                class='blue lighten-5 ma-3'
                color='white'
                @click='clearFollowRequest'
            >フォロー申請中</v-btn>
        </span>
        <span v-else>
            <v-btn v-if='profileData.isFollow'
                class='blue lighten-4 ma-3'
                color='white'
                @click='unFollow'
            >フォローを外す</v-btn>
            <v-btn v-else
                class='blue lighten-4 ma-3'
                color='white'
                @click='follow'
            >フォローする</v-btn>
        </span>
        <BlockDialog
          @closeModal='closeModal'
          :username='profileData.username'
          :isBlockedDialog='isBlockedDialog'
          :event='"follow"'
        ></BlockDialog>
    </span>
</template>

<script>
    import BlockDialog from '@/components/common/BlockDialog'

    const IS_FOLLOW = 1
    export default {
        name: 'Follow',
        props: [
          'profileData'
        ],
        data: () => ({
            isBlockedDialog: false,
        }),
        components: {
          BlockDialog
        },
        created () {

        },
        methods: {
            follow () {
                console.log('followMethod')
                const {isFollow, isPrivate, isBlocked} = this.profileData
                if (isPrivate || isBlocked) {
                    if (isBlocked) {
                        this.showBlockedDialog()
                    } else if (isPrivate) {
                        this.sendFollowRequest()
                    }
                } else {
                    this.profileData.isFollow = true
                    this.$axios({
                        method: 'POST',
                        url: '/api/users/follow/',
                        data: {
                            target_user : this.profileData.username
                        },
                    })
                    .then(res => {
                        console.log(res.data)
                    })
                    .catch(e => {
                        console.log(e)
                    })
                }
            },
            unFollow () {
                this.profileData.isFollow = false
                this.$axios({
                    method: 'POST',
                    url: '/api/users/unFollow/',
                    data: {
                        target_user : this.profileData.username
                    },
                })
                .then(res => {
                    console.log(res.data)
                })
                .catch(e => {
                    console.log(e)
                })
            },
            closeModal () {
                this.isBlockedDialog = false
            },
            showBlockedDialog () {
                this.isBlockedDialog = true
            },
            sendFollowRequest () {
                console.log('sendFollowRequest')
                this.profileData.isSendFollowRequest = true
                this.$axios({
                    method: 'POST',
                    url: '/api/users/followRequest/',
                    data: {
                        target_user: this.profileData.username
                    },
                })
                .then(res => {
                    console.log(res)
                })
                .catch(e => {
                    console.log(e)
                })
            },
            clearFollowRequest () {
                // フォロー申請をキャンセル。そのうち実装。
            },
        }
    }
</script>

<style>

</style>
