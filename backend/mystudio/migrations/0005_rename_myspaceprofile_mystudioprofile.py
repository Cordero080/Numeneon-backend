from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mystudio', '0004_increase_url_field_lengths'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MySpaceProfile',
            new_name='MyStudioProfile',
        ),
    ]
