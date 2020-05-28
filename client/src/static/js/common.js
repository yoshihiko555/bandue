class Common {
    // 共通メソッドはこのクラスで管理
    init () {
        console.log('OK')
    }

    reload (router) {
        router.go({
            path: router.currentRoute.path, force: true
        })
    }
}

export { Common }
