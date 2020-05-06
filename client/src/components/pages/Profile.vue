<template>
	<v-app id='profile'>
		<Header/>
		<div>
			<v-container fluid>
				<v-row>
					<v-col cols='3'>
						<Sidebar/>
					</v-col>

					<v-col cols='6'>
						<v-card
							outlined
						>
							<v-card-text>
								{{ profileData.username }}
							</v-card-text>
							<v-card-text>
								{{ profileData.introduction }}
							</v-card-text>
							<v-card-text>
								{{ profileData.created_at }}
							</v-card-text>
							<v-card-text>
								{{ profileData.followees_count }} Following
								{{ profileData.followers_count }} Followers
							</v-card-text>

							<v-tabs
								grow
							>
								<v-tab>Tweets</v-tab>
								<v-tab>Tweets & replies</v-tab>
								<v-tab>Media</v-tab>
								<v-tab>Likes</v-tab>
							</v-tabs>
						</v-card>
					</v-col>

					<v-col cols='3'>
						<Search/>
					</v-col>
				</v-row>
			</v-container>
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import axios from 'axios'
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Search from '@/components/common/Search'

	export default {
		name: 'Profile',
		components: {
			Header,
			Footer,
			Sidebar,
			Search
		},
		data: () => ({
			profileData: {}
		}),
		mounted: function () {
			const token = this.$session.get('token')
			const username = this.$session.get('username')
			axios.get('http://192.168.33.12:8000/api/profile/' + username , {
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				}
			})
			.then(res => {
				res.data.created_at = res.data.created_at.substr(0, 10)

				this.profileData = res.data
				console.log(res)
			})
			.catch(e => {
				console.log(e)
			})
		}
	}
</script>
