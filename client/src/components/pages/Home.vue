<template>
	<v-app v-if='!lodding'>
		<Header/>
		<div id="home" class='main' v-if='!lodding'>
			<div v-if='isAuth'>
				<v-container fluid>
					<v-row>
						<v-col cols='3'>
							<Sidebar/>
						</v-col>

						<v-col cols='6'>
							<Tweet/>
							<TweetList/>
						</v-col>

						<v-col cols='3'>
							<Search/>
						</v-col>
					</v-row>
				</v-container>
			</div>
		</div>

		<div v-if='lodding'>
			<img src="@/static/img/lodding.gif" alt="">
		</div>
		<Footer/>
	</v-app>
</template>

<script>
	import { Common } from '@/static/js/common'
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Tweet from '@/components/common/Tweet'
	import TweetList from '@/components/common/TweetList'
	import Search from '@/components/common/Search'

	const Com = new Common()

	export default {
		props: ['isAuth', 'lodding'],
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

		}),

		methods: {
			reload () {
				Com.reload(this.$router)
			}
		}
	}
</script>
