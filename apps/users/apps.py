from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = u'用户管理'

    # 加载进来相关的users apps里面的信号量
    def ready(self):
        import users.signals
