from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

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


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'textarea' if isinstance(field.widget, forms.Textarea) else 'input'
            if isinstance(field.widget, forms.Select):
                css_class = 'select'
            field.widget.attrs.setdefault('class', css_class)

            if isinstance(field.widget, forms.DateInput):
                field.widget.format = '%Y-%m-%d'

    def clean(self):
        cleaned_data = super().clean()

        for field_name in ['quantidade_estoque', 'peso', 'area_total', 'quantidade']:
            value = cleaned_data.get(field_name)
            if value is not None and value < 0:
                self.add_error(field_name, ValidationError('Este campo não pode ser negativo.'))

        data_nascimento = cleaned_data.get('data_nascimento')
        if data_nascimento and data_nascimento > timezone.localdate():
            self.add_error('data_nascimento', ValidationError('A data de nascimento não pode ser futura.'))

        data_validade = cleaned_data.get('data_validade')
        if data_validade and data_validade < timezone.localdate():
            self.add_error('data_validade', ValidationError('A data de validade deve ser hoje ou no futuro.'))

        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error('data_fim', ValidationError('A data de fim não pode ser anterior à data de início.'))

        data_aplicacao = cleaned_data.get('data_aplicacao')
        proxima_dose = cleaned_data.get('proxima_dose')
        if data_aplicacao and proxima_dose and proxima_dose < data_aplicacao:
            self.add_error('proxima_dose', ValidationError('A próxima dose não pode ser anterior à data de aplicação.'))

        return cleaned_data


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'nome', 'email', 'tipo_usuario', 'permissao', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = 'textarea' if isinstance(field.widget, forms.Textarea) else 'input'
            if isinstance(field.widget, forms.Select):
                css_class = 'select'
            field.widget.attrs.setdefault('class', css_class)


class ProdutoForm(StyledModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'quantidade_estoque', 'unidade_medida', 'data_validade', 'fornecedor', 'ativo']
        widgets = {'data_validade': forms.DateInput(attrs={'type': 'date'})}


class TalhaoForm(StyledModelForm):
    class Meta:
        model = Talhao
        fields = ['nome', 'localizacao', 'capacidade', 'area_total', 'observacoes', 'ativo']


class RebanhoForm(StyledModelForm):
    class Meta:
        model = Rebanho
        fields = ['talhao', 'nome', 'tipo_criacao', 'observacoes', 'ativo']


class AlimentoForm(StyledModelForm):
    class Meta:
        model = Alimento
        fields = ['produto', 'rebanho', 'nome', 'tipo', 'quantidade', 'data_fornecimento', 'observacoes', 'ativo']
        widgets = {'data_fornecimento': forms.DateInput(attrs={'type': 'date'})}


class AnimalForm(StyledModelForm):
    class Meta:
        model = Animal
        fields = [
            'rebanho',
            'identificacao',
            'raca',
            'sexo',
            'idade',
            'peso',
            'data_nascimento',
            'status_saude',
            'observacoes',
            'ativo',
        ]
        widgets = {'data_nascimento': forms.DateInput(attrs={'type': 'date'})}

    def clean(self):
        cleaned_data = super().clean()
        data_nascimento = cleaned_data.get('data_nascimento')

        if data_nascimento:
            today = timezone.localdate()
            idade = today.year - data_nascimento.year - ((today.month, today.day) < (data_nascimento.month, data_nascimento.day))
            cleaned_data['idade'] = idade

        return cleaned_data


class SanidadeForm(StyledModelForm):
    class Meta:
        model = Sanidade
        fields = ['animal', 'data_registro', 'status_sanitario', 'observacoes']
        widgets = {'data_registro': forms.DateInput(attrs={'type': 'date'})}


class ExameForm(StyledModelForm):
    class Meta:
        model = Exame
        fields = ['sanidade', 'nome', 'tipo', 'data_realizacao', 'resultado', 'status', 'observacoes']
        widgets = {'data_realizacao': forms.DateInput(attrs={'type': 'date'})}


class VacinaForm(StyledModelForm):
    class Meta:
        model = Vacina
        fields = ['sanidade', 'nome', 'dose', 'data_aplicacao', 'proxima_dose', 'status', 'observacoes']
        widgets = {
            'data_aplicacao': forms.DateInput(attrs={'type': 'date'}),
            'proxima_dose': forms.DateInput(attrs={'type': 'date'}),
        }


class MedicamentoForm(StyledModelForm):
    class Meta:
        model = Medicamento
        fields = ['sanidade', 'nome', 'dosagem', 'periodo_tratamento', 'data_inicio', 'data_fim', 'observacoes']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'type': 'date'}),
        }


class EnfermidadeForm(StyledModelForm):
    class Meta:
        model = Enfermidade
        fields = ['sanidade', 'nome', 'descricao', 'data_diagnostico', 'gravidade', 'status_tratamento', 'observacoes']
        widgets = {'data_diagnostico': forms.DateInput(attrs={'type': 'date'})}
