<template>
	<v-container id="footer_wrap">
		<v-row>
			<v-col>
				<small>bandue</small>
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
#footer_wrap {
	padding: 0;
	height: $footer;

	small {
		float: right;
		padding-right: 2%;
	}
}
</style>
