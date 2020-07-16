class GetLoginUserMixin:
    """
    Getで来たログインユーザーの名前を取得するメソッド
    Viewsetなどで継承して使う
    """

    def set_login_user(self, request):
        if 'loginUser' in request.query_params:
            self.login_user = request.query_params['loginUser']


    def get_login_user(self):
        return getattr(self, 'login_user', None)
