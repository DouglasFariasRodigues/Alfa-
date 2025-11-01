# Generated manually to add last_login field to Membro
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0004_add_base_model_fields'),
    ]

    operations = [
        # Add last_login field to Membro
        migrations.AddField(
            model_name='membro',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
