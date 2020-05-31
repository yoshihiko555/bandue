<template>
	<v-dialog v-model='dialog' fullscreen hide-overlay transition="dialog-bottom-transition">
		<template v-slot:activator="{ on }">
			<v-btn
				depressed
				tile
				width='100%'
				class='teal lighten-2 white--text mb-3'
				v-on='on'
			>
				記事投稿
			</v-btn>
		</template>

		<v-card>
			<v-container fluid>
				<v-row class="create_article_title_wrap">
					<v-card-title class="">記事を投稿する</v-card-title>
					<v-spacer></v-spacer>
					<v-btn color="teal darken-1" class='white--text create_article_close_btn' tile depressed icon @click="dialog = false">
						<v-icon>mdi-close-octagon</v-icon>
					</v-btn>
				</v-row>
				<v-row>
					<v-col cols='12'>
						<v-form>
							<v-text-field
								v-model='title'
								outlined
								placeholder='Title'
							></v-text-field>
							<v-textarea
								v-model='content'
								outlined
								placeholder='Content'
								rows='20'
							></v-textarea>
						</v-form>
					</v-col>
				</v-row>

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn v-show='isSave' color="teal darken-1" class='white--text' tile depressed @click="save">下書き</v-btn>
					<v-btn v-show='!isSave' color="teal darken-1" class='white--text' tile depressed @click="create">投稿</v-btn>
					<v-menu top :offset-y='offset'>
						<template v-slot:activator='{ on }'>
							<v-btn color='teal darken-1' class='drop_up_btn' tile depressed v-on='on'>
								<v-icon class='white--text'>mdi-menu-up</v-icon>
							</v-btn>
						</template>

						<v-list>
							<v-list-item @click='isSave = true'>
								<v-list-item-title>下書き</v-list-item-title>
							</v-list-item>

							<v-list-item @click='isSave = false'>
								<v-list-item-title>投稿</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</v-card-actions>
			</v-container>
		</v-card>
	</v-dialog>
</template>

<script>
	import axios from 'axios'

	export default {
		name: 'CreateArticle',
		components: {

		},
		data: () => ({
			dialog: false,
			isSave: false,
			offset: true,
			title: '',
			content: ''
		}),
		mounted: function () {

		},

		methods: {
			save () {
				console.log('下書き')
				this.dialog = false
			},

			create () {
				console.log('投稿')
				var JWTToken = this.$session.get('token')
				axios.defaults.xsrfCookieName = 'csrftoken'
				axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
				axios({
					method: 'POST',
					url: 'http://192.168.33.12:8000/api/bbs/',
					data: {
						title: this.title,
						content : this.content
					},
					headers: {
						Authorization: `JWT ${JWTToken}`,
						'Content-Type': 'application/json'
					}
				})
				.then(res => {
					console.log(res.data)
					this.dialog = false
					this.$eventHub.$emit('create-tweet', res)
				})
				.catch(e => {
					console.log(e)
				})
			}
		}
	}
</script>

<style lang='scss'>
	.create_article_title_wrap {
		align-items: center;

		.create_article_close_btn {
			position: absolute;
			right: 1%;
		}
	}
	.drop_up_btn {
		border-left: solid 1px #ccc !important;
	}
</style>
