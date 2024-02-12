from rest_framework import routers

from api import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'/users', views.UserViewSet)
router.register(r'/register_user', views.RegisterUserView, basename='register_user')
router.register(r'/modify_user', views.ModifyUserView, basename='modify_user')
router.register(r'/tasks', views.TaskViewSet)
router.register(r'/tasks_history', views.HistoryViewSet, 'history')

urlpatterns = router.urls
