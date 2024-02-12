from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from api.models import Task
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    history = serializers.HyperlinkedRelatedField(read_only=True, view_name='history-detail', many=True)

    class Meta:
        model = Task
        fields = ['url', 'name', 'desc', 'status', 'user', 'history']


class HistorySerializer(serializers.Serializer):
    id = serializers.HyperlinkedRelatedField(read_only=True, view_name='task-detail')
    history_date = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(max_length=16, read_only=True)
    desc = serializers.CharField(max_length=256, read_only=True)
    status = serializers.CharField(max_length=11, read_only=True)
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')
