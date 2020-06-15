<template>
	<div class="">
		BbsSetting
	</div>
</template>

<script>
	export default {
		name: 'BbsSetting',
		data: () => ({
			articleList: []
		}),

		mounted: function () {
			this.$axios({
				method: 'GET',
				url: '/api/bbs/'
			})
			.then(res => {
				console.log('記事一覧', res.data)
				this.articleList = res.data
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {

		}
	}
</script>
