<template>
	<v-app id="main" v-if='!lodding'>
		<Header/>
			<div v-if='isAuth'>
				<v-container fluid>
					<v-row>
						<v-col cols='3'>
							<Sidebar/>
						</v-col>
						<v-col cols='9'>
							<Tweet/>
							<TweetList/>
						</v-col>
					</v-row>
				</v-container>
			</div>

			<div v-if='!isAuth'>
				<p>ログインして</p>
			</div>
		<Footer/>
	</v-app>
</template>

<script>
	import Header from '@/components/common/Header'
	import Footer from '@/components/common/Footer'
	import Sidebar from '@/components/common/Sidebar'
	import Tweet from '@/components/common/Tweet'
	import TweetList from '@/components/common/TweetList'

	export default {
		props: ['isAuth', 'lodding'],
		name: 'Index',
		components: {
			Header,
			Footer,
			Sidebar,
			Tweet,
			TweetList
		},
		data: () => ({

		})
	}
</script>
