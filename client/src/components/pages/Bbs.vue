<template>
	<v-app>
		<Header/>
		<div id='bbs' class="main">
			BBS
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'

	export default {
		name: 'Bbs',
		components: {
			Header,
			Footer
		},
		data: () => ({
		}),
		mounted: function () {

		}
	}
</script>
