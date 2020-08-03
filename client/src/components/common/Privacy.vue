<template>
	<div class="privacy_setting_wrap">

		<!-- Privacy設定画面ここから -->
	    <v-container>
	      	<v-list-item-group>
				<v-list-item>
					<v-list-item-content>
						<v-row>
							<v-col cols='10'>
						        <v-list-item-title>Public Level</v-list-item-title>
								<v-spacer></v-spacer>
								<v-list-item-subtitle>Make tweets private</v-list-item-subtitle>
							</v-col>
							<v-col cols='2'>
								<v-switch v-model='settingData.isPrivate' @change='togglePrivate'></v-switch>
							</v-col>
						</v-row>
					</v-list-item-content>
				</v-list-item>
		        <v-list-item
					v-for='(item, i) in settingList'
					:key='i'
					@click='settingListMethod(i, item)'
		        >
					<v-list-item-content>
						<v-row>
							<v-col cols='10'>
								<v-list-item-title v-text='item.text'></v-list-item-title>
							</v-col>
							<v-col cols='2'>
								<v-icon>mdi-chevron-right</v-icon>
							</v-col>
						</v-row>
					</v-list-item-content>
		    	</v-list-item>
			</v-list-item-group>
	    </v-container>
		<!-- Privacy設定画面ここまで -->

		<!-- ミュートしたアカウント一覧ここから -->
	    <v-dialog
			v-model='muteListDialog'
			max-width='600px'
	    >
			<v-card>
		        <v-container
		          fluid
		        >
					<v-row>
						<v-col
							cols='1'
						></v-col>
						<v-col
							cols='10'
							align=center
						>
				  			ミュートしたアカウント
						</v-col>
						<v-col
					  		cols='1'
						>
				  			<v-btn color='teal darken-1' class='white--text' tile depressed icon @click='closeModal'>
					    		<v-icon>mdi-close-octagon</v-icon>
					  		</v-btn>
						</v-col>
					</v-row>
		        </v-container>
			<div v-if='initLoading === false'>
				<div v-if='muteUserList.length > 0'>
					<div v-for='(user, index) in muteUserList' :key='`username-${index}`'>
						<v-card>
							<v-card-title>
								<v-avatar>
									<v-img v-if='user.icon !== "/media/" && user.icon !== null' :src='user.icon'></v-img>
									<v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
								</v-avatar>
									{{ user.username }}
								<v-spacer></v-spacer>
								<span>
									<v-btn
									  icon
									  @click='showUnMuteDialog(user, index)'
									>
								  		<v-icon>mdi-volume-variant-off</v-icon>
									</v-btn>
								</span>
							</v-card-title>
							<v-card-text>{{ user.introduction | truncate(60) }}</v-card-text>
						</v-card>
					</div>
				</div>
				<div v-else>
					<v-card>
					<v-card-title>ミュートしているアカウントは0件です。</v-card-title>
					</v-card>
				</div>
	        </div>
	        <div v-else>
				<v-container>
					<Loading></Loading>
				</v-container>
	        </div>
			</v-card>
		</v-dialog>
		<!-- ミュートしたアカウント一覧ここまで -->

		<!-- ブロックしたアカウント一覧ここから -->
	    <v-dialog
			v-model='blockListDialog'
			max-width='600px'
	    >
			<v-card>
				<v-container
					fluid
				>
					<v-row>
						<v-col
							cols='1'
							></v-col>
						<v-col
							cols='10'
							align=center
						>
							ブロックしたアカウント
						</v-col>
						<v-col
							cols='1'
						>
							<v-btn color='teal darken-1' class='white--text' tile depressed icon @click='closeModal'>
								<v-icon>mdi-close-octagon</v-icon>
							</v-btn>
						</v-col>
					</v-row>
				</v-container>
			<div v-if='initLoading === false'>
				<div v-if='blockUserList.length > 0'>
					<div v-for='(user, index) in blockUserList' :key='`username-${index}`'>
						<v-card>
							<v-card-title>
								<v-avatar>
									<v-img v-if='user.icon !== "/media/" && user.icon !== null' :src='user.icon'></v-img>
									<v-img v-else src='@/static/img/default_icon.jpeg'></v-img>
								</v-avatar>
								{{ user.username }}
								<v-spacer></v-spacer>
								<span>
									<v-btn
										icon
										@click='showUnBlockDialog(user, index)'
									>
										<v-icon>mdi-account-cancel</v-icon>
									</v-btn>
								</span>
							</v-card-title>
						<v-card-text>{{ user.introduction | truncate(60) }}</v-card-text>
						</v-card>
					</div>
				</div>
				<div v-else>
					<v-card>
						<v-card-title>ブロックしているアカウントは0件です。</v-card-title>
					</v-card>
				</div>
			</div>
			<div v-else>
				<v-container>
					<Loading></Loading>
				</v-container>
			</div>
			</v-card>
	    </v-dialog>
		<!-- ブロックしたアカウント一覧ここまで -->

		<!-- ミュートを解除するモーダルここから -->
	    <v-dialog
			v-model='unMuteDialog'
			max-width='400px'
	    >
			<v-card>
				<v-container fluid>
					<v-card-title>ミュートを解除しますか？</v-card-title>
					<v-row>
						<v-col
							cols='6'
							align=center
						>
							<v-btn
								text
								@click='unMute'
							>はい</v-btn>
						</v-col>
						<v-col
							cols='6'
							align=center
						>
							<v-btn
								text
								@click='unMuteDialog = false'
							>いいえ</v-btn>
						</v-col>
					</v-row>
				</v-container>
			</v-card>
	    </v-dialog>
		<!-- ミュートを解除するモーダルここまで -->

		<!-- ブロックを解除するモーダルここから -->
	    <v-dialog
			v-model='unBlockDialog'
			max-width='400px'
	    >
			<v-card>
				<v-container fluid>
					<v-card-title>ブロックを解除しますか？</v-card-title>
					<v-row>
						<v-col
							cols='6'
							align=center
						>
							<v-btn
								text
								@click='unBlock'
							>はい</v-btn>
						</v-col>
						<v-col
							cols='6'
							align=center
						>
							<v-btn
								text
								@click='unBlockDialog = false'
							>いいえ</v-btn>
						</v-col>
					</v-row>
				</v-container>
			</v-card>
	    </v-dialog>
		<!-- ブロックを解除するモーダルここまで -->

	</div>
