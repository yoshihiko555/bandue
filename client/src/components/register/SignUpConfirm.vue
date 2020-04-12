<template>
	<v-card
		class='pa-3'
		outlined
		width=368.8
		height=314
	>
		<v-card-title>
			<h1 class="register_title">確認画面</h1>
		</v-card-title>

		<v-simple-table>
			<template v-slot:default>
			<tbody>
				<tr>
					<th class="text-left">Name</th>
					<td>{{ data.username }}</td>
				</tr>
				<tr>
					<th class='text-left'>Password</th>
					<td>{{ data.password }}</td>
				</tr>
			</tbody>
			</template>
		</v-simple-table>
		<p>上記の内容でよろしいですか？</p>
		<v-form ref='form'>
			<v-col class='text-center' cols='12'>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-3'
					@click='back'
				>戻る</v-btn>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-3'
					@click='signup'
				>SignUp</v-btn>
			</v-col>
		</v-form>
	</v-card>
</template>

<script>
	import axios from 'axios'
	import { Const } from '@/static/js/const'

	const Con = new Const()
	export default {
		props: ['data'],
		name: 'signup-conf',
		data: () => ({
			valid: true,
			loading: false
		}),
		methods: {
			signup () {
				console.log(this.data)
				axios.post('http://192.168.33.12/auth/', this.data)
				.then(res => {
					console.log(res)
					this.$emit('signup-change-view', Con.SIGNUP_DONE_VIEW)
				})
				.catch(e => {
					console.log(e)
					this.$emit('signup-change-view', Con.SIGNUP_DONE_VIEW)
				})
			},
			back () {
				this.$emit('signup-change-view', Con.SIGNUP_VIEW)
			}
		}
	}
</script>

<style lang='scss'>

</style>
