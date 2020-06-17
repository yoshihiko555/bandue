<template>
    <v-dialog
        v-model='retweetConfirmDialog'
        max-width='600'
        persistent
    >
        <v-card>
            <v-card-actions>
                <v-row>
                    <v-btn
                        v-if='!tweet.isRetweeted'
                        text
                        @click='retweet(tweet)'
                    >
                        <v-icon
                            color='black lighten-5'
                        >mdi-repeat</v-icon>リツイート
                    </v-btn>

                    <v-btn
                        v-else
                        text
                        @click='retweet("tweet")'
                    >
                        <v-icon
                            color='red lighten-1'
                        >mdi-repeat</v-icon>リツイートを取り消す
                    </v-btn>
                </v-row>
                <v-btn
                    text
                    @click='closeModal'
                >キャンセル</v-btn>
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
            }

        }
    }

</script>
