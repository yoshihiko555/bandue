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
					<th class="text-left">EMail</th>
					<td>{{ data.email }}</td>
				</tr>
				<tr>
					<th class='text-left'>Password</th>
					<td>{{ data.password }}</td>
				</tr>
			</tbody>
			</template>
		</v-simple-table>
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
      console.log('入力情報',this.data)
      // axios.defaults.xsrfCookieName = 'csrftoken'
      // axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
      this.$axios.post('api/signup/', this.data)
        .then(res => {
          console.log(res)
		  // サインアップ後は、認証完了の状態にするだけでいい？
          this.$axios.post('auth/', this.data)
            .then(res => {
              console.log(res)
              // this.$session.start()
              // this.$session.set('token', res.data.token)
			  // this.$session.set('username', JSON.parse(res.config.data).username)
			  // 認証データの設定
			  this.$store.commit('setToken', { res: res.data, req:res.requestData })
              this.$emit('signup-change-view', Con.SIGNUP_DONE_VIEW)
            })
            .catch(e => {
              console.log(e)
            })
        })
        .catch(e => {
          console.log(e)
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
