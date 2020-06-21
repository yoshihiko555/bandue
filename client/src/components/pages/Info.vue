<template>
	<v-app>
		<Header/>
		<div id="info_wrap" class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6' class="px-0">
						Info
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
		name: 'Message',
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

</style>
