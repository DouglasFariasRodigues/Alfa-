# Generated manually to simplify member field validations
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0011_simplify_cpf_field'),
    ]

    operations = [
        # Remove validators from telefone field
        migrations.AlterField(
            model_name='membro',
            name='telefone',
            field=models.CharField(
                max_length=15, 
                blank=True, 
                null=True, 
                help_text="Telefone (opcional)"
            ),
        ),
        
        # Remove validate_email_domain from email field
        migrations.AlterField(
            model_name='membro',
            name='email',
            field=models.EmailField(
                validators=[], 
                help_text="Email válido"
            ),
        ),
        
        # Remove validate_age from data_nascimento field
        migrations.AlterField(
            model_name='membro',
            name='data_nascimento',
            field=models.DateField(
                blank=True, 
                null=True, 
                help_text="Data de nascimento (opcional)"
            ),
        ),
        
        # Remove validate_rg from rg field
        migrations.AlterField(
            model_name='membro',
            name='rg',
            field=models.CharField(
                max_length=20, 
                blank=True, 
                null=True, 
                help_text="RG (opcional)"
            ),
        ),
    ]
