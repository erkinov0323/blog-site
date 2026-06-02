from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

from .models import Category, Post, Comment, Like



class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['first_name', "username", "password", "confirm_password"]


    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
    
        if password != confirm_password:
            raise ValidationError({
                "message":"Parollar bir xil emas"
            })
        
        return attrs
    

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        User.objects.create_user(**validated_data)

        return validated_data



class SigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs["username"]
        password = attrs['password']

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError({
                "message":"Login yoki parol xato",
            })
        
        attrs['user'] = user

        return attrs


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', "username"]




class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']



class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ["id", "title", 'content', 'author', 'category', 'image', 'likes_count', 'comments_count']
    
    def get_likes_count(self, obj):
        return obj.like_set.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id','text', 'post']



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']
    
