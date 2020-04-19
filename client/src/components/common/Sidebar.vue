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
								<v-list-item-title v-text='item.title'></v-list-item-title>
							</v-list-item-content>
						</v-list-item>
					</v-list-item-group>
				</v-list>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: 'Sidebar',
	data: () => ({
		sidebarItem: 7,
		items: [
			{
				icon: 'mdi-home',
				title: 'Home',
				url: '/'
			},
			{
				icon: 'mdi-file-document-edit',
				title: 'BBS',
				url: '/'
			},
			{
				icon: 'mdi-forum',
				title: 'Message',
				url: '/'
			},
			{
				icon: 'mdi-information',
				title: 'info',
				url: '/'
			},
			{
				icon: 'mdi-account',
				title: 'Profile',
				url: '/'
			},
			{
				icon: 'mdi-cogs',
				title: 'Setting',
				url: '/'
			},
			{
				icon: 'mdi-logout-variant',
				title: 'Signout',
				url: '/'
			}
		]
	})
}
</script>
