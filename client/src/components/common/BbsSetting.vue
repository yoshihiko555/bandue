<template>
	<v-container fluid>
		<div v-for='(article, i) in articleList' :key='i'>
			<v-row align='center'>
				<v-col cols='9'>
					{{ article.title }}
				</v-col>

				<v-col cols='3'>
					<v-btn
						class='teal lighten-4 ma-3'
						@click='articleDelete(article.id)'
					>DELETE</v-btn>
				</v-col>
			</v-row>
		</div>
	</v-container>
</template>

<script>
	export default {
		name: 'BbsSetting',
		data: () => ({
			articleList: []
		}),

		mounted: function () {
			this.$axios({
				method: 'GET',
				url: '/api/entry/'
			})
			.then(res => {
				console.log('記事一覧', res.data)
				this.articleList = res.data
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
			articleDelete (id) {
				this.$axios({
					method: 'DELETE',
					url: '/api/entry/' + id
				})
				.then(res => {
					console.log(res)
					this.articleList = res.data
				})
				.catch(e => {
					console.log(e)
				})
			}
		}
	}
</script>
