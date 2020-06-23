class GetLoginUserMixin:

    def get_login_user(self):
        return self.login_user if hasattr(self, 'login_user') else None