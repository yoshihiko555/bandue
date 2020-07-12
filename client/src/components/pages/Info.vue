<template>
	<v-app>
		<Header/>
		<div class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6' class="px-0">
						<div v-for='(info, index) in infoList' :key='`infoList-${index}`' class='info_area'>
							<v-card
								flat
								class='info_wrap'
								ref='info_ref'
							>
								<v-card-title
									class='info_title'
								>
								{{ info.pk }}
									<div v-if='info.event === "Liked"'>
										<v-icon
											color='red lighten-1'
										>mdi-heart</v-icon>
									</div>
									<div v-else-if='info.event === "Retweet"'>
										<v-icon
											color='grey lighten-1'
										>mdi-repeat</v-icon>
									</div>
									<v-avatar
									 	v-else
										class='infomation_icon'
									>
										<v-img v-if='info.send_user.icon === null' src='@/static/img/default_icon.jpeg'></v-img>
										<v-img v-else :src=icon></v-img>
									</v-avatar>
								</v-card-title>

								<v-card-text
									class='info_text'
								>
									{{ info.infomation }}
								</v-card-text>
							</v-card>
						</div>
					</v-col>
					<v-col cols='3'>
						<Search/>
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
	import Search from '@/components/common/Search'

	export default {
		name: 'Message',
		components: {
			Header,
			Footer,
			Sidebar,
			Search
		},
		data: () => ({
			infoList: [],
			readedInfoPk: [],
		}),
		created () {

		},
		mounted: function () {

			this.$axios.get('/api/info/')
			.then(res => {
				this.infoList = res.data.results
			})
			.catch(e => {
				console.log(e)
			})

			this.readInfo()

		},
		methods: {
			readInfo () {
				this.$axios.get('/api/info/readInfo/')
				.then(res => {
					this.$eventHub.$emit('cntZeroInfo', 'Info')
				})
				.catch(e => {
					console.log(e)
				})
			}
		}
	}
</script>

<style lang='scss'>
	.info_wrap {
		border-radius: 0 !important;
		border-bottom: solid 0.5px #ccc !important;
		cursor: pointer;
	}

</style>
