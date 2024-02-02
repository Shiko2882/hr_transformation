# Generated by Django 4.2.9 on 2024-02-02 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr_admin', '0010_alter_company_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='organizational_people',
        ),
        migrations.AddField(
            model_name='company',
            name='organizational',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='people',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='ceo',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Chief Executive Officer'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_address',
            field=models.TextField(blank=True, null=True, verbose_name='Company Address'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_contacts_numbers',
            field=models.TextField(blank=True, null=True, verbose_name='Company Contact Numbers'),
        ),
        migrations.AlterField(
            model_name='company',
            name='company_website',
            field=models.URLField(blank=True, null=True, verbose_name='Company Website'),
        ),
        migrations.AlterField(
            model_name='company',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='General Background'),
        ),
        migrations.AlterField(
            model_name='company',
            name='gm',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='General Manager'),
        ),
        migrations.AlterField(
            model_name='company',
            name='industry',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Company Industry'),
        ),
        migrations.AlterField(
            model_name='company',
            name='market',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Market'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True, verbose_name='Company Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='official_social_media_pages',
            field=models.TextField(blank=True, null=True, verbose_name='Official Social Media Pages'),
        ),
        migrations.AlterField(
            model_name='company',
            name='social_facebook',
            field=models.URLField(blank=True, null=True, verbose_name='Facebook'),
        ),
        migrations.AlterField(
            model_name='company',
            name='social_instagram',
            field=models.URLField(blank=True, null=True, verbose_name='Instagram'),
        ),
        migrations.AlterField(
            model_name='company',
            name='social_linkedin',
            field=models.URLField(blank=True, null=True, verbose_name='LinkedIn'),
        ),
        migrations.AlterField(
            model_name='company',
            name='social_website',
            field=models.URLField(blank=True, null=True, verbose_name='Website'),
        ),
    ]
