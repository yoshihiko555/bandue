<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<v-card
					class='mx-auto'
					max-width='400'
				>
					<v-card-title>
						<span class='title font-weight-light'>Bandue</span>
					</v-card-title>

					<v-form>
						<v-textarea
							solo
							flat
							auto-grow
							clearable
							:counter='144'
							label="何が起こっていますか？"
							v-model="tweet_content"
						></v-textarea>
						<v-file-input
						><v-icon>mdi-image</v-icon></v-file-input>
						<div class="text-right">
							<v-btn
								class='teal lighten-4 ma-3'
								@click='tweet'
							>つぶやく</v-btn>
						</div>
					</v-form>
				</v-card>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
	export default {
		props: ['data'],
		name: 'Tweet',
		data: () => ({
			valid: true,
			loading: false,
			tweet_content: ''
		}),
		methods: {
			tweet () {
				this.$axios({
					method: 'POST',
					url: '/api/tweet/',
					data: {
						content : this.tweet_content
					},
				})
				.then(res => {
					console.log(res.data)
					this.$eventHub.$emit('create-tweet', res)
					this.tweet_content = ''
				})
				.catch(e => {
					console.log(e)
				})
			}
		}
	}
</script>
