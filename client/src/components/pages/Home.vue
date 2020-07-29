<template>
	<v-app>
		<Header/>
		<div id="home_wrap" class='main' v-show='!lodding'>
			<div v-if='isAuth'>
				<v-container fluid>
					<v-row>
						<v-col cols='3'>
							<Sidebar/>
						</v-col>

						<v-col cols='6'>
							<Tweet/>
							<TweetList
								:tweet-list-flg=4
							></TweetList>
						</v-col>

						<v-col cols='3'>
							<Search/>
						</v-col>
					</v-row>
				</v-container>
			</div>
		</div>

		<div v-show='lodding'>
			<img src="@/static/img/lodding.gif" alt="">
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import { Common } from '@/static/js/common'
	import { Const } from '@/static/js/const'
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Tweet from '@/components/common/Tweet'
	import TweetList from '@/components/common/TweetList'
	import Search from '@/components/common/Search'

	const Com = new Common()
	const Con = new Const()

	export default {
		name: 'Index',
		components: {
			Header,
			Footer,
			Sidebar,
			Tweet,
			TweetList,
			Search
		},
		data: () => ({
			isAuth: false,
	    lodding: true,
			ws: null,
		}),
		mounted: function () {
		  this.isAuth = this.$store.state.isAuth
      this.lodding = false

      if (!this.isAuth) {
          this.$router.push('/signin')
          Com.reload(this.$router)
      }
			const url = 'ws://' + window.location.host + '/ws/user/' + this.$store.state.loginUser + '/'
			this.ws = new WebSocket(url)

			this.ws.onmessage = e => {
				var receiveData = JSON.parse(e.data)
                console.log('ソケット結果受信', receiveData)
                let event = (receiveData.type === Con.WS_TYPE_NOTIFICATION) ? 'Info' : 'Message'
				this.$eventHub.$emit('cntUpInfo', event)
			}
    },
		methods: {
			reload () {
				Com.reload(this.$router)
			}
		}
	}
</script>
