<template>
    <v-dialog
        v-model='replyModalDialog'
        max-width='600'
        persistent
        class='reply_modal_wrap'
    >
        <v-card>
            <v-card-title>
              @{{ tweet.author }}さんへ返信
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols='12'>
                    <v-textarea
                      v-model='reply_content'
                      prepend-inner-icon='mdi-chat-processing-outline'

                      solo
                      label='返信をツイート'
                      :counter='144'
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color='light-blue lighten-3'
                class='reply_cancel_btn'
                @click='closeModal'
                text
              >Close</v-btn>
              <v-spacer></v-spacer>
              <v-btn
                color='primary light-blue lighten-3'
                class='reply_send_btn'
                x-large
                width='140px'
                @click='reply'
              >Send</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: 'ReplyModal',
        props: {
          tweet: {
            type: Object,
            required: true
          },
          replyModalDialog: {
            type: Boolean,
            required: true
          },
        },
    		data: () => ({
          reply_content: ''
    		}),
        created () {

        },
        mounted: function () {

        },
        methods: {
            closeModal () {
                this.$emit('closeModal')
            },
            reply () {
                if (this.reply_content.length !== 0) {
                    this.$emit('reply', this.reply_content)
                    this.closeModal()
                    this.reply_content = ''
                }
            }
        },
    }

</script>
<style lang='scss'>

  .reply_cancel_btn {
    margin-top: 20px;
    margin-left: 20px;
  }

  .reply_send_btn {
    margin-right: 20px;
    margin-bottom: 10px;
  }
</style>
