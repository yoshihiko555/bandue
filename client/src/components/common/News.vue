<template>
    <div class='news_wrap'>
        <div v-for='(article, i) in article' :key='i'>
            <v-card>
                <v-img :src=article.urlToImage></v-img>
                <v-card-title>{{ article.title }}</v-card-title>
                <v-card-text>
                    {{ article.content }}
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
        name: 'News',
        data: () => ({
            article: null,
        }),
        mounted () {
            axios({
                url: 'http://newsapi.org/v2/top-headlines?' +
                     'country=us&' +
                     'apiKey=' + process.env.VUE_APP_NEWS_API,
                method: 'GET',
            })
            .then(res => {
                console.log(res)
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
    }
</style>
