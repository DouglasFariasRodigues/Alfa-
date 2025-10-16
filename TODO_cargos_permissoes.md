# TODO: Implementar Sistema de Cargos com Permissões

## Tarefas Pendentes
- [x] Modificar modelo Cargo para adicionar campos de permissões (pode_fazer_postagens, pode_registrar_dizimos, pode_registrar_ofertas)
- [x] Modificar Admin e Usuario para usar ForeignKey para Cargo em vez de CharField
- [x] Criar migração para as mudanças nos modelos
- [x] Atualizar views para verificar permissões antes de permitir ações
- [x] Atualizar admin.py para refletir mudanças nos modelos
- [x] Testar criação de cargos com permissões via admin
- [x] Testar verificações de permissões nas views
