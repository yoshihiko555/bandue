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
						<v-card-title v-text='username'></v-card-title>
						<div v-for='(item, i) in messages' :key='i'>
							<v-card-text v-text='item.content'></v-card-text>
						</div>
						<v-textarea
							ref='content'
							class='input_message_area'
							@keydown='sendMessage'
							outlined
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
	import axios from 'axios'

	export default {
		name: 'MessageBox',
		data: () => ({
			username: null,
			messages: {},
			ws: null,
			isShowMsg: false,
			roomId: null,
			sender: null,
			receiver: null,
		}),
		mounted: function () {

		},
		methods: {
			showMessage (id, name) {
				var JWTToken = this.$session.get('token')
				axios.defaults.xsrfCookieName = 'csrftoken'
				axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
				axios({
					method: 'GET',
					url: 'http://192.168.33.12:8000/api/message/',
					headers: {
						Authorization: `JWT ${JWTToken}`,
						'Content-Type': 'application/json'
					}
				})
				.then(res => {
					console.log(res.data)
					this.messages = res.data
					const url = 'ws://' + window.location.host + '/ws/' + name + '/'
					this.ws = new WebSocket(url)
					this.isShowMsg = true
					this.username = name
					this.roomId = id
					this.sender = this.$session.get('username')
					this.receiver = name
				})
				.catch(e => {
					console.log(e)
				})
			},

			sendMessage (e) {
				if (((e.ctrlKey && !e.metaKey) || (!e.ctrlKey && e.metaKey)) && e.keyCode === 13) {
					var sendData = {
						roomId: this.roomId,
						content: this.$refs.content.internalValue,
						sender: this.sender,
						receiver: this.receiver,
					}
					console.log('送信')
					console.log(sendData)
					console.log(this.$refs.content)
					console.log(this.ws)
					this.ws.send(JSON.stringify(sendData))

					this.ws.onmessage = e => {
						console.log('ソケット結果受信')
						console.log(e)
						var receiveData = JSON.parse(e.data)
						this.messages.push(receiveData)
						this.$refs.content.internalValue = ''
					}
				}
			}
		}
	}
</script>

<style lang='scss'>
	.input_message_area {
		textarea {
			resize: none !important;
		}
	}
</style>
