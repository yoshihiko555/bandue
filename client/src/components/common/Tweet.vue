<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<v-card
					class='mx-auto'
					max-width='400'
				>
					<v-card-title>
						<img src='@/static/img/Logo_Icon.png' alt="logo" width="40">
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
						<div v-show='showImage' class="preview_wrap">
							<img :src="previewSrc" alt="" width="300"/>
							<v-btn
								icon
								class='delete_image_btn grey darken-3 ma-2'
								@click='delete_image'
							>
								<v-icon color='white'>mdi-close</v-icon>
							</v-btn>
						</div>
						<v-file-input
							hide-input
							class='ml-2'
							ref='input'
							accept="image/*"
							prepend-icon="mdi-image"
							@change='inputFile'
						>
						</v-file-input>
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
	const reader = new FileReader()

	export default {
		props: ['data'],
		name: 'Tweet',
		data: () => ({
			valid: true,
			loading: false,
			tweet_content: '',
			showImage: false,
			file: null,
			previewSrc: '',
		}),
		methods: {
			tweet () {
				var tweetData
				// 画像があればFormDataとして、送信
				if (this.file !== null) {
					tweetData = new FormData()
					tweetData.append('images', this.file)
					tweetData.append('content', this.tweet_content)
				} else {
					tweetData = {
						content: this.tweet_content
					}
				}
				console.log('送信データ', tweetData)
				this.$axios({
					method: 'POST',
					url: '/api/tweet/',
					data: tweetData,
				})
				.then(res => {
					console.log(res)
					this.$eventHub.$emit('create-tweet', res)
					this.tweet_content = ''
					this.file = null
					this.previewSrc = ''
					this.$refs.input.lazyValue = ''
					this.showImage = false
				})
				.catch(e => {
					console.log(e)
				})
			},
			inputFile (e) {
				reader.readAsDataURL(e)
				reader.onload = e => {
					this.previewSrc = e.target.result
				}
				this.file = e
				this.showImage = true
			},
			delete_image () {
				this.file = null
				this.file = null
				this.previewSrc = ''
				this.$refs.input.lazyValue = ''
				this.showImage = false
			}
		}
	}
</script>

<style lang='scss'>
	.preview_wrap {
		position: relative;

		.delete_image_btn {
			position: absolute;
			top: 0;
			left: 0;
			width: 30px;
			height: 30px;
		}
	}
</style>
