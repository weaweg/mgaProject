from django.contrib.auth.models import Group, User
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.models import Task
from api.serializers import UserSerializer, TaskSerializer, HistorySerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class RegisterUserView(ViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post']

    def create(self, request):
        request.data['is_staff'] = False
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


class ModifyUserView(ViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch', 'delete']

    def list(self, request):
        return JsonResponse({})

    def patch(self, request):
        if request.data['username'] != request.user.username:
            raise PermissionDenied("You can't change another user profile")
        user = User.objects.get(username=request.data['username'])
        serializer = self.serializer_class(user, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=200)

    def delete(self, request, pk=None):
        User.objects.get(username=request.data['username']).delete()
        return JsonResponse({"detail": "User deleted"}, status=204)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def __permissionDenied(self, request):
        if not request.user.is_staff or request.user.is_superuser:
            raise PermissionDenied("You don't have permissions")

    def create(self, request, *args, **kwargs):
        self.__permissionDenied(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.__permissionDenied(request)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.__permissionDenied(request)
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status is not None:
            queryset = queryset.filter(status=status)
        username = self.request.query_params.get('user')
        if username is not None:
            try:
                user = User.objects.get(username=username)
                if user is not None:
                    queryset = queryset.filter(user)
            except User.DoesNotExist:
                return queryset.none()
        search = self.request.query_params.get('search')
        if search is not None:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(desc__icontains=search)
        return queryset


class HistoryViewSet(ModelViewSet):
    queryset = Task.history.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.request.user)
        queryset = super().get_queryset()
        task = self.request.query_params.get('task')
        if task is not None:
            queryset = queryset.filter(id=task)
        return queryset


def custom400(request, exception=None):
    return custom_error(request, "Bad request", 400)


def custom403(request, exception=None):
    return custom_error(request, "Forbidden", 403)


def custom404(request, exception=None):
    return custom_error(request, "Not found", 404)


def custom500(request, exception=None):
    return custom_error(request, "Server error", 500)


def custom_error(request, message, status):
    path = request.build_absolute_uri()
    return JsonResponse({"messsage": message, "url": path}, status=status)
