# Generated manually to fix last_login field to allow NULL
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0006_fix_admin_fields'),
    ]

    operations = [
        # Make last_login field nullable for Admin
        migrations.AlterField(
            model_name='admin',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Make last_login field nullable for Usuario
        migrations.AlterField(
            model_name='usuario',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Make last_login field nullable for Membro
        migrations.AlterField(
            model_name='membro',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
