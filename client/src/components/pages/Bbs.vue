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
								<v-expansion-panels accordion tile flat multiple focusable class='mt-3'>
									<v-expansion-panel
										v-for='(article, i) in articleList'
										:key='i'
										class='article_wrap'
										color='orange'
										@click='open(article)'
									>

										<v-expansion-panel-header>
											<v-row>
												<v-col cols='8'>
													<span class='font-weight-black'>{{ article.title }}</span>
												</v-col>
												<v-col cols='4'>
													<span class="font-weight-thin">{{ article.author }}</span>
												</v-col>
											</v-row>
										</v-expansion-panel-header>

										<v-expansion-panel-content class="blue-grey lighten-5">
											<v-row class='article_content_border'>
												<v-col cols='12'>
													<v-card-subtitle class="font-weight-black">記事の内容</v-card-subtitle>
													<v-card-text>
														{{ article.content }}
													</v-card-text>
												</v-col>
											</v-row>

											<v-row class='article_content_border'>
												<v-col cols='4'>
													<v-card-subtitle class="font-weight-black">記事の種類</v-card-subtitle>
													<v-card-text>
														{{ article.type_disp }}
													</v-card-text>
												</v-col>
												<v-col cols='4'>
													<v-card-subtitle class="font-weight-black">都道府県</v-card-subtitle>
													<v-card-text>
														{{ article.prefecture_disp }}
													</v-card-text>
												</v-col>
												<v-col cols='4'>
													<v-card-subtitle class="font-weight-black">活動エリア</v-card-subtitle>
													<v-card-text>
														{{ article.area }}
													</v-card-text>
												</v-col>
												<v-col cols='4'>
													<v-card-subtitle class="font-weight-black">活動曜日</v-card-subtitle>
													<v-card-text>
														{{ article.day_week_disp }}
													</v-card-text>
												</v-col>
												<v-col cols='4'>
													<v-card-subtitle class="font-weight-black">活動方向性</v-card-subtitle>
													<v-card-text>
														{{ article.direction_disp }}
													</v-card-text>
												</v-col>
											</v-row>

											<v-row class='article_content_border'>
												<v-col cols='6'>
													<v-card-subtitle class="font-weight-black">パート</v-card-subtitle>
													<v-card-text>
														{{ article.part }}
													</v-card-text>
												</v-col>
												<v-col cols='6'>
													<v-card-subtitle class="font-weight-black">ジャンル</v-card-subtitle>
													<v-card-text>
														{{ article.genre }}
													</v-card-text>
												</v-col>
											</v-row>

											<v-row>
												<v-col cols='6'>
													<v-card-subtitle class="font-weight-black">募集性別</v-card-subtitle>
													<v-card-text>
														{{ article.sex_disp }}
													</v-card-text>
												</v-col>
												<v-col cols='6'>
													<v-card-subtitle class="font-weight-black">募集年齢</v-card-subtitle>
													<v-card-text v-for='(age, i) in article.age_disp' :key='i'>
														<span>{{ age }}</span>
													</v-card-text>
												</v-col>
											</v-row>
										</v-expansion-panel-content>
									</v-expansion-panel>
								</v-expansion-panels>
							</v-tab-item>
						</v-tabs-items>
					</v-col>

					<v-col cols='3'>
						<!-- TODO 記事検索フォーム -->
                        <!-- 入力フォームのダークモード -->
						<v-text-field
							prepend-inner-icon='mdi-magnify'
						>
						</v-text-field>

						<CreateArticle></CreateArticle>
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
			articleList: []
		}),
		created () {
			this.$eventHub.$on('create-article', this.articleUpdate)
		},
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
			articleUpdate (res) {
				console.log('記事更新')
				this.articleList = res.data.results
			},

			open (article) {
				// 既読機能用メソッド
				console.log('open')
				this.$axios({
					url: 'api/entry/isRead/',
					method: 'POST',
					data: article,
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
			},

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

	.article_wrap {
		> button {
			border-bottom: solid 0.5px #ccc;
		}
		.v-expansion-panel-header__icon {
			display: none;
		}

		.v-expansion-panel-content {
			background-color: #fefefe;
		}

		.article_content_border {
			border-bottom: solid 0.5px #fff;
		}
	}
</style>
