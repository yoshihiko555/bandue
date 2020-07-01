<template>
	<v-dialog
		v-model='dialog'
		width=300
        :dark='this.$store.state.settings.isDark'
	>
		<template #activator='{ on }'>
			<v-btn icon @click='getUsers' v-on='on'>
				<v-icon>mdi-chat-plus</v-icon>
			</v-btn>
		</template>

		<v-card>
			<v-container fluid>
				<v-row align='center'>
					<v-col cols='12'>
						<v-card-title class='pa-0 d-inline-block'>New Message</v-card-title>
						<v-btn icon @click='dialog = false' class='float-right'>
							<v-icon>mdi-close-octagon</v-icon>
						</v-btn>
					</v-col>
				</v-row>
				<v-text-field
					prepend-inner-icon='mdi-magnify'
				></v-text-field>
				<v-list>
					<v-list-item
						v-for='(user, i) in users'
						:key='i'
						@click='newRoom(user.username)'
					>
						<v-list-item-content>
							<v-list-item-title v-text='user.username'></v-list-item-title>
						</v-list-item-content>
					</v-list-item>
				</v-list>
			</v-container>
		</v-card>
	</v-dialog>
</template>

<script>
	export default {
		name: 'NewRoom',
		data: () => ({
			dialog: false,
			users: {},
		}),
		methods: {
			getUsers () {
				// フォローユーザー一覧取得
				var loginUser = this.$store.state.loginUser
				this.$axios({
					method: 'GET',
					url: '/api/profile/' + loginUser + '/',
				})
				.then(res => {
					console.log(res)
					this.users = res.data.followees
				})
				.catch(e => {
					console.log(e)
				})
			},
			newRoom (member) {
				console.log('新規メッセージ作成')
				console.log('メンバー：' + member)
				var loginUser = this.$store.state.loginUser
				this.$axios({
					method: 'POST',
					url: '/api/room/',
					data: {
						name: member,
						loginUser: loginUser
					},
				})
				.then(res => {
					console.log(res)
					this.dialog = false
				})
				.catch(e => {
					console.log(e)
				})
			},
		}
	}
</script>
