from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "slug", "description"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Public registration serializer.
    - Creates a User with hashed password.
    - Optionally assigns a Role by slug.
    """

    password = serializers.CharField(write_only=True, required=True)
    role = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Role.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]

    def validate_password(self, value):
        validate_password(value)
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", None)
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)

        if role:
            user.role = role

        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Basic login using username + password.
    """

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid username or password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """
    Read-only serializer for normal responses (login, /me, etc.).
    Includes user_code + nested role.
    """

    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "user_code", "username", "email", "role"]
        read_only_fields = ["id", "user_code", "role"]


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Admin-only serializer used in UserViewSet.

    - View & edit users.
    - Set role via slug.
    - Optionally update password.
    """

    role = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Role.objects.all(),
        required=False,
        allow_null=True,
    )
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_null=True,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "id",
            "user_code",
            "username",
            "email",
            "role",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
        ]
        read_only_fields = ["id", "user_code"]

    def validate_password(self, value):
        if value:
            validate_password(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)

        user = User(**validated_data)

        if password:
            user.set_password(password)

        if role:
            user.role = role

        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        role = validated_data.pop("role", None)

        # update basic fields
        for attr, val in validated_data.items():
            setattr(instance, attr, val)

        # update role if provided (can be set to None)
        if role is not None:
            instance.role = role

        # update password if provided
        if password:
            instance.set_password(password)

        instance.save()
        return instance
