<template>
  <span>
    <span v-if='isFollow != null'>
      <v-btn v-if='isFollow'
          class='blue lighten-4 ma-3'
          color='white'
          @click='follow'
      >フォローを外す</v-btn>
      <v-btn v-else
          class='blue lighten-4 ma-3'
          color='white'
          @click='follow'
      >フォローする</v-btn>
    </span>
    <BlockDialog
      @closeModal='closeModal'
      :username='username'
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
          'username',
          'isBlocked',
          'isPrivate',
        ],
        data: () => ({
            isFollow: null,
            isBlockedDialog: false,
        }),
        components: {
          BlockDialog
        },
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
                if (this.isPrivate && this.isBlocked) {
                  console.log('非公開＆ブロック')
                  this.isBlockedDialog = true
                } else if (this.isPrivate) {
                  console.log('非公開アカウントのためフォローには許可が必要')
                // フォローを認証する仕組み作る
                } else if (this.isBlocked) {
                  console.log('ブロックされているためフォロー出来ない')
                  this.isBlockedDialog = true
                } else {
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
            },
            closeModal () {
              this.isBlockedDialog = false
            }
        }
    }
</script>

<style>

</style>
