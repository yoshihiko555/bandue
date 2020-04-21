<template>
	<v-container fluid>
		<v-row>
			<v-col cols='12'>
				<div v-for='tweet in tweetList' :key='tweet.author'>
					<v-card
					>
						<v-card-title>
							{{ tweet.author }}
							<span class='ml-8' style="font-size:50%;">{{ tweet.updated_at }}</span>
						</v-card-title>

						<v-card-text>
							{{ tweet.content }}
						</v-card-text>

						<v-card-actions>
							<v-list-item>
								<v-list-content v-for='tag in tweet.hashTag' :key='tag.title'>
									<v-list-item-title>{{ tag.title }}</v-list-item-title>
								</v-list-content>
								<v-row
									align='center'
									justify='end'
								>
									<v-icon class='mr-1' color='red lighten-1'>mdi-heart</v-icon>
									<span class='mr-2'>{{ tweet.liked }}</span>
								</v-row>
							</v-list-item>
						</v-card-actions>
					</v-card>
				</div>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TweetList',
  data: () => ({
    tweetList: {}
  }),
  mounted: function () {
    axios.get('http://192.168.33.12:8000/api/tweet/')
      .then(res => {
        console.log(res)
        for (var i in res.data) {
          var updatedAt = res.data[i].updated_at.substr(0, 10)
          console.log(updatedAt)
          res.data[i].updated_at = updatedAt
        }
        this.tweetList = res.data
        console.log(this.tweetList)
      })
      .catch(e => {
        console.log(e)
      })
  }
}
</script>
