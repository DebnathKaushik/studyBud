# Generated by Django 4.1.7 on 2023-05-25 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_meassage_topic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-updated', '-created']},
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='name',
            new_name='namee',
        ),
    ]
