import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Alfa_project.settings')
django.setup()

from app_Alfa.models import Admin, Cargo, Usuario
from django.contrib.auth.hashers import make_password

def create_admin():
    # Create or get the 'Administrador' cargo
    cargo_admin, created = Cargo.objects.get_or_create(
        nome='Administrador',
        defaults={'descricao': 'Administrador do sistema'}
    )

    # Check if admin already exists
    if Admin.objects.filter(email='admin@exemplo').exists():
        print("Admin já existe!")
        return

    # Create the admin user
    admin = Admin.objects.create(
        username='admin@exemplo',
        nome='Admin',
        email='admin@exemplo',
        password=make_password('admin'),
        cargo=cargo_admin,
        is_staff=True
    )
    print("Admin criado com sucesso!")
    print(f"Username: {admin.username}")
    print("Password: admin")

def create_visitor():
    # Check if visitor already exists
    if Usuario.objects.filter(username='visitante').exists():
        print("Visitante já existe!")
        return

    # Create the visitor user
    visitor = Usuario.objects.create(
        username='visitante',
        email='visitante@exemplo.com',
        password=make_password('visitante'),
        is_active=True
    )
    print("Visitante criado com sucesso!")
    print(f"Username: {visitor.username}")
    print("Password: visitante")

if __name__ == '__main__':
    create_admin()
    create_visitor()
