<template>
    <v-dialog v-model='replyDetailDialog' persistent max-width='600px'>
        <v-card>
            <v-container
                fluid
            >
                <v-row>
                    <v-col
                        cols='3'
                    >
                        <v-btn
                            @click='closeModal'
                            text
                            color='light-blue lighten-3'
                            class='close_btn'
                        >Close</v-btn>
                    </v-col>
                    <v-col
                        cols='6'
                        align='center'
                    >スレッド</v-col>
                    <v-col
                        cols='3'
                    ></v-col>
                </v-row>
            </v-container>
            <v-card>
                <v-card-title>
                    <v-avatar>
                        <v-img v-if='tweet.userIcon !== "/media/"' :src='tweet.userIcon'></v-img>
                        <v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
                    </v-avatar>
                    <v-btn
                        text
                        class='tweet_author z10'
                        @click='toProfile(tweet)'
                        style='text-transform: none'
                    >{{ tweet.author }}</v-btn>
                    <v-spacer></v-spacer>

                    <span class='created_time'>
                        {{ tweet.created_time }}
                    </span>
                </v-card-title>
                <v-card-text>
                    {{ tweet.content }}
                </v-card-text>
                <v-container fluid>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <reply
                            :tweet=tweet
                        ></reply>
                        <retweet
                            :tweet=tweet
                        ></retweet>
                        <like
                            :tweet=tweet
                        ></like>
                    </v-card-actions>
                </v-container>
            </v-card>
            <div v-for='(replyTweet, index) in targetTweet.reply' :key='`replyTweet.author-${index}`'>
                <v-card
                    flat
                    class='reply_tweet_wrap'
                >
                    <v-card-title>
                        <v-avatar>
                            <v-img v-if='replyTweet.userIcon !== "/media/"' :src='replyTweet.userIcon'></v-img>
                            <v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
                        </v-avatar>
                        <v-btn
                            text
                            class='tweet_author z10'
                            @click='toProfile(replyTweet)'
                            style='text-transform: none'
                        >{{ replyTweet.author }}</v-btn>
                        <v-spacer></v-spacer>

                        <span class='created_time'>
                            {{ replyTweet.created_time }}
                        </span>
                    </v-card-title>
                    <v-card-text>
                        {{ replyTweet.content }}
                    </v-card-text>
                    <v-container fluid>
                        <v-card-actions>
                            <v-spacer></v-spacer>
                            <reply
                                :tweet=replyTweet
                            ></reply>
                            <retweet
                                :tweet=replyTweet
                            ></retweet>
                            <like
                                :tweet=replyTweet
                            ></like>
                        </v-card-actions>
                    </v-container>
                </v-card>
            </div>
        </v-card>
    </v-dialog>
</template>
<script>
    import { Common } from '@/static/js/common'
    import Retweet from '@/components/common/Retweet'
    import Like from '@/components/common/Like'
    import Reply from '@/components/common/Reply'

    const Com = new Common()

    export default {
        name: 'ReplyDetail',
        props: {
            tweet: {
                type: Object,
                required: true
            },
            replyDetailDialog: {
                tyle: Boolean,
                required: true
            }
        },
        data: () => ({
            targetTweet: {}
        }),
        components: {
            Retweet,
            Like,
            Reply,
        },
        created () {
        },
        mounted: function () {
        },
        watch: {
            replyDetailDialog: function (newValue, oldValue) {
                if (newValue === true && oldValue === false) {
                    this.getReplyDetail()
                }
            }
        },
        methods: {
            closeModal () {
                this.$emit('closeModal')
            },
            getReplyDetail () {
                this.$axios({
                    method: 'GET',
                    url: '/api/tweet/replyDetail/',
                    params: {
                        target_tweet_pk : this.tweet.pk,
                    },
                })
                .then(res => {
                    var updatedAt = res.data.updated_at.substr(0, 10)
                    res.data.updated_at = updatedAt
                    this.targetTweet = res.data
                    console.log(this.targetTweet)
                })
                .catch(e => {
                    console.log(e)
                })
            },
            toProfile (tweet) {
                this.$router.push('/profile/' + tweet.author + '/')
                // Com.reload(this.$router)
            },
        }
    }
</script>
<style>
</style>
