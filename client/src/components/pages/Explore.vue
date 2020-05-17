<template>
	<v-app id="main">
		<Header/>
		<div>
			<v-btn
				to='/signup'
				@click='reload'
			>SignUp</v-btn>
			<v-btn
				to='/signin'
				@click='reload'
			>SignIn</v-btn>
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import { Common } from '@/static/js/common'
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'

	const Com = new Common()

	export default {
		props: [],
		name: 'Explore',
		components: {
			Header,
			Footer
		},
		data: () => ({

		}),

		methods: {
			reload () {
				Com.reload(this.$router)
			}
		}
	}
</script>
