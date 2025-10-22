"""
Forms customizados para o sistema Alfa+
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Admin, Usuario, Membro, Cargo
from .validators import validate_cpf, validate_phone, validate_rg


class AdminForm(forms.ModelForm):
    """Form para criação/edição de Admin"""
    
    class Meta:
        model = Admin
        fields = ['nome', 'email', 'telefone', 'cargo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            validate_phone(telefone)
        return telefone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Admin.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este email já está em uso.')
        return email


class UsuarioForm(forms.ModelForm):
    """Form para criação/edição de Usuario"""
    
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'telefone', 'cargo']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            validate_phone(telefone)
        return telefone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Usuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este email já está em uso.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este nome de usuário já está em uso.')
        return username


class MembroForm(forms.ModelForm):
    """Form para criação/edição de Membro"""
    
    class Meta:
        model = Membro
        fields = [
            'nome', 'cpf', 'rg', 'data_nascimento', 'telefone', 'email', 
            'endereco', 'status', 'data_batismo', 'igreja_origem', 'cargo'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '000.000.000-00'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RG'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@exemplo.com'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Endereço completo'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'data_batismo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'igreja_origem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Igreja de origem'}),
            'cargo': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf:
            validate_cpf(cpf)
            # Verificar se CPF já existe
            if Membro.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este CPF já está cadastrado.')
        return cpf
    
    def clean_rg(self):
        rg = self.cleaned_data.get('rg')
        if rg:
            validate_rg(rg)
        return rg
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            validate_phone(telefone)
        return telefone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and Membro.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Este email já está em uso.')
        return email


class CargoForm(forms.ModelForm):
    """Form para criação/edição de Cargo"""
    
    class Meta:
        model = Cargo
        fields = [
            'nome', 'descricao', 'pode_registrar_dizimos', 'pode_registrar_ofertas',
            'pode_gerenciar_membros', 'pode_gerenciar_eventos', 'pode_gerenciar_financas',
            'pode_gerenciar_cargos', 'pode_gerenciar_documentos', 'pode_visualizar_relatorios'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cargo'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do cargo'}),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and Cargo.objects.filter(nome=nome).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um cargo com este nome.')
        return nome


class MembroSearchForm(forms.Form):
    """Form para busca de membros"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome, email ou CPF...'
        })
    )
    status = forms.ChoiceField(
        choices=[('', 'Todos os status')] + Membro.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.all(),
        required=False,
        empty_label="Todos os cargos",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class AdminPasswordForm(forms.Form):
    """Form para alteração de senha de admin"""
    senha_atual = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha atual'})
    )
    nova_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova senha'})
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar nova senha'})
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if nova_senha and confirmar_senha:
            if nova_senha != confirmar_senha:
                raise ValidationError('As senhas não coincidem.')
            
            if len(nova_senha) < 6:
                raise ValidationError('A senha deve ter pelo menos 6 caracteres.')
        
        return cleaned_data
