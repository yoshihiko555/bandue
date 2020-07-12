<template>
	<div id="messagebox_wrap">
		<v-container fluid>
			<v-row>
				<v-col cols='12'>
					<v-card
						v-if='isShowMsg'
						outlined
						tile
					>
						<v-card-title v-text='roomName'></v-card-title>
						<v-divider></v-divider>
						<v-container id="messages" class="message_wrap" ref='messages'>
							<v-row v-for='(item, i) in messages' :key='i'>
                                <v-col cols='12'>
                                    <v-row v-if='item.deleted' class="message_coutent_wrap" :class='{ sender: item.isMe, receiver: !item.isMe }'>
                                        <v-card-text class="message deleted" :class='{ sender: item.isMe, receiver: !item.isMe }'>削除されました</v-card-text>
                                    </v-row>

                                    <v-row v-else class="message_coutent_wrap" :class='{ sender: item.isMe, receiver: !item.isMe }'>
                                        <v-card-text v-html='item.content' class='message' :class='{ sender: item.isMe, receiver: !item.isMe }'></v-card-text>
                                        <!-- Message編集ボタン -->
                                        <v-menu bottom left>
                                            <template v-slot:activator='{ on }'>
                                                <v-btn
                                                    dark
                                                    icon
                                                    v-on='on'
                                                    color='grey'
                                                    v-show='item.isMe'
                                                >
                                                    <v-icon>mdi-dots-vertical</v-icon>
                                                </v-btn>
                                            </template>

                                            <v-list>
                                                <v-list-item @click='updateMessage(item)'>
                                                    <v-list-item-title>削除</v-list-item-title>
                                                </v-list-item>
                                            </v-list>
                                        </v-menu>
                                    </v-row>
                                </v-col>

							</v-row>
						</v-container>

						<v-textarea
							ref='content'
							class='input_message_area'
							@keydown='sendMessage'
							outlined
							no-resize
							auto-grow
							rows='1'
							placeholder='メッセージを入力'
						></v-textarea>
					</v-card>

					<v-card
						v-if='!isShowMsg'
						outlined
						tile
					>
						<v-card-title>メッセージを選択してください</v-card-title>
					</v-card>
				</v-col>
			</v-row>
		</v-container>
	</div>
</template>

<script>
	export default {
		name: 'MessageBox',
		data: () => ({
			loginUser: null,
			roomName: null,
			messages: {},
			ws: null,
			isShowMsg: false,
			roomId: null,
			sender: null,
			receiver: null,
            showMenu: false,
		}),
		mounted: function () {
			this.loginUser = (this.$store.state.isAuth) ? this.$store.state.loginUser : null
		},
		updated () {
			this.scrollEnd()
		},
		methods: {
			showMessage (id, roomName) {
				this.$axios({
					method: 'GET',
					url: '/api/message/',
					params: {
						loginUser: this.loginUser
					},
				})
				.then(res => {
					console.log('メッセージ一覧', res.data)
					this.messages = res.data
					this.isShowMsg = true
					this.roomName = roomName
					this.roomId = id
					this.sender = this.$store.state.loginUser
					this.receiver = roomName
					const url = 'ws://' + window.location.host + '/ws/' + id + '/'
					this.ws = new WebSocket(url)
				})
				.catch(e => {
					console.log(e)
				})
			},

			sendMessage (e) {
				if (((e.ctrlKey && !e.metaKey) || (!e.ctrlKey && e.metaKey)) && e.keyCode === 13) {
					var sendData = {
						roomId: this.roomId,
						content: this.$refs.content.internalValue.replace(/\r?\n/g, '<br>'),
						sender: this.sender,
						receiver: this.receiver,
					}
					console.log('送信データ',sendData)
					this.ws.send(JSON.stringify(sendData))

					this.ws.onmessage = e => {
						var receiveData = JSON.parse(e.data)
						var isMe = this.loginUser === receiveData.sender
						receiveData.isMe = isMe
						console.log('ソケット結果受信', receiveData)
						this.messages.push(receiveData)
						this.$refs.content.internalValue = ''
					}
				}
			},

			scrollEnd () {
				var ref = this.$refs.messages
				ref.scrollTop = ref.scrollHeight
            },
            
            updateMessage (msg) {
                console.log(msg)
                this.$axios({
                    url: `/api/message/${msg.id}/message_delete/`,
                    method: 'PUT',
                })
                .then(res => {
                    console.log(res)
                    msg.deleted = true
                })
                .catch(e => {
                    console.log(e)
                })
            },
		},
	}
</script>

<style lang='scss'>
#messagebox_wrap{
	.message_wrap {
		height: 490px;
		overflow: auto;

        .message_coutent_wrap {
            &.sender {
                justify-content: flex-end;
            }
            &.receiver {
                justify-content: flex-start;
            }

            .message {
                margin: 5px 10px;
                padding: 10px;
                width: auto;
                max-width: 50%;
                border-radius: 10px;
                clear: both;
                position: relative;
                display: inline-block;

                &:after {
                    content: '';
                    position: absolute;
                    top: 50%;
                }
            }
            .sender {
                background-color: #80CBC4;

                &:after {
                    right: -7px;
                    border-style: solid;
                    border-width: 10px 0 10px 15px;
                    border-color: transparent transparent transparent #80CBC4;
                }
            }
            .receiver {
                background-color: #CFD8DC;

                &:after {
                    left: -7px;
                    border-style: solid;
                    border-width: 10px 15px 10px 0;
                    border-color: transparent #CFD8DC transparent transparent;
                }
            }
            .deleted {
                background-color: #ccc;
                &:after {
                    border: none;
                }
            }
        }
	}

	.input_message_area {
		clear: both;
		textarea {
			margin: 2px 2px 2px 0;
			overflow: auto;
			max-height: 120px;

			&::-webkit-scrollbar {
				width:7px;
			}

			&::-webkit-scrollbar-thumb {
				background-color: #cacaca;
				border-radius: 5px;
			}

			&::-webkit-scrollbar-track {
				background: rgba(100,100,100, 0);
			}
		}
	}
}

</style>
