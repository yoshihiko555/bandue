<template>
	<v-container fluid>
		<div v-for='(article, i) in articleList' :key='i'>
			<v-row align='center' class="edit_article_list_wrap">
				<v-col cols='10'>
					{{ article.title }}
				</v-col>

				<v-col cols='2'>
					<v-menu bottom left>
						<template v-slot:activator='{ on }'>
							<v-btn
								icon
								v-on='on'
								color='grey'
							>
								<v-icon>mdi-dots-vertical</v-icon>
							</v-btn>
						</template>

						<v-list>
							<v-list-item
								v-for='(item, i) in kebabMenu'
								:key='i'
								@click='articleEditMethods(i, article)'
							>
								<v-list-item-title :class='item.color'>{{ item.title }}</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</v-col>
			</v-row>
		</div>

		<EditArticle
			@closeModal='closeModal'
			:editDialog='editDialog'
			:article='selectArticle'
		></EditArticle>
	</v-container>

</template>

<script>
	import EditArticle from '@/components/common/EditArticle'

	export default {
		name: 'BbsSetting',
		components: {
			EditArticle
		},
		data: () => ({
			articleList: [],
			kebabMenu: [
				{
					title: 'Edit',
					color: '',
				},
				{
					title: 'Delete',
					color: 'red--text',
				}
			],
			editDialog: false,
			selectArticle: {},
		}),

		mounted: function () {
			this.$axios({
				method: 'GET',
				url: '/api/entry/'
			})
			.then(res => {
				console.log('記事一覧', res.data)
				this.articleList = res.data.results
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
			articleEditMethods (i, article) {
				const methodsList = [
					this.showArticleEdit,
					this.articleDelete,
				]

				if (methodsList[i] !== '') {
					methodsList[i](article)
				}
			},
			showArticleEdit (article) {
				console.log('記事編集', article)
				this.editDialog = true
				this.selectArticle = article
			},
			articleDelete (article) {
				this.$axios({
					method: 'DELETE',
					url: '/api/entry/' + article.id
				})
				.then(res => {
					console.log(res)
					this.articleList = res.data.results
				})
				.catch(e => {
					console.log(e)
				})
			},
			closeModal () {
				this.editDialog = false
			},
		}
	}
</script>

<style lang='scss'>
	.edit_article_list_wrap {
		border-bottom: solid 0.5px #ccc;
	}
</style>
