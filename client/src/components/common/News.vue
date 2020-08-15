<template>
    <div class='news_wrap'>
        <div v-for='(article, i) in article' :key='i'>
            <v-card>
                <a :href='article.url' target="blank">
                    <v-img v-show='article.urlToImage !== null' :src="article.urlToImage" alt='article.title'></v-img>
                </a>

                <a :href='article.url' target='blank'>
                	<v-card-title>{{ article.title | truncate(30)}}</v-card-title>
                </a>
                <v-card-text>
                    {{ article.description | truncate(60) }}
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'News',
        data: () => ({
            article: null,
        }),
        mounted () {
            this.$axios({
                url: '/api/news/',
                method: 'GET',
            })
            .then(res => {
                console.log(res)
                // ImageのNull対策
                for (var data of res.data.articles) {
                    data.urlToImage = data.urlToImage || ''
                }
                this.article = res.data.articles
            })
            .catch(e => {
                console.log(e)
            })
        },
    }
</script>

<style lang='scss'>
    .news_wrap {
        height: 690px;
        overflow: auto;

        a {
        	text-decoration: none;
    		color: $default-color !important;
        }
    }
</style>
