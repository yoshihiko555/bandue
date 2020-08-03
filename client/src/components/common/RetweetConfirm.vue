<template>
    <v-dialog
        v-model='retweetConfirmDialog'
        max-width='600'
        persistent
    >
        <v-card>
            <v-card-title>
              リツイートしますか？
            </v-card-title>

            <v-container
              class='retweet_target_wrap'
            >
                <v-card>
                    <v-card-title>
                        <v-avatar>
                            <v-img v-if='tweet.userIcon !== "/media/"' :src='tweet.userIcon'></v-img>
                            <v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
                        </v-avatar>
                        {{ tweet.author }}
                        <v-spacer></v-spacer>
                        <span class='created_time'>
                            {{ tweet.created_time }}
                        </span>
                    </v-card-title>

                    <v-card-text>
                        {{ tweet.content }}
                    </v-card-text>

                    <div>
                        <img :src='tweet.images' width="100">
                    </div>
                    <v-list-item>
                        <v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
                            <v-list-item-title>{{ tag.title }}</v-list-item-title>
                        </v-list-item-content>

                        <v-row
                            align='center'
                            justify='end'
                        >
                            <!-- リプライボタン -->
                            <v-icon
                                color='grey lighten-2'
                            >mdi-chat-outline</v-icon>
                            <span class='mr-2'>{{ tweet.reply_count }}</span>

                            <!-- リツイートボタン -->
                            <v-icon v-if='!tweet.isRetweeted'
                                color='grey lighten-1'
                            >mdi-repeat</v-icon>
                            <v-icon v-else
                                color='green lighten-1'
                            >mdi-repeat</v-icon>
                            <span class='mr-2'>{{ tweet.retweet_count }}</span>

                            <!-- いいねボタン -->
                            <v-icon
                                color='red lighten-3'
                                ref='tweet_isLiked'
                            >mdi-heart</v-icon>
                            <span class='mr-2'>{{ tweet.liked_count }}</span>

                        </v-row>

                    </v-list-item>
                </v-card>
            </v-container>

            <v-card-actions
              class='retweet_btn_area'
            >
                <v-btn
                    text
                    color='light-blue lighten-3'
                    class='retweet_cancel_btn'
                    @click='closeModal'
                >Close</v-btn>
                <v-spacer></v-spacer>
                <v-btn
                    v-if='!tweet.isRetweeted'
                    x-large
                    @click='retweet(tweet)'
                    class='retweet_btn'
                >
                    <v-icon
                        color='green lighten-1'
                    >mdi-repeat</v-icon>リツイート
                </v-btn>
                <v-btn
                    v-else
                    x-large
                    @click='retweet("tweet")'
                    class='retweet_delete_btn'
                >
                    <v-icon
                        color='red lighten-1'
                    >mdi-repeat</v-icon>リツイートを取り消す
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
    export default {
        name: 'RetweetConfirm',

        props: ['tweet', 'retweetConfirmDialog'],

		data: () => ({
        }),

        methods: {
            closeModal () {
                this.$emit('closeModal')
            },

            retweet () {
                this.$emit('retweet')
            },

        }
    }

</script>
<style lang='scss'>

  .retweet_target_wrap {
    width: 90%;
  }

  .retweet_btn_area {
    margin-top: 50px;
    height: 100px;
  }

  .retweet_cancel_btn {
    margin-top: 20px;
    margin-left: 20px;
  }

  .retweet_btn {
    margin-right: 15px;
    height: 120px;
    width: 150px;
  }

  .retweet_delete_btn {
    margin-right: 15px;
    height: 150px;
  }
</style>
