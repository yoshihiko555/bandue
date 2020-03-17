const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
    transpileDependencies: [
        'vuetify'
    ],
    // ローカルサーバーのIP設定
    devServer: {
      port: 8080,
      host: '192.168.33.12',
    },
    // serverで展開する
    outputDir: '../server',
    // サーバーを起動したときのルートパス
    publicPath: '/',
    // outputDir起点で、index.htmlを格納する場所
    indexPath: 'templates/index.html',
    // outputDir起点で、staticファイルを格納する場所
    assetsDir: 'static'
}
