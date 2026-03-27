from django.db import models


class HomePageContent(models.Model):
    brand_name = models.CharField(max_length=120, default='Keruvim Performance')
    hero_title = models.CharField(max_length=180, default='Train like an athlete. Perform like a champion.')
    hero_subtitle = models.TextField(default='Premium coaching programs built for speed, strength, and peak performance.')
    primary_cta_label = models.CharField(max_length=60, default='Shop Programs')
    primary_cta_url = models.CharField(max_length=200, default='/program')
    support_email = models.EmailField(default='coach@keruvimperformance.com')
    support_phone = models.CharField(max_length=40, default='+254700000000')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Homepage Content'
