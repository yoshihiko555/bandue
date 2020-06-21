<template>
	<v-dialog v-model='editDialog' fullscreen hide-overlay transition="dialog-bottom-transition">
		<v-card>
			<v-container fluid>
				<!-- ヘッダー -->
				<v-row class="edit_article_title_wrap">
					<v-card-title class="">記事を編集する</v-card-title>
					<v-spacer></v-spacer>
					<v-btn color="teal darken-1" class='white--text edit_article_close_btn' tile depressed icon @click="closeModal">
						<v-icon>mdi-close-octagon</v-icon>
					</v-btn>
				</v-row>

				<!-- コンテンツ -->
				<v-row>
					<v-col cols='12'>
						<v-form>
							<!-- タイトル -->
							<v-text-field
								v-model='article.title'
								outlined
								placeholder='Title'
							></v-text-field>

							<!-- 内容 -->
							<v-textarea
								v-model='article.content'
								outlined
								placeholder='Content'
								rows='15'
							></v-textarea>

							<v-row>
								<v-col cols='4'>
								<!-- 記事の種類 -->
								<v-select
									v-model='article.type'
									:items='entryType'
									item-text='text'
									item-value='value'
									label='Entry Type'
									dense
								></v-select>

								<!-- 都道府県 -->
								<v-select
									v-model='article.prefecture'
									:items='prefecture'
									item-text='text'
									item-value='value'
									label='Prefecture'
									dense
								></v-select>

								<!-- 活動の曜日 -->
								<v-select
									v-model='article.day_week'
									:items='dayWeek'
									item-text='text'
									item-value='value'
									label='Day Week'
									dense
								></v-select>
								</v-col>

								<v-col cols='4'>
								<!-- 活動の方向性 -->
								<v-select
									v-model='article.direction'
									:items='direction'
									item-text='text'
									item-value='value'
									label='Direction'
									dense
								></v-select>

								<!-- 募集する性別 -->
								<v-select
									v-model='article.sex'
									:items='sex'
									item-text='text'
									item-value='value'
									label='Sex'
									dense
								></v-select>

								<!-- 募集する年齢 -->
								<v-select
									v-model='article.age'
									:items='age'
									item-text='text'
									item-value='value'
									label='Age'
									dense
								></v-select>
								</v-col>

								<v-col cols='4'>
								<!-- 活動エリア -->
								<v-text-field
									v-model='article.area'
									label='Area'
									dense
								></v-text-field>

								<!-- 募集パート -->
								<v-text-field
									v-model='article.part'
									label='Part'
									dense
								></v-text-field>

								<!-- ジャンル -->
								<v-text-field
									v-model='article.genre'
									label='Genre'
									dense
								></v-text-field>
								</v-col>
							</v-row>
						</v-form>
					</v-col>
				</v-row>

				<!-- フッター -->
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn v-show='isSave' color="teal darken-1" class='white--text' tile depressed @click="save">下書き</v-btn>
					<v-btn v-show='!isSave' color="teal darken-1" class='white--text' tile depressed @click="update">更新</v-btn>
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
								<v-list-item-title>更新</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</v-card-actions>

			</v-container>
		</v-card>
	</v-dialog>
</template>

<script>
	import { Const } from '@/static/js/const'

	const Con = new Const()
	export default {
		name: 'EditArticle',
		props: ['editDialog', 'article'],
		data: () => ({
			isSave: false,
			offset: true,
			entryType: Con.ENTRY_TYPE,
			prefecture: Con.PREFECTURE,
			dayWeek: Con.DAY_WEEK,
			direction: Con.DIRECTION,
			sex: Con.SEX,
			age: Con.AGE,
		}),

		mounted () {

		},

		methods: {
			save () {
				console.log('下書き')
				this.closeModal()
			},

			update () {
				console.log('更新')
				console.log(this.article)
				this.$axios({
					method: 'PUT',
					url: '/api/entry/' + this.article.id + '/',
					data: this.article,
				})
				.then(res => {
					console.log(res)
					this.closeModal()
				})
				.catch(e => {
					console.log(e)
				})
			},
			closeModal () {
				this.$emit('closeModal')
			},
		}
	}
</script>

<style lang='scss'>
	.edit_article_title_wrap {
		align-items: center;

		.edit_article_close_btn {
			position: absolute;
			right: 1%;
		}
	}
	.drop_up_btn {
		border-left: solid 1px #ccc !important;
	}
</style>
