# Generated migration file

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0002_alter_engineeringqa_category'),
    ]

    operations = [
        # Add new field BEFORE renaming
        migrations.AddField(
            model_name='engineeringqa',
            name='source_url',
            field=models.URLField(blank=True, null=True, help_text='Where this information was sourced from'),
        ),
        
        # Rename EngineeringQA to RUGIPOKnowledge
        migrations.RenameModel(
            old_name='EngineeringQA',
            new_name='RUGIPOKnowledge',
        ),
        
        # Create ScraperURL model
        migrations.CreateModel(
            name='ScraperURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True, help_text='Website URL to scrape')),
                ('is_active', models.BooleanField(default=True, help_text='Enable/disable scraping for this URL')),
                ('scrape_frequency', models.CharField(
                    max_length=50,
                    default='daily',
                    choices=[
                        ('daily', 'Daily'),
                        ('weekly', 'Weekly'),
                        ('manual', 'Manual Only'),
                    ]
                )),
                ('last_scraped', models.DateTimeField(null=True, blank=True, help_text='Last time this URL was scraped')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('notes', models.TextField(blank=True, help_text='Notes about this source')),
            ],
            options={
                'verbose_name': 'Scraper URL',
                'verbose_name_plural': 'Scraper URLs',
            },
        ),
    ]
