from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'

    # 加载进来相关的users apps里面的信号量
    def ready(self):
        import posts.signals
