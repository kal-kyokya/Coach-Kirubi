from django.db import models
from django.utils.text import slugify


class Program(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    DELIVERY_FORMAT_CHOICES = [
        ('pdf', 'PDF Guide'),
        ('video', 'Video Library'),
        ('hybrid', 'Hybrid'),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    short_description = models.CharField(max_length=280)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_weeks = models.PositiveIntegerField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    delivery_format = models.CharField(max_length=20, choices=DELIVERY_FORMAT_CHOICES)
    thumbnail_url = models.URLField(blank=True)
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
