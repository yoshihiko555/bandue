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
							@click='SidebarMethods(item)'
						>
							<v-list-item-icon>
								<v-icon v-text='item.icon'></v-icon>
							</v-list-item-icon>
							<v-list-item-content>
								<v-list-item-title v-text=item.title></v-list-item-title>
							</v-list-item-content>

							<v-list-item-action>
								<v-badge
									color='red accent-2'
									:content='item.info_content'
									:value='item.info_content'
								>
								</v-badge>
							</v-list-item-action>

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
	import { Const } from '@/static/js/const'

	const Com = new Common()
	const Con = new Const()

	export default {
		name: 'Sidebar',

		components: {
			SignOut
		},

		data: () => ({
			sidebarItem: 7,
			dialog: false,
			items: [
				{
					icon: 'mdi-home',
					title: 'Home',
					url: '/home',
					info_content: 0,
				},
				{
					icon: 'mdi-file-document-edit',
					title: 'BBS',
					url: '/bbs',
					info_content: 0,
				},
				{
					icon: 'mdi-forum',
					title: 'Message',
					url: '/message',
					info_content: 0,
				},
				{
					icon: 'mdi-information',
					title: 'Info',
					url: '/info',
					info_content: 0,
				},
				{
					icon: 'mdi-account',
					title: 'Profile',
					url: '/profile/',
					info_content: 0,
				},
				{
					icon: 'mdi-cogs',
					title: 'Setting',
					url: '/setting',
					info_content: 0,
				},
				{
					icon: 'mdi-logout-variant',
					title: 'Signout',
					url: '',
					info_content: 0,
				}
			],
		}),

		created () {
			this.$eventHub.$on('cntUpInfo', this.cntUpInfo)
			this.$eventHub.$on('cntDownInfo', this.cntDownInfo)
            this.$eventHub.$on('cntZeroInfo', this.cntZeroInfo)
            this.$eventHub.$on('removeMessageInfo', this.removeMessageInfo)
		},

		mounted: function () {

			const scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
            const url = scheme + '://' + window.location.host + '/ws/user/' + this.$store.state.loginUser + '/'

			this.ws = new WebSocket(url)

			this.ws.onmessage = e => {
				var receiveData = JSON.parse(e.data)
				console.log('ソケット結果受信', receiveData)
				let event = (receiveData.type === Con.WS_TYPE_NOTIFICATION) ? 'Info' : 'Message'
				this.$eventHub.$emit('cntUpInfo', event)
			}

			this.$axios.get('/api/info/getInfoCnt/')
			.then(res => {
				console.log(res)
				this.items[Con.SIDEBAR_INDEX.Info].info_content = res.data.info_count
				this.items[Con.SIDEBAR_INDEX.Message].info_content = res.data.msg_count
			})
			.catch(e => {
				console.log(e)
			})
		},

		methods: {
			SidebarMethods (item) {
				const methodsList = {
					Home: this.reload,				// HOME
					BBS: this.reload,				// BBS
                    Message: this.reload,   		// Message
					Info: this.reload,				// Info
					Profile: this.toProfile,		// Profile
					Setting: this.reload,			// Setting
					Signout: this.togleSignoutModal	// Signout
                }
				if (methodsList[item.title] !== '') {
					// メソッドが定義されている
					methodsList[item.title](item.url)
				}
			},

			togleSignoutModal () {
				this.dialog = !this.dialog
			},

			toProfile (url) {
                this.$router.push({
                    name: 'Profile',
                    params: {
                        username: this.$store.state.loginUser
                    }
                })
				// Com.reload(this.$router)
			},

			reload (url) {
                this.$router.push(url)
				// Com.reload(this.$router)
			},

			cntUpInfo(menu) {
				this.items[Con.SIDEBAR_INDEX[menu]].info_content++
			},

			cntDownInfo(menu) {
				this.items[Con.SIDEBAR_INDEX[menu]].info_content--
			},

			cntZeroInfo(menu) {
				this.items[Con.SIDEBAR_INDEX[menu]].info_content = 0
            },

            removeMessageInfo (cnt) {
                this.items[Con.SIDEBAR_INDEX.Message].info_content -= cnt
            },
		}
	}
</script>
