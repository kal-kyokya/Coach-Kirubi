from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True)),
                ('short_description', models.CharField(max_length=280)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('duration_weeks', models.PositiveIntegerField()),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('delivery_format', models.CharField(choices=[('pdf', 'PDF Guide'), ('video', 'Video Library'), ('hybrid', 'Hybrid')], max_length=20)),
                ('thumbnail_url', models.URLField(blank=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['-is_featured', '-created_at']},
        ),
    ]
