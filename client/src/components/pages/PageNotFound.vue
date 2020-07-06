<template>
	<v-app>
		<Header/>
		<div id="page_not_found_wrap" class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6' class="px-0">
						<v-card
							flat
						>
							<v-card-title
								class='page_not_found_title'
								text-h2
							>
								404
							</v-card-title>
							<v-card-text
								class='page_not_found_text'
								text-h2
							>
								お探しのページは見つかりませんでした
							</v-card-text>
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

	export default {
		name: 'PageNotFound',
		components: {
			Header,
			Footer,
			Sidebar,
		},
		data: () => ({
		}),
		mounted: function () {
		},
		methods: {
		}
	}
</script>

<style lang='scss'>
	#page_not_found_wrap {

		.page_not_found_title {
			margin-top: 50px;
			font-size: 4em;
		}

		.page_not_found_text {
			margin-top: 25px;
			font-size: 2em;
		}
	}
</style>
