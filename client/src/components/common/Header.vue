<template>
	<v-container id='header_wrap'>
		<v-row>
			<v-col cols='12'>
				<h1 class='logo'>Bandue</h1>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
	export default {
		data: () => ({

		}),
		methods: {

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
	}
}
</style>
