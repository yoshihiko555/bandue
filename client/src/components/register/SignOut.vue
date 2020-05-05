<template>
	<v-row
		justify='center'
	>
		<v-dialog
			v-model='dialog'
			max-width='300'
			persistent
		>
			<v-card>
				<v-card-title class='headline'>Signout</v-card-title>

				<v-card-text>
					BandueからSignoutしますか？
				</v-card-text>
					<div class='text-center'>
						<v-btn
							depressed
							class='ma-5'
							@click='closeModal'
						>
							戻る
						</v-btn>
						<v-btn
							depressed
							class='ma-5 teal lighten-4'
							@click='signout'
						>
							SignOut
						</v-btn>
					</div>
			</v-card>
		</v-dialog>
	</v-row>
</template>

<script>
	import { Common } from '@/static/js/common'

	const Com = new Common()
	export default {
		name: 'SignOut',
		props: ['dialog'],
		data: () => ({

		}),

		methods: {
			closeModal () {
				this.$emit('togle-signout-modal', false)
			},

			signout () {
				console.log('サインアウト')
				this.$session.remove('token')
				console.log(this.$session.has('token'))
				this.$router.push('/')
				Com.reload(this.$router)
				// const token = this.$session.get('token')
				// axios.defaults.xsrfCookieName = 'csrftoken'
				// axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
				// axios.delete('http://192.168.33.12:8000/api/signout/', {

				// 今後取得したTOKENを利用して処理を行う場合のために一旦残しておく
				// 以下のようにheadersの中に、tokenを埋め込んでAjaxを投げると、
				// サーバ側でtokenが正しいか判定して、処理を行う
				// (例)パスワードのリセット処理などで行う
				// 	headers: {
				// 		'Content-Type': 'application/json',
				// 		Authorization: `Bearer ${token}`
				// 	}
				// })

				// .then(res => {
					// console.log(res)
				// })
				// .catch(e => {
				// 	console.log(e)
				// 	console.log(this.$session.has('token'))
				// })
			}
		}
	}
</script>
