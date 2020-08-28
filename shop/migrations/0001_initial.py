# Generated by Django 2.2.10 on 2020-08-25 19:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Категория')),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Ссылка')),
                ('state', models.BooleanField(default=True, verbose_name='Статус получения заказов')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазины',
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.PositiveIntegerField(verbose_name='Внешний ИД')),
                ('model', models.CharField(blank=True, max_length=100, verbose_name='Модель')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('price_rrc', models.PositiveIntegerField(blank=True, null=True, verbose_name='Рекомендуемая розничная цена')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Category', verbose_name='Категория')),
                ('shop', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shop.Shop', verbose_name='Магазин')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='shops',
            field=models.ManyToManyField(blank=True, related_name='categories', to='shop.Shop', verbose_name='Магазины'),
        ),
    ]