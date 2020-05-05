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
			items: [
				{
					icon: 'mdi-home',
					title: 'Home',
					url: '',
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
					url: '/profile',
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
			],

			dialog: false
		}),

		methods: {
			SidebarMethods (i) {
				const methodsList = [
					'',		// HOME
					this.reload,		// BBS
					this.reload,		// Message
					'',		// Info
					this.reload,		// Profile
					this.reload,		// Setting
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

			reload () {
				console.log('リロード')
				Com.reload(this.$router)
			}
		}
	}
</script>
