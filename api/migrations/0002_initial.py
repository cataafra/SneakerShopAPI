# Generated by Django 3.2.18 on 2023-04-09 11:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoughtGarments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('review', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['customer'],
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country_of_origin', models.CharField(max_length=100)),
                ('founder', models.CharField(max_length=100)),
                ('motto', models.CharField(max_length=100)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Garment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('size', models.CharField(max_length=15)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sneaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
                ('size', models.PositiveIntegerField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('age', models.PositiveIntegerField()),
                ('date_added', models.DateField(auto_now_add=True)),
                ('garments_bought', models.ManyToManyField(through='api.BoughtGarments', to='api.Garment')),
            ],
        ),
        migrations.AddField(
            model_name='boughtgarments',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.customer'),
        ),
        migrations.AddField(
            model_name='boughtgarments',
            name='garment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.garment'),
        ),
        migrations.AlterUniqueTogether(
            name='boughtgarments',
            unique_together={('garment', 'customer')},
        ),
    ]
