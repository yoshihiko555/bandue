<template>
	<v-app>
		<Header/>
		<div id="message_wrap" class="main">
			Message
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'

	export default {
		name: 'Message',
		data: () => ({
		}),
		mounted: function () {

		}
	}
</script>
