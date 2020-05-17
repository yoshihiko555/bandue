const path = require('path')
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    transpileDependencies: [
        'vuetify'
    ],

    // publicPathはdjango-webpack-loaderがパスをbundleにリダイレクトしたときに
    // http://192.168.33.12:8080/http://192.168.33.12:8080みたいに意味不明なURLを生み出さないための回避策
    publicPath: 'http://192.168.33.12:8080',

    // ビルド先のディレクトリの設定
    outputDir: './bundles/',
    assetsDir: 'static',

    pages: {
        // MPAのための設定
        // それぞれのページ毎にエントリーポイントを設定している
        isAuth: {
            entry: 'src/entry/isAuth.js',
            template: 'public/index.html',
            filename: 'isAuth.html'
        },
        home: {
            entry: 'src/entry/main.js',
            template: 'public/index.html',
            filename: 'home.html'
        },
        explore: {
            entry: 'src/entry/explore.js',
            template: 'public/index.html',
            filename: 'explore.html'
        },
        register: {
            entry: 'src/entry/register.js',
            template: 'public/index.html',
            filename: 'register.html'
        },
        bbs: {
            entry: 'src/entry/bbs.js',
            template: 'public/index.html',
            filename: 'bbs.html'
        },
        message: {
            entry: 'src/entry/message.js',
            template: 'public/index.html',
            filename: 'message.html'
        },
        profile: {
            entry: 'src/entry/profile.js',
            template: 'public/index.html',
            filename: 'profile.html'
        },
        setting: {
            entry: 'src/entry/setting.js',
            template: 'public/index.html',
            filename: 'setting.html'
        }
    },

    css: {
        loaderOptions: {
            scss: {
                // 生のCSSを吐き出さないファイルの指定
                // 主にmixinやvariableなどのファイル
                prependData: '@import "./src/static/scss/prepends.scss";'
            }
        }
    },

    chainWebpack: config => {
        // チャンクの設定
        // チャンク自体まだよくわからない
        config.optimization
        .splitChunks(false)

        // webpak-stats.jsonの出力先を設定
        config
        .plugin('BundleTracker')
        .use(BundleTracker, [{ filename: '../client/webpak-stats.json' }])

        // 開発サーバーの設定
        config.devServer
        // .allowedHosts([
        //     '192.168.33.12:8080',
        //     '192.168.33.13:8080',
        // ])
        .public('http://192.168.33.12:8080')
        .host('192.168.33.12')
        .port(8080)
        .hotOnly(true)
        .watchOptions({ poll: 1000 })
        .https(false)
        .headers({ 'Access-Control-Allow-Origin': ['\*'] })

        config.resolve.alias
        // 完全ビルドにすることで、Django側でVueコンポーネントを使用可能にする
        .set('vue$', 'vue/dist/vue.esm.js')
    }
}
