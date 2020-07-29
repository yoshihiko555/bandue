<template>
	<v-app>
		<Header/>
		<div id="setting_wrap" class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='3'>
						<v-list dense>
							<v-subheader>設定</v-subheader>
							<v-list-item-group v-model='settingModel' color='primary' value="true">
								<v-list-item
									v-for='(item, i) in settingList'
									:key='i'
									@click='changePage(i)'
								>
									<v-list-item-content>
										<v-list-item-title v-text='item.text'></v-list-item-title>
									</v-list-item-content>
								</v-list-item>
							</v-list-item-group>
						</v-list>
					</v-col>

					<v-col cols='6'>
						<component
							:is='currentPage'
						></component>
					</v-col>
				</v-row>
			</v-container>
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import AcountSetting from '@/components/common/AcountSetting'
	import SystemSetting from '@/components/common/SystemSetting'
	import BbsSetting from '@/components/common/BbsSetting'
	import Privacy from '@/components/common/Privacy'

	export default {
		name: 'Setting',
		components: {
			Header,
			Footer,
			Sidebar,
			AcountSetting,
			SystemSetting,
			BbsSetting,
			Privacy,
		},
		data: () => ({
			settingPage: 0,
			pageList: [
				AcountSetting,
				SystemSetting,
				BbsSetting,
				Privacy,
			],
			settingModel: 0,		// 使わない？
			settingList: [			// 使わない？
				{
					text: 'AcountSetting',
					icon: ''
				},
				{
					text: 'SystemSetting',
					icon: ''
				},
				{
					text: 'BbsSetting',
					icon: ''
				},
				{
					text: 'Privacy'
				}
			],
			acountSettingList: [
				{
					text: 'Profile',
					icon: 'mdi-account'
				},
				{
					text: 'Password',
					icon: 'mdi-lock-question'
				}
			]
		}),

		mounted: function () {

		},

		computed: {
			currentPage () {
				return this.pageList[this.settingPage]
			}
		},

		methods: {
			changePage (no) {
				this.settingPage = no
			},
		}
	}
</script>
