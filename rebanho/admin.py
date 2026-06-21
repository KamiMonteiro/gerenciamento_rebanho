from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Alimento,
    Animal,
    Enfermidade,
    Exame,
    Medicamento,
    Produto,
    Rebanho,
    Sanidade,
    Talhao,
    Usuario,
    Vacina,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Dados do sistema', {'fields': ('nome', 'tipo_usuario', 'permissao', 'data_cadastro')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados do sistema', {'fields': ('nome', 'email', 'tipo_usuario', 'permissao')}),
    )
    readonly_fields = ['data_cadastro']
    list_display = ['username', 'nome', 'email', 'tipo_usuario', 'is_active']
    search_fields = ['username', 'nome', 'email']


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_estoque', 'unidade_medida', 'data_validade', 'ativo']
    search_fields = ['nome', 'fornecedor']
    list_filter = ['ativo', 'data_validade']


@admin.register(Talhao)
class TalhaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'localizacao', 'capacidade', 'area_total', 'ativo']
    search_fields = ['nome', 'localizacao']
    list_filter = ['ativo']


@admin.register(Rebanho)
class RebanhoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'talhao', 'quantidade_animais', 'tipo_criacao', 'ativo']
    search_fields = ['nome', 'tipo_criacao']
    list_filter = ['ativo', 'tipo_criacao']


@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'rebanho', 'produto', 'quantidade', 'data_fornecimento', 'ativo']
    search_fields = ['nome', 'tipo']
    list_filter = ['ativo', 'tipo', 'data_fornecimento']


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['identificacao', 'rebanho', 'raca', 'sexo', 'peso', 'status_saude', 'ativo']
    search_fields = ['identificacao', 'raca']
    list_filter = ['ativo', 'sexo', 'status_saude', 'rebanho']


@admin.register(Sanidade)
class SanidadeAdmin(admin.ModelAdmin):
    list_display = ['animal', 'data_registro', 'status_sanitario', 'criado_por']
    search_fields = ['animal__identificacao', 'observacoes']
    list_filter = ['status_sanitario', 'data_registro']


admin.site.register(Exame)
admin.site.register(Vacina)
admin.site.register(Medicamento)
admin.site.register(Enfermidade)

# Register your models here.
