<template>
	<v-app>
		<Header/>
		<div id="message_wrap" class="main">
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='3' class="px-0">
						<v-row align='center'>
							<v-col cols='8'>
								<v-text-field
									prepend-inner-icon='mdi-magnify'
								></v-text-field>
							</v-col>

							<v-col cols='4'>
								<NewRoom/>
							</v-col>
						</v-row>

						<v-list>
							<v-list-item
								v-for='(room, i) in rooms'
								:key='i'
								@click='showRoom(room.id, room.room_name)'
                                v-show='room.users.length !== 0'
							>
								<v-list-item-content>
									<v-list-item-title v-text='room.room_name'></v-list-item-title>
								</v-list-item-content>

                                <!-- Message編集ボタン -->
                                <v-menu bottom left>
                                    <template v-slot:activator='{ on }'>
                                        <v-btn
                                            dark
                                            icon
                                            v-on='on'
                                            color='grey'
                                        >
                                            <v-icon>mdi-dots-vertical</v-icon>
                                        </v-btn>
                                    </template>

                                    <v-list>
                                        <v-list-item @click='deleteRoom(room)'>
                                            <v-list-item-title>削除</v-list-item-title>
                                        </v-list-item>
                                    </v-list>
                                </v-menu>
							</v-list-item>
						</v-list>
					</v-col>

					<v-col cols='6' class="px-0">
						<MessageBox
							ref='messageBox'
						></MessageBox>
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
	import MessageBox from '@/components/common/MessageBox'
	import NewRoom from '@/components/common/NewRoom'

	export default {
		name: 'Message',
		components: {
			Header,
			Footer,
			Sidebar,
			MessageBox,
			NewRoom,
		},
		data: () => ({
			rooms: {},
        }),
        created () {
			this.$eventHub.$on('create-room', this.roomsUpdate)
		},
		mounted: function () {
			const loginUser = this.$store.state.loginUser
			this.$axios({
				method: 'GET',
				url: '/api/room/',
				params: {
					loginUser: loginUser
				},
			})
			.then(res => {
                console.log('ルーム一覧',res.data)
				this.rooms = res.data
			})
			.catch(e => {
				console.log(e)
			})
		},
		methods: {
			showRoom (id, roomName) {
				this.$refs.messageBox.showMessage(id, roomName)
            },
            roomsUpdate (res) {
                console.log(res)
                this.rooms = res.data
            },
            deleteRoom (room) {
                this.$axios({
                    url: `/api/room/${room.id}/delete_room/`,
                    method: 'PUT',
                    data: room
                })
                .then(res => {
                    console.log(res)
                })
                .catch(e => {
                    console.log(e)
                })
            },
		}
	}
</script>

<style lang='scss'>

</style>
