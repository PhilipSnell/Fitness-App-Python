# Generated by Django 2.2.14 on 2021-10-28 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_week_isactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='SetFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=300)),
                ('difficulty', models.IntegerField()),
                ('training_Entry', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='setFeedback', to='api.TrainingEntry')),
            ],
        ),
    ]
