"""
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.static import serve

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from .views import *
aguncn_router = DefaultRouter()

# category的url
aguncn_router.register(r'sprints', views.SprintViewSet, base_name='sprints')
aguncn_router.register(r'tasks', views.TaskViewSet, base_name='tasks')
aguncn_router.register(r'users', views.UserViewSet, base_name='users')