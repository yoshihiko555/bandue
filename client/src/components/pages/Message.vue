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
                                    v-model="searchText"
								></v-text-field>
							</v-col>

							<v-col cols='4'>
								<NewRoom/>
							</v-col>
						</v-row>
                        <div v-if="loading">
                            <Loading/>
                        </div>

                        <div v-else>
                            <v-list v-if="!showSearchList">
                                <v-list-item
                                    v-for='(room, i) in rooms'
                                    :key='i'
                                    @click='showRoom(room)'
                                >
                                    <v-list-item-content>
                                        <v-list-item-title v-text='room.room_name'></v-list-item-title>
                                    </v-list-item-content>

                                    <v-list-item-action>
                                        <v-badge
                                            color='red accent-2'
                                            :content='room.msg_count'
									        :value='room.msg_count'
                                        >
                                        </v-badge>
                                    </v-list-item-action>

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
                            <v-list v-else>
                                <div v-if="searchRoom.length > 0">
                                    <v-list-item
                                        v-for='(room, i) in searchRoom'
                                        :key='i'
                                        @click='showRoom(room.id, room.room_name)'
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
                                </div>
                                <div v-else>
                                    <v-card-title>部屋が見つかりません</v-card-title>
                                </div>
                            </v-list>
                        </div>
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
    import Loading from '@/components/common/Loading'
    import _ from 'lodash'
    import { Const } from '@/static/js/const'

    const Con = new Const()

	export default {
		name: 'Message',
		components: {
			Header,
			Footer,
			Sidebar,
			MessageBox,
			NewRoom,
            Loading,
		},
		data: () => ({
            rooms: [],
            searchRoom: [],
            searchText: '',
            showSearchList: false,
            loading: false,
        }),
        watch: {
            searchText (val) {
                if (val) {
                    this.loading = true
                    this.search(val)
                } else {
                    this.loading = false
                    this.showSearchList = false
                }
            }
        },
        created () {
			this.$eventHub.$on('create-room', this.roomsUpdate)
			this.$eventHub.$on('clear-cnt', this.clearCount)
		},
		mounted () {
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
			showRoom (room) {
				this.$refs.messageBox.showMessage(room)
            },
            roomsUpdate (res) {
                console.log(res)
                if (res.status === Con.HTTP_STATUS_CREATED) this.rooms.unshift(res.data)
                this.showRoom(res.data.id, res.data.room_name)
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
            search: _.debounce(function search(searchText) {
                // 空白削除し、カンマ区切りの文字列で送る
                var trimedText = this.trim(searchText)
                var trimedTextList = [...new Set(trimedText.split(/\s+/))]
                var searchWord = trimedTextList.join(',')
                console.log('検索文字列 : ' + searchWord)
                this.$axios.get('api/room/', {
                    params: {
                        searchText: searchWord
                    }
                })
                .then(res => {
                    console.log(res.data)
                    this.searchRoom = res.data
                    this.showSearchList = true
                    this.loading = false
                })
                .catch(e => {
                    console.log(e)
                    this.loading = false
                })
            }, 200),
            trim (word) {
                return String(word).replace(/^\s+|\s+$/g, '')
            },
            clearCount (room, cnt) {
                console.log(room)
                room.msg_count = 0
                this.$eventHub.$emit('removeMessageInfo', cnt)
            }
		}
	}
</script>

<style lang='scss'>

</style>
