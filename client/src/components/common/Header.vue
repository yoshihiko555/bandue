<template>
	<v-container id='header_wrap'>
		<v-row>
			<v-col cols='12'>
				<router-link to='/'><h1 class='logo'><img src='@/static/img/Logo_Icon&Text.png' alt="logo" width="150"></h1></router-link>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		data: () => ({

		}),
		methods: {
			// reload () {
			// 	Com.reload(this.$router)
			// }
		}
	}
</script>

<style lang='scss'>
	#header_wrap {
		padding: 0;

		height: $header;

		.logo{
			padding-left: 2%;
			font-size: 22px;

			a {
				color: $default-color;
				text-decoration: blink;
			}
		}
	}
</style>
