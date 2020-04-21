<template>
	<v-card
		class='pa-3'
		outlined
	>
		<v-card-title>
			<h1 class="register_title" val='Testデータ'>BandueにSignUpする</h1>
		</v-card-title>

		<!-- v-model='valid'で、入力項目のvalidationがすべてOKになったらtrueになる。
		それまではvalidはfalse -->
		<v-form ref='form' v-model='valid'>
			<!-- v-modelでデータとの紐付け
			:rulesでscript内で設定したValidationとの紐付け
			:idでpropsで親コンポーネント側からデータを紐付ける
			今回の場合の親コンポーネントは、Djangoテンプレート側 -->
			<v-text-field
				v-model='credentials.username'
				:rules='rules.username'
				:counter='70'
				maxlength='70'
				label='UserName'
				required
				clearable
				tabindex='1'
			></v-text-field>

			<v-text-field
				v-model='credentials.email'
				:rules='rules.email'
				:counter='70'
				maxlength='70'
				label='Mail'
				required
				clearable
				tabindex='2'
			></v-text-field>

			<v-text-field
				v-model='credentials.password'
				:rules='rules.password'
				:counter='70'
				maxlength='70'
				label='Password'
				required
				clearable
				tabindex='3'
			></v-text-field>

			<v-col class='text-center' cols='12'>
				<v-btn
					depressed
					x-large
					class='teal lighten-4 ma-1'
					:disabled='!valid'
					@click='confirm'
					tabindex='4'
				>次へ</v-btn>
			</v-col>
		</v-form>
	</v-card>
</template>

<script>
import { Const } from '@/static/js/const'

const Con = new Const()

export default {
  name: 'signup',
  data: () => ({
    valid: true,
    loading: false,
    credentials: {},
    msg: 'メッセージ',
    rules: {
      username: [
        v => !!v || '必須項目です',
        v => (v && v.length <= 70) || '70文字以内で入力してください'
      ],
      email: [
        v => !!v || '必須項目です'
      ],
      password: [
        v => !!v || '必須項目です',
        v => (v && v.length >= 8 && v.length <= 70) || '8文字以上、70文字以内で入力してください'
        // v => //.test(v) || '半角英数字を1文字以上含めてください'		// TODO: 正規表現後で考える
      ]
    }
  }),
  methods: {
    confirm () {
      this.$emit('signup-change-view', Con.SIGNUP_CONFRIM_VIEW, this.credentials)
    }
  }
}
</script>

<style lang='scss'>

</style>
