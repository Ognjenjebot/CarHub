# Generated by Django 4.0.4 on 2022-05-20 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarHub', '0004_alter_oglas_model_idmodel_alter_oglas_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model',
            name='karoserija',
        ),
        migrations.RemoveField(
            model_name='model',
            name='kilometraza',
        ),
        migrations.RemoveField(
            model_name='model',
            name='snaga',
        ),
        migrations.AddField(
            model_name='oglas',
            name='karoserija',
            field=models.CharField(blank=True, db_column='Karoserija', default='limuzina', max_length=20),
        ),
        migrations.AddField(
            model_name='oglas',
            name='kilometraza',
            field=models.IntegerField(db_column='Kilometraza', default=0),
        ),
        migrations.AddField(
            model_name='oglas',
            name='snaga',
            field=models.IntegerField(db_column='Snaga', default=0),
        ),
    ]
