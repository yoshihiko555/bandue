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
				this.$emit('togle-signout-modal')
			},

			signout () {
				console.log('サインアウト')
				this.$store.commit('initState')
				this.$router.push('/')
				// Com.reload(this.$router)
			}
		}
	}
</script>
