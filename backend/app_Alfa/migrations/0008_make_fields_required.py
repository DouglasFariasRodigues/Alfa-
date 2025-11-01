# Generated manually to make important fields required
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0007_fix_last_login_nullable'),
    ]

    operations = [
        # Make Admin fields required
        migrations.AlterField(
            model_name='admin',
            name='nome',
            field=models.CharField(help_text='Nome completo do administrador', max_length=100),
        ),
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.EmailField(help_text='Email válido', unique=True),
        ),
        
        # Make Usuario fields required
        migrations.AlterField(
            model_name='usuario',
            name='username',
            field=models.CharField(help_text='Nome de usuário único', max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(help_text='Email válido', unique=True),
        ),
        
        # Make Cargo fields required
        migrations.AlterField(
            model_name='cargo',
            name='nome',
            field=models.CharField(help_text='Nome do cargo', max_length=100, unique=True),
        ),
        
        # Make Membro important fields required
        migrations.AlterField(
            model_name='membro',
            name='nome',
            field=models.CharField(help_text='Nome completo do membro', max_length=200),
        ),
        migrations.AlterField(
            model_name='membro',
            name='email',
            field=models.EmailField(help_text='Email válido'),
        ),
    ]
