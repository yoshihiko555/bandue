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
  </div>
</template>

<script>
  import ReplyModal from '@/components/common/ReplyModal'

  export default {
    props: {
      tweet: {
        type: Object,
        required: true
      }
    },
    components: {
      ReplyModal,
    },
    data: () => ({
      replyModalDialog: false,
      selectTweet: {},
    }),
    created () {

    },
    mounted: function () {

    },
    methods: {
      showReplyModal (tweet) {
        console.log('showReplyModal')
        this.replyModalDialog = true
        this.selectTweet = tweet
      },
      closeModal () {
        this.replyModalDialog = false
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
