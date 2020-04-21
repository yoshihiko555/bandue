<template>
	<v-container id='header_wrap'>
		<v-row>
			<v-col cols='12'>
				<h1 class='logo' @click='reload'><router-link to='/'>Bandue</router-link></h1>
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
    reload () {
      Com.reload(this.$router)
    }
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
			color: #333;
			text-decoration: blink;
		}
	}
}
</style>
