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

    chainWebpack: config => {
        // チャンクの設定
        // チャンク自体まだよくわからない
        config.optimization
            .splitChunks(false)

        // webpak-stats.jsonの出力先を設定
        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../client/webpak-stats.json'}])

        // 開発サーバーの設定
        config.devServer
            .public('http://192.168.33.12:8080')
            .host('192.168.33.12')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["\*"]})
    }
}
