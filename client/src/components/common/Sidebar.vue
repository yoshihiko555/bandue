<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<v-list>
					<v-list-item-group
						v-model='sidebarItem'
						color='primary'
					>
						<v-list-item
							v-for='(item, i) in items'
							:key='i'
							:to='item.url'
							@click='SidebarMethods(i)'
						>
							<v-list-item-icon>
								<v-icon v-text='item.icon'></v-icon>
							</v-list-item-icon>
							<v-list-item-content>
								<v-list-item-title v-text=item.title></v-list-item-title>
							</v-list-item-content>
						</v-list-item>
					</v-list-item-group>
				</v-list>
			</v-col>
		</v-row>

		<SignOut
			:dialog='dialog'
			@togle-signout-modal='togleSignoutModal'
		>
		</SignOut>
	</v-container>
</template>

<script>
	import SignOut from '@/components/register/SignOut'
	import { Common } from '@/static/js/common'

	const Com = new Common()

	export default {
		name: 'Sidebar',
		components: {
			SignOut
		},
		data: () => ({
			sidebarItem: 7,
			dialog: false,
			username: '',
			items: [
				{
					icon: 'mdi-home',
					title: 'Home',
					url: '/home',
				},
				{
					icon: 'mdi-file-document-edit',
					title: 'BBS',
					url: '/bbs',
				},
				{
					icon: 'mdi-forum',
					title: 'Message',
					url: '/message',
				},
				{
					icon: 'mdi-information',
					title: 'Info',
					url: '',
				},
				{
					icon: 'mdi-account',
					title: 'Profile',
					url: '/profile/',
				},
				{
					icon: 'mdi-cogs',
					title: 'Setting',
					url: '/setting',
				},
				{
					icon: 'mdi-logout-variant',
					title: 'Signout',
					url: '',
				}
			]
		}),

		mounted: function () {
			this.username = this.$store.state.loginUser
		},

		methods: {
			SidebarMethods (i) {
				const methodsList = [
					this.reload,				// HOME
					this.reload,				// BBS
					this.reload,				// Message
					'',							// Info
					this.toProfile,				// Profile
					this.reload,				// Setting
					this.togleSignoutModal		// Signout
				]
				if (methodsList[i] !== '') {
					// メソッドが定義されている
					methodsList[i]()
				}
			},

			togleSignoutModal () {
				this.dialog = !this.dialog
			},

			toProfile () {
				this.$router.push(this.username)
				Com.reload(this.$router)
			},

			reload () {
				Com.reload(this.$router)
			}
		}
	}
</script>
