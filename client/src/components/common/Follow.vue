<template>
    <span>
        <span v-if='profileData.isSendFollowRequest'>
            <v-btn
                class='follow_btn blue lighten-5'
                color='white'
                @click='clearFollowRequest'
                height=height
                width=width
                v-bind:style='followBtnStyleObject'
            >フォロー申請中</v-btn>
        </span>

        <span v-else>
            <v-btn v-if='profileData.isFollow'
                class='follow_btn blue lighten-4'
                color='white'
                @click='unFollow'
                v-bind:style='followBtnStyleObject'
            >フォローを外す</v-btn>
            <v-btn v-else
                class='follow_btn outlined'
                color='white'
                @click='follow'
                v-bind:style='followBtnStyleObject'
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
          'profileData',
          'followBtnStyleObject',
        ],

        data: () => ({
            isBlockedDialog: false,
        }),

        components: {
          BlockDialog
        },

        created () {
        },
        mounted: function () {
            console.log(this.styleObject)
        },
        methods: {

            // フォローするメソッド
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

            // フォロー解除するメソッド
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

            // フォロー申請を送るメソッド
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
    .search_follow_btn {
        font-size: 100px;
    }
</style>
