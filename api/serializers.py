from rest_framework import serializers
from .models import Category, Article, Comment, Image, NestedComment
from django.shortcuts import reverse


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('content', 'title', 'category')


class NestedCommentDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    update_url = serializers.SerializerMethodField()

    def get_update_url(self, obj):
        return reverse('nested-comment-detail', kwargs={'slug': obj.slug})

    def get_user_name(self, obj):
        return obj.user.username

    def get_user_image(self, obj):
        if obj.user.author.picture:
            return obj.user.author.picture.url
        else:
            return None

    class Meta:
        model = NestedComment
        fields = ('comment', 'user_name', 'user_image',
                  'date_created', 'update_url', )


class CommentDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    update_url = serializers.SerializerMethodField()
    all_nested_comment = serializers.SerializerMethodField()
    add_nested_comment = serializers.SerializerMethodField()

    def get_all_nested_comment(self, obj):
        return NestedCommentDetailSerializer(obj.get_nested_comments, many=True).data

    def get_update_url(self, obj):
        return reverse('comment-detail', kwargs={'slug': obj.slug})

    def get_add_nested_comment(self, obj):
        return reverse('nested-comment-create', kwargs={'slug': obj.slug})

    def get_user_name(self, obj):
        return obj.user.username

    def get_user_image(self, obj):
        if obj.user.author.picture:
            return obj.user.author.picture.url
        else:
            return None

    class Meta:
        model = Comment
        fields = ('comment', 'user_name', 'user_image',
                  'date_created', 'update_url', 'all_nested_comment', 'add_nested_comment', )


class ImageDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        else:
            return None

    class Meta:
        model = Image
        fields = ('caption', 'slug', 'date_created', 'image_url')


class ArticleListSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)
    like = serializers.StringRelatedField(many=True)
    author_image = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='article-detail', lookup_field='slug')

    def get_author_image(self, obj):
        if obj.author.author.picture:
            return obj.author.author.picture.url
        else:
            return None

    def get_author_name(self, obj):
        return obj.author.username

    class Meta:
        model = Article
        fields = ('title', 'content', 'featured', 'author_name', 'author_image',
                  'slug', 'date_modified', 'date_created',  'category', 'like',  'detail_url')


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.StringRelatedField(many=True)
    like = serializers.StringRelatedField(many=True)
    author_image = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_url = serializers.HyperlinkedIdentityField(
        view_name='comment-create', lookup_field='slug')
    add_image = serializers.HyperlinkedIdentityField(
        view_name='image-create', lookup_field='slug')

    def get_author_image(self, obj):
        if obj.author.author.picture:
            return obj.author.author.picture.url
        else:
            return None

    def get_author(self, obj):
        return obj.author.username

    def get_all_comments(self, obj):
        return CommentDetailSerializer(obj.get_comments, many=True).data

    def get_all_images(self, obj):
        return ImageDetailSerializer(obj.get_images, many=True).data

    class Meta:
        model = Article
        fields = ('title',  'content', 'featured', 'author', 'author_image',
                  'slug', 'date_modified', 'date_created', 'category', 'like', 'all_comments', 'all_images', 'comment_url', 'add_image')


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['comment', ]


class ImageCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ("image", 'caption', )


class NestedCommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NestedComment
        fields = ['comment', ]


class CategoryListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
