class GetLoginUserMixin:
    """
    Getで来たログインユーザーの名前を取得するメソッド
    Viewsetなどで継承して使う
    """

    def get_login_user(self):
        return self.login_user if hasattr(self, 'login_user') else None
