<template>
	<v-app>
		<Header/>
		<div id='bbs_wrap' class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6'>
						<v-tabs
							v-model='bbsTabModel'
							grow
							class='bbslist_tab_wrap'
						>
							<v-tab
								v-for='(tab, i) in BbsTabList'
								:key='i'
								:href='`#tab-${i}`'
							>
								{{ tab }}
							</v-tab>
						</v-tabs>

						<v-tabs-items v-model='bbsTabModel'>
							<v-tab-item
								v-for='(tab, i) in BbsTabList'
								:key='i'
								:value="'tab-' + i"
							>
							<div v-for='(article, i) in articleList' :key='i'>
								<v-card
									flat
									class='article_wrap'
								>
									<v-card-title>
										{{ article.title }}
									</v-card-title>

									<v-card-text>
										{{ article.content }}
									</v-card-text>

									<v-card-text>
										{{ article.writer }}
									</v-card-text>
								</v-card>
							</div>
							</v-tab-item>
						</v-tabs-items>
					</v-col>

					<v-col cols='3'>
						<!-- TODO 記事検索フォーム -->
						<v-text-field
							prepend-inner-icon='mdi-magnify'
						>
						</v-text-field>

						<CreateArticle></CreateArticle>

						<!-- TODO 人気タグ表示 -->
						<v-card
							flat
							outlined
							tile
							class='mb-3 pa-3'
							min-height='250px'
						>
							<v-card-title class='pa-2'>人気タグ</v-card-title>
							<v-divider class="mx-3"></v-divider>
							<v-chip-group
								column
							>
								<v-chip
									v-for='tag in tags'
									:key='tag'
									@click='tag'
								>
									{{ tag }}
								</v-chip>
							</v-chip-group>
						</v-card>

						<v-card
							tile
							outlined
							class='pa-2'
							min-height='250px'
						>
							<v-card-title class='pa-2'>カテゴリー</v-card-title>
							<v-divider class="mx-3"></v-divider>

							<v-list
							>
								<v-list-item
									v-for='category in categorys'
									:key='category'
									@click='category'
								>
									<v-list-item-content>
										<v-list-item-title v-text='category'></v-list-item-title>
									</v-list-item-content>
								</v-list-item>
							</v-list>

						</v-card>
					</v-col>
				</v-row>
			</v-container>
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import CreateArticle from '@/components/common/CreateArticle'
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'Bbs',
		components: {
			Header,
			Footer,
			Sidebar,
			CreateArticle
		},
		data: () => ({
			bbsTabModel: null,
			BbsTabList: [
				'人気記事',
				'新着記事'
			],
			tags: [
				'tag1',
				'tag2',
				'tag3',
				'tag4'
			],
			categorys: [
				'category1',
				'category2',
				'category3',
				'category4'
			],
			articleList: []
		}),
		mounted: function () {
			this.$axios({
				method: 'GET',
				url: '/api/bbs/'
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
			tag () {
				console.log('タグをクリック')
			},

			category () {
				console.log('カテゴリーをクリック')
			},
			reload () {
				Com.reload(this.$router)
			},
		}
	}
</script>

<style lang='scss'>
	.bbslist_tab_wrap {
		border-bottom: solid 1px #ccc !important;
	}
</style>
