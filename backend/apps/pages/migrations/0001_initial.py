from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='HomePageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(default='Keruvim Performance', max_length=120)),
                ('hero_title', models.CharField(default='Train like an athlete. Perform like a champion.', max_length=180)),
                ('hero_subtitle', models.TextField(default='Premium coaching programs built for speed, strength, and peak performance.')),
                ('primary_cta_label', models.CharField(default='Shop Programs', max_length=60)),
                ('primary_cta_url', models.CharField(default='/programs', max_length=200)),
                ('support_email', models.EmailField(default='coach@keruvimperformance.com', max_length=254)),
                ('support_phone', models.CharField(default='+254700000000', max_length=40)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
