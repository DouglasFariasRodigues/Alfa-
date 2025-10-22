# Generated manually to fix BaseModel fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_alfa', '0003_add_cargo_to_membro'),
    ]

    operations = [
        # Add BaseModel fields to Cargo
        migrations.AddField(
            model_name='cargo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='cargo',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        
        # Add BaseModel fields to Admin
        migrations.AddField(
            model_name='admin',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        
        # Add BaseModel fields to Usuario
        migrations.AddField(
            model_name='usuario',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        
        # Add BaseModel fields to Evento
        migrations.AddField(
            model_name='evento',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='evento',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        
        # Add BaseModel fields to Doacao
        migrations.AddField(
            model_name='doacao',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='doacao',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='doacao',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='doacao',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
        
        # Add BaseModel fields to Postagem
        migrations.AddField(
            model_name='postagem',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='postagem',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='postagem',
            name='deleted_at',
            field=models.DateTimeField(blank=True, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='postagem',
            name='is_active',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