</template>

<script>
    import { mapState } from 'vuex'
    import Loading from '@/components/common/Loading'

    export default {
		name: 'Privacy',

	    data: () => ({
			settingList: [
				{
					text: 'Mute List'
				},
				{
					text: 'Block List'
				}
			],
			muteListDialog: false,
			blockListDialog: false,
			unMuteDialog: false,
			unBlockDialog: false,
			muteUserList: [],
			blockUserList: [],
			selectUser: [],
			selectUserIndex: 0,
			initLoading: true,
			settingData: []
	    }),

	    components: {
			Loading,
	    },

		mounted: function () {
			const loginUser = this.$store.state.loginUser
			this.$axios.get('/api/profile/' + loginUser + '/')
			.then(res => {
			    console.log(res)
			    this.settingData = res.data.setting
			})
			.catch(e => {
				console.log(e.response)
			})
		},

		methods: {
			// 設定リスト毎のメソッド
			settingListMethod (i, item) {
				let settingListMethodList = [
					this.showMuteList,
					this.showBlockList,
				]
				settingListMethodList[i](item)
			},

			// ミュートリストを表示するメソッド
			showMuteList (item) {
				console.log('showMuteList')
				this.$axios({
					method: 'POST',
					url: '/api/users/muteList/',
				})
				.then(res => {
					console.log(res)
					this.muteUserList = res.data
				})
				.catch(e => {
					console.log(e)
				})
				this.initLoading = false
				this.muteListDialog = true
			},

			// ブロックリストを表示するメソッド
			showBlockList (item) {
				console.log('showBlockList')
				this.$axios({
					method: 'POST',
					url: '/api/users/blockList/',
				})
				.then(res => {
					console.log(res)
					this.blockUserList = res.data
				})
				.catch(e => {
					console.log(e)
				})
				this.initLoading = false
				this.blockListDialog = true
			},

			closeModal () {
				this.muteListDialog = false
				this.blockListDialog = false
				this.unMuteDialog = false
				this.unBlockDialog = false
				this.initLoading = true
			},

			showUnMuteDialog (user, index) {
				this.selectUserIndex = index
				this.selectUser = user
				this.unMuteDialog = true
			},

			showUnBlockDialog (user, index) {
				this.selectUserIndex = index
				this.selectUser = user
				this.unBlockDialog = true
			},

			// ミュートを解除するメソッド
			unMute () {
				this.unMuteDialog = false
				this.$axios({
					method: 'POST',
					url: 'api/users/unMute/',
					data: {
						target_user: this.selectUser.username
					}
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
				this.muteUserList.splice(this.selectUserIndex, 1)
			},

			// ミュートをブロックするメソッド
			unBlock () {
				this.unBlockDialog = false
				this.$axios({
					method: 'POST',
					url: 'api/users/unBlock/',
					data: {
						target_user: this.selectUser.username
					}
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
				this.blockUserList.splice(this.selectUserIndex, 1)
			},

			// ツイート非公開の設定を変更するメソッド
			togglePrivate () {
				console.log('togglePrivate')
				this.$axios({
					url: 'api/setting/' + this.settingData.id + '/',
					method: 'PUT',
					data: this.settingData
				})
				.then(res => {
					console.log(res)
				})
				.catch(e => {
					console.log(e)
				})
			}
	    },
	}
</script>

<style lang="scss">
</style>
