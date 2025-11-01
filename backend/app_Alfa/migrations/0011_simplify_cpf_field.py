# Generated manually to simplify CPF field
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0010_fix_usuario_table'),
    ]

    operations = [
        # Remove unique constraint from CPF field
        migrations.AlterField(
            model_name='membro',
            name='cpf',
            field=models.CharField(
                max_length=14, 
                blank=True, 
                null=True, 
                help_text="CPF (opcional)"
            ),
        ),
    ]
