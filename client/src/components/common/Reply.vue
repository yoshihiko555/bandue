<template>
  <div>
    <v-btn
      icon
      @click='showReplyModal(tweet)'
      class='z10'
    >
      <v-icon
        color='grey lighten-2'
      >mdi-chat-outline</v-icon>
    </v-btn>
    <span class='mr-2'>{{ tweet.reply_count }}</span>

    <ReplyModal
      @closeModal='closeModal'
      @reply='reply'
      :tweet='selectTweet'
      :replyModalDialog='replyModalDialog'
    ></ReplyModal>

    <BlockDialog
      @closeModal='closeModal'
      :username='tweet.author'
      :isBlockedDialog='isBlockedDialog'
      :event='"reply"'
    ></BlockDialog>
  </div>
</template>

<script>
  import ReplyModal from '@/components/common/ReplyModal'
  import BlockDialog from '@/components/common/BlockDialog'

  export default {
    props: {
      tweet: {
        type: Object,
        required: true
      },
    },
    components: {
      ReplyModal,
      BlockDialog,
    },
    data: () => ({
      replyModalDialog: false,
      selectTweet: {},
      isBlocked: false,
      isBlockedDialog: false,
    }),
    created () {
      this.isBlocked = this.tweet.isBlocked
    },
    mounted: function () {

    },
    methods: {
      showReplyModal (tweet) {
        if (this.isBlocked) {
          this.isBlockedDialog = true
        } else {
          console.log('showReplyModal')
          this.replyModalDialog = true
          this.selectTweet = tweet
        }
      },
      closeModal () {
        this.replyModalDialog = false
        this.isBlockedDialog = false
      },
      reply (content) {
        console.log('reply')
        console.log(content)
        let tweet = this.selectTweet

        this.$axios({
          method: 'POST',
          url: '/api/tweet/reply/',
          data: {
            target_tweet_pk : tweet.pk,
            content: content
          },
        })
        .then(res => {
          console.log(res)
          tweet.reply_count++
        })
        .catch(e => {
          console.log(e)
        })

      }
    },
  }
</script>

<style>

</style>
