from rest_framework import mixins
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import NotAcceptable, NotAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from .models import Category, Article, Comment, Image, NestedComment
from . import serializers
from .serializers_user import UserSerializer
import os
# from rest_framework.pagination import PageNumberPagination


def intro(request):
    url = ""
    with open(os.getcwd() + '/api/urls.py', 'r') as data:
        for line in data:
            if "path(" in line:
                url += line
    return render(request, 'intro.html', {"urls": url})


class WhoAmIView(APIView):
    def get(self, request, format=None):
        try:
            user = User.objects.get(pk=request.user.pk)
        except User.DoesNotExist:
            return Response({"detail": "You are not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content',  'title', 'author__username']
    # pagination_class = PageNumberPagination  # handle at settings

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ArticleListSerializer
        else:
            return serializers.ArticleCreateSerializer


class ArticleEditUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    lookup_field = 'slug'
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        return serializers.ArticleDetailSerializer if self.request.method == 'GET' else serializers.ArticleCreateSerializer


class CommentCreateView(mixins.CreateModelMixin, generics.RetrieveAPIView):
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ArticleDetailSerializer
        return serializers.CommentCreateSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return Article.objects.all()
        return Comment.objects.all()

    def perform_create(self, serializer):
        try:
            article = Article.objects.get(slug=self.kwargs.get("slug"))
        except Article.DoesNotExist:
            raise NotAcceptable(
                detail="You're trying to comment to an unknown article"
            )
        user = self.request.user
        serializer.save(user=user, article=article)

    def post(self, request, slug, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentEditUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    lookup_field = 'slug'
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CommentDetailSerializer
        return serializers.CommentCreateSerializer


class ImageCreateView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = serializers.ImageCreateSerializer
    permission_classes = [DjangoModelPermissions]

    def perform_create(self, serializer):
        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        image = self.request.FILES.getlist('image')
        for im in image:
            img = Image(image=im, article=article)
            img.save()

    def get(self, request, *args, **kwargs):
        return Response({"detail": "Only recieves POST of image for an article"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ImageEditUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    lookup_field = 'slug'
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ImageDetailSerializer
        return serializers.ImageCreateSerializer


class NestedCommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.NestedCommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        parent = get_object_or_404(Comment, slug=self.kwargs.get("slug"))
        user = self.request.user
        serializer.save(user=user, parent=parent)


class NestedCommentEditUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NestedComment.objects.all()
    lookup_field = 'slug'
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.NestedCommentDetailSerializer
        return serializers.NestedCommentCreateSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategoryListCreateSerializer
    permission_classes = [IsAdminUser]


@api_view(['POST'])
def post_like_view(request, slug):
    if not request.user.is_authenticated:
        return Response({"detail": "You are not authenticated!"}, status=status.HTTP_401_UNAUTHORIZED)
    article = get_object_or_404(Article, slug=slug)
    if request.user in article.like.all():
        article.like.remove(request.user)
        return Response({"detail": "Unlike successful"}, status=status.HTTP_201_CREATED)
    else:
        article.like.add(request.user)
        return Response({"detail": "Like is successful"})
    return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
