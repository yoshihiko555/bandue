<template>
	<v-dialog v-model='tweetEditDialog' persistent max-width='600px'>
		<v-card>
			<v-card-title>
				<span class='title font-weight-light'>編集</span>
			</v-card-title>

			<v-card-text>
				<v-container>
					<v-row>
						<v-col cols='12'>
							<v-textarea
								v-model='tweet.content'
								solo
								flat
								auto-grow
								clearable
								:counter='144'
								label="何が起こっていますか？"
								:value="tweet.content"
							></v-textarea>
							<v-file-input
							><v-icon>mdi-image</v-icon></v-file-input>
						</v-col>
					</v-row>
				</v-container>
			</v-card-text>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color='teal lighten-4' @click='closeModal'>Close</v-btn>
				<v-btn color='teal lighten-4' @click='tweetEdit'>Edit</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script>
	export default {
		name: 'TweetEdit',
		props: ['tweet', 'tweetEditDialog'],
		data: () => ({
			update: {
				content: ''
			}
		}),

		mounted () {

		},

		methods: {
			closeModal () {
				this.$emit('closeModal')
			},

			tweetEdit () {
				this.$axios({
					method: 'PUT',
					url: '/api/tweet/' + this.tweet.pk + '/',
					data: {
						content : this.tweet.content
					},
				})
				.then(res => {
					console.log(res)
					this.closeModal()
				})
				.catch(e => {
					console.log(e)
				})
			},
			
		}
	}
</script>
