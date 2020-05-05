<template>
	<v-app>
		<Header/>
		Profile
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'

	export default {
		name: 'Profile',
		data: () => ({
			profileData: {}
		}),
		mounted: function () {

		}
	}
</script>
