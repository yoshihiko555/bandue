<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<v-list>
					<v-list-item-group v-model='sidebarItem' color='primary'>
						<v-list-item
							v-for='(item, i) in items'
							:key='i'
						>
							<v-list-item-icon>
								<v-icon v-text='item.icon'></v-icon>
							</v-list-item-icon>
							<v-list-item-content>
								<v-list-item-action
									@click=changeView(item.no)
								>
									<v-list-item-title v-text='item.title'></v-list-item-title>
								</v-list-item-action>
							</v-list-item-content>
						</v-list-item>
					</v-list-item-group>
				</v-list>
			</v-col>
		</v-row>

		<SignOut
			:dialog='dialog'
		>
		</SignOut>
	</v-container>
</template>

<script>
import SignOut from '@/components/register/SignOut'
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
				url: '/',
				no: 1
			},
			{
				icon: 'mdi-file-document-edit',
				title: 'BBS',
				url: '/',
				no: 2
			},
			{
				icon: 'mdi-forum',
				title: 'Message',
				url: '/',
				no: 3
			},
			{
				icon: 'mdi-information',
				title: 'info',
				url: '/',
				no: 4
			},
			{
				icon: 'mdi-account',
				title: 'Profile',
				url: '/',
				no: 5
			},
			{
				icon: 'mdi-cogs',
				title: 'Setting',
				url: '/',
				no: 6
			},
			{
				icon: 'mdi-logout-variant',
				title: 'Signout',
				url: '/',
				no: 7
			}
		],

		dialog: false
	}),

	methods: {
		changeView (no) {
			if (no === 7) {
				this.dialog = true
			} else {

			}
		}
	}
}
</script>
