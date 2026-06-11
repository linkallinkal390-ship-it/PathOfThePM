from rest_framework import serializers
from .models import User, Result, Session
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            sur_name=validated_data['sur_name'],
        )
    
    class Meta:
            model = User
            fields = ['id', 'email', 'password','first_name', 'sur_name', 'role', 'created_at']
            read_only_fields = ['id', 'created_at']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            request=self.context.get('request'),
            email=data['email'],
            password=data['password'],
        )
        if not user:
            raise serializers.ValidationError('Неверные учетные данные')
        data['user'] = user
        return data
    
    
class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='get_role_display', read_only=True)
    role_code = serializers.CharField(source='role', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'sur_name', 'role', 'role_code', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'sur_name', 'password', 'password_confirm', 'role']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(**validated_data)


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ['id', 'finalConstructionDate']


class SessionSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.SerializerMethodField()
    result_reputation = serializers.IntegerField(source='result.reputation', read_only=True)
    
    class Meta:
        model = Session
        fields = ['id', 'user', 'user_email', 'user_full_name', 'result', 
                 'result_reputation', 'start_date', 'end_date']
        read_only_fields = ['id']
    
    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.sur_name}"


class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['user', 'result', 'start_date', 'end_date']
    
    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({
                'end_date': 'End date must be after start date'
            })
        return data


class SessionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['start_date', 'end_date']
    
    def validate(self, data):
        if 'start_date' in data and 'end_date' in data:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError({
                    'end_date': 'End date must be after start date'
                })
        return data