<template>
	<div></div>
</template>

<script>
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'IsAuth',
		data: () => ({

		}),
		mounted: function () {
			this.$session.start()
			if (this.$session.has('token')) {
				// HOMEへ
				this.$router.push('/home')
				Com.reload(this.$router)
			} else {
				// 未認証ページへ
				this.$router.push('/explore')
				Com.reload(this.$router)
			}
		},

		methods: {

		}
	}
</script>
