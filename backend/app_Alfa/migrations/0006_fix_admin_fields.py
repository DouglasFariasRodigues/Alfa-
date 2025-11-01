# Generated manually to fix Admin model fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0005_add_last_login_to_membro'),
    ]

    operations = [
        # Add is_admin field to Admin
        migrations.AddField(
            model_name='admin',
            name='is_admin',
            field=models.BooleanField(default=True, help_text='Indica se é administrador do sistema'),
        ),
        
        # Remove is_staff field from Admin
        migrations.RemoveField(
            model_name='admin',
            name='is_staff',
        ),
        
        # Remove date_joined field from Admin
        migrations.RemoveField(
            model_name='admin',
            name='date_joined',
        ),
    ]
