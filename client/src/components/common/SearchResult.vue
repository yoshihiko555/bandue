<template>
  <div class='search_result_wrap'>
    <v-tabs
      v-model='searchTabModel'
      class='search_tab_wrap'
      centered
      fixed-tabs
      color='light-blue lighten-4'
    >
      <v-tab
        v-for='(tab, i) in SearchTabList'
        :key='i'
        :href='`#tab-${i}`'
        @click='tabChange(tab, i)'
      >
        {{ tab }}
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model='searchTabModel'>
      <v-tab-item
        v-for='(tab, i) in SearchTabList'
        :key='i'
        :value="'tab-' + i"

      >
        <div v-if='loading'>
          <Loading></Loading>
        </div>
        <div v-else>
          <div v-if='i != 2'>
            <div v-if='tweetList.length > 0'>
              <div v-for='(tweet, index) in tweetList' :key='`tweet.author-${index}`'>
                <v-card
                  flat
                  class='tweet_wrap'
                >
                <v-card-title>
                  <span
                    class='tweet_author z10'
                  >{{ tweet.author }}</span>
                  <span class='ml-8' style='font-size:50%;'>{{ tweet.updated_at }}</span>
                  <span v-if='tweet.isRetweeted'>
                    <v-icon
                      class='mr-1 retweet'
                      color='green lighten-1'
                    >mdi-repeat</v-icon>
                    リツイート済み
                  </span>
                </v-card-title>

                <!-- 内容 -->
                <v-card-text>
                  {{ tweet.content }}
                </v-card-text>

                <div>
        					<img :src='tweet.images' width="100">
        				</div>
        				<v-card-actions>
        					<v-list-item>
        						<v-list-item-content v-for='tag in tweet.hashTag' :key='tag.title'>
        							<v-list-item-title>{{ tag.title }}</v-list-item-title>
        						</v-list-item-content>

        						<v-row
        							align='center'
        							justify='end'
        						>
        							<retweet :tweet=tweet :index=index></retweet>
        							<like :tweet=tweet :index=index></like>
        						</v-row>
        					</v-list-item>
        				</v-card-actions>

                </v-card>
              </div>
            </div>

            <div v-else>
              <v-card
                flat
                class='tweet_not_found_wrap'
              >
                <v-card-title
                  class='tweet_not_found'
                >
                  ツイートが見つかりません。
                </v-card-title>
              </v-card>
            </div>
          </div>

          <div v-else>
            <div v-if='userList.length > 0'>

              <div v-for='(user, index) in userList' :key='`user.username-${index}`'>
                <v-card
                  flat
                  class='user_wrap'
                >
                  <v-card-title>
                    <span
                      class='username z10'
                    >{{ user.username }}</span>
                    <span class='ml-8'>
                      <follow :username='user.username'></follow>
                    </span>
                  </v-card-title>
                  <v-card-text>
                    {{ user.introduction }}
                  </v-card-text>
                </v-card>
              </div>
            </div>
            <div v-else>
              <v-card
                flat
                class='user_not_found_wrap'
              >
                <v-card-title>
                  ユーザーが見つかりません。
                </v-card-title>
              </v-card>
            </div>
          </div>

        </div>

      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>

import Retweet from '@/components/common/Retweet'
import Like from '@/components/common/Like'
import Follow from '@/components/common/Follow'
import Loading from '@/components/common/Loading'

export default {
  name: 'SearchResult',
  props: {
    'searchText': {
      type: String,
      required: true
    }
  },
  components: {
    Retweet,
    Like,
    Follow,
    Loading,
  },
  data: () => ({
    searchTabModel: null,
    SearchTabList: [
      'Trand',
      'New',
      'User',
      'Media'
    ],
    tweetList: [],
    userList: [],
    searchFlg: 0,
    loading: true,
  }),
  watch: {

	},
  created () {
    this.$watch(
      () => [this.searchFlg, this.searchText], (val) => {
        console.log('searchFlg, searchText => ' + val)
        this.search(...val)
      }
    )
  },
  mounted: function () {
    this.search(this.searchFlg, this.searchText)
  },
  methods: {
    tabChange (tab, i) {
      this.searchFlg = i
    },
    search (searchFlg, searchText) {
      this.loading = true
      this.$axios.get('api/search/', {
        params: {
          searchFlg: searchFlg,
          searchText: searchText
        }
      })
      .then(res => {
        if (this.searchFlg !== 2) {
          for (var i in res.data) {
            var updatedAt = res.data[i].updated_at.substr(0, 10)
            res.data[i].updated_at = updatedAt
          }
          this.tweetList = res.data
          console.log('ツイート一覧', this.tweetList)
          this.loading = false
        } else {
          this.userList = res.data
          console.log('ユーザー一覧', this.userList)
          this.loading = false
        }
      })
      .catch(e => {
        console.log(e)
        this.loading = false
      })
    },

  }
}

</script>

<style lang='scss'>
  .tweet_wrap {
    cursor: pointer;

    .tweet_author {
      position: relative;

    }
  }
</style>
