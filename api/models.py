from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.shortcuts import reverse
from django.dispatch import receiver
import random
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_slug(self):
        return self.name[:10]


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)
    title = models.CharField(
        max_length=100, verbose_name='title', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    featured = models.BooleanField(default=False, blank=True)
    like = models.ManyToManyField(
        User, related_name="liker", default=None, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    date_modified = models.DateTimeField(auto_now_add=True)
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-date_modified',)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.title

    def get_slug(self):
        return self.content[:10]

    @property
    def get_comments(self):
        return self.comment_set.all().order_by('-date_created')

    @property
    def get_images(self):
        return self.articleImage.all().order_by('-date_created')

    @property
    def comment_count(self):
        return Comment.objects.filter(article=self).count()


class Comment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    slug = models.SlugField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_slug(self):
        return self.comment[:10]

    def __str__(self):
        return f'{self.comment[:20]}... by {self.user.username}'

    @property
    def get_nested_comments(self):
        return self.commentNestedComment.all().order_by('-date_created')


class NestedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        Comment, related_name='commentNestedComment', on_delete=models.CASCADE)
    comment = models.TextField()
    slug = models.SlugField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment[:20]}... by {self.user.username}'

    def get_slug(self):
        return self.comment[:10]


class Image(models.Model):
    article = models.ForeignKey(
        Article, related_name='articleImage', on_delete=models.CASCADE)
    caption = models.CharField(max_length=300, blank=True)
    slug = models.SlugField(unique=True, blank=True, db_index=True)
    image = models.ImageField(
        blank=True, upload_to=f'article/%Y/%m/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.article.content[0:10]} image '

    def get_slug(self):
        return random.randint(1, 9)

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    picture = models.ImageField(
        upload_to='author/', default="default.png", blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        if self.picture:
            self.picture.delete()
        super().delete(*args, **kwargs)


def create_author(sender, instance, created, *args, **kwargs):
    if created:
        Author.objects.create(user=instance)


post_save.connect(create_author, sender=User)


@receiver(pre_save, sender=Category)
@receiver(pre_save, sender=Article)
@receiver(pre_save, sender=Comment)
@receiver(pre_save, sender=NestedComment)
@receiver(pre_save, sender=Image)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.get_slug())
        while sender.objects.filter(slug=instance.slug).exists():
            instance.slug += slugify(random.randint(0, 9))
        return instance.slug
