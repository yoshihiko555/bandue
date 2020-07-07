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
							<!-- タイトル -->
							<v-text-field
								v-model='articleData.title'
								outlined
								placeholder='Title'
							></v-text-field>

							<!-- 内容 -->
							<v-textarea
								v-model='articleData.content'
								outlined
								placeholder='Content'
								rows='15'
							></v-textarea>

							<v-row>
								<v-col cols='4'>
								<!-- 記事の種類 -->
								<v-select
									v-model='articleData.type'
									:items='entryType'
									item-text='text'
									item-value='value'
									label='Entry Type'
									dense
								></v-select>

								<!-- 都道府県 -->
								<v-select
									v-model='articleData.prefecture'
									:items='prefecture'
									item-text='text'
									item-value='value'
									label='Prefecture'
									dense
								></v-select>

								<!-- 活動の曜日 -->
								<v-select
									v-model='articleData.day_week'
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
									v-model='articleData.direction'
									:items='direction'
									item-text='text'
									item-value='value'
									label='Direction'
									dense
								></v-select>

								<!-- 募集する性別 -->
								<v-select
									v-model='articleData.sex'
									:items='sex'
									item-text='text'
									item-value='value'
									label='Sex'
									dense
								></v-select>

								<!-- 募集する年齢 -->
								<v-select
									v-model='articleData.age'
									:items='age'
									item-text='text'
									item-value='value'
									label='Age'
									dense
									multiple
								></v-select>
								</v-col>

								<v-col cols='4'>
								<!-- 活動エリア -->
								<v-text-field
									v-model='articleData.area'
									label='Area'
									dense
								></v-text-field>

								<!-- 募集パート -->
								<v-text-field
									v-model='articleData.part'
									label='Part'
									dense
								></v-text-field>

								<!-- ジャンル -->
								<v-text-field
									v-model='articleData.genre'
									label='Genre'
									dense
								></v-text-field>
								</v-col>
							</v-row>
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
	import { Const } from '@/static/js/const'

	const Con = new Const()
	export default {
		name: 'CreateArticle',
		components: {

		},
		data: () => ({
			dialog: false,
			isSave: false,
			offset: true,
			articleData: {
				title: '',
				content: '',
				type: 'NO',
				prefecture: 0,
				area: '',
				day_week: 'NO',
				direction: 'NO',
				part: '',
				genre: '',
				sex: 0,
				age: [0],
			},
			entryType: Con.ENTRY_TYPE,
			prefecture: Con.PREFECTURE,
			dayWeek: Con.DAY_WEEK,
			direction: Con.DIRECTION,
			sex: Con.SEX,
			age: Con.AGE,
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
				this.$axios({
					method: 'POST',
					url: '/api/entry/',
					data: this.articleData,
				})
				.then(res => {
					console.log(res.data)
                    this.dialog = false
                    this.initArticleData()
					this.$eventHub.$emit('create-article', res)
				})
				.catch(e => {
					console.log(e.response)
				})
            },
            
            initArticleData () {
                this.articleData = {
                    title: '',
                    content: '',
                    type: 'NO',
                    prefecture: 0,
                    area: '',
                    day_week: 'NO',
                    direction: 'NO',
                    part: '',
                    genre: '',
                    sex: 0,
                    age: [0],
                }
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
