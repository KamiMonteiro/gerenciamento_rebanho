from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .forms import (
    AlimentoForm,
    AnimalForm,
    MedicamentoForm,
    ProdutoForm,
    TalhaoForm,
    VacinaForm,
)
from .models import (
    Alimento,
    Animal,
    Medicamento,
    Produto,
    Rebanho,
    Sanidade,
    Talhao,
    Usuario,
    Vacina,
)


class FormValidationTests(TestCase):
    def setUp(self):
        self.talhao = Talhao.objects.create(
            nome='Talhao teste',
            localizacao='Area 1',
            capacidade=100,
            area_total=1000,
        )
        self.rebanho = Rebanho.objects.create(
            talhao=self.talhao,
            nome='Rebanho teste',
            tipo_criacao='Pastagem',
        )
        self.usuario = Usuario.objects.create_user(
            username='tester',
            email='tester@example.com',
            password='123456',
            nome='Tester',
        )
        self.animal = Animal.objects.create(
            rebanho=self.rebanho,
            identificacao='A-001',
            raca='Holandesa',
            sexo=Animal.Sexo.MACHO,
            idade=2,
            peso=150,
            data_nascimento=timezone.localdate() - timedelta(days=365),
            status_saude=Animal.StatusSaude.SAUDAVEL,
        )
        self.sanidade = Sanidade.objects.create(
            animal=self.animal,
            data_registro=timezone.localdate(),
            status_sanitario=Sanidade.StatusSanitario.SAUDAVEL,
            observacoes='',
            criado_por=self.usuario,
        )

    def test_produto_form_rejeita_quantidade_estoque_negativa(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        form = ProdutoForm(data={
            'nome': 'Racao',
            'quantidade_estoque': -1,
            'unidade_medida': 'kg',
            'data_validade': tomorrow.strftime('%Y-%m-%d'),
            'fornecedor': 'Fornecedor',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('quantidade_estoque', form.errors)

    def test_produto_form_rejeita_validade_expirada(self):
        yesterday = timezone.localdate() - timedelta(days=1)
        form = ProdutoForm(data={
            'nome': 'Racao',
            'quantidade_estoque': 10,
            'unidade_medida': 'kg',
            'data_validade': yesterday.strftime('%Y-%m-%d'),
            'fornecedor': 'Fornecedor',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('data_validade', form.errors)

    def test_animal_form_rejeita_peso_negativo(self):
        form = AnimalForm(data={
            'rebanho': self.rebanho.id_rebanho,
            'identificacao': 'A-002',
            'raca': 'Holandesa',
            'sexo': Animal.Sexo.MACHO,
            'idade': 2,
            'peso': -5,
            'data_nascimento': (timezone.localdate() - timedelta(days=365)).strftime('%Y-%m-%d'),
            'status_saude': Animal.StatusSaude.SAUDAVEL,
            'observacoes': '',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('peso', form.errors)

    def test_animal_form_rejeita_data_nascimento_futura(self):
        tomorrow = timezone.localdate() + timedelta(days=1)
        form = AnimalForm(data={
            'rebanho': self.rebanho.id_rebanho,
            'identificacao': 'A-003',
            'raca': 'Holandesa',
            'sexo': Animal.Sexo.FEMEA,
            'idade': 2,
            'peso': 150,
            'data_nascimento': tomorrow.strftime('%Y-%m-%d'),
            'status_saude': Animal.StatusSaude.SAUDAVEL,
            'observacoes': '',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('data_nascimento', form.errors)

    def test_talhao_form_rejeita_area_total_negativa(self):
        form = TalhaoForm(data={
            'nome': 'Talhao invalido',
            'localizacao': 'Area 2',
            'capacidade': 20,
            'area_total': -10,
            'observacoes': '',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('area_total', form.errors)

    def test_alimento_form_rejeita_quantidade_negativa(self):
        form = AlimentoForm(data={
            'produto': None,
            'rebanho': self.rebanho.id_rebanho,
            'nome': 'Alimento',
            'tipo': 'Concentrado',
            'quantidade': -1,
            'data_fornecimento': timezone.localdate().strftime('%Y-%m-%d'),
            'observacoes': '',
            'ativo': True,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('quantidade', form.errors)

    def test_medicamento_form_rejeita_data_fim_anterior_data_inicio(self):
        start = timezone.localdate()
        end = start - timedelta(days=1)
        form = MedicamentoForm(data={
            'sanidade': self.sanidade.id_sanidade,
            'nome': 'Antibiotico',
            'dosagem': '10ml',
            'periodo_tratamento': '7 dias',
            'data_inicio': start.strftime('%Y-%m-%d'),
            'data_fim': end.strftime('%Y-%m-%d'),
            'observacoes': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('data_fim', form.errors)

    def test_vacina_form_rejeita_proxima_dose_anterior_data_aplicacao(self):
        application = timezone.localdate()
        next_dose = application - timedelta(days=1)
        form = VacinaForm(data={
            'sanidade': self.sanidade.id_sanidade,
            'nome': 'Vacina',
            'dose': '1 dose',
            'data_aplicacao': application.strftime('%Y-%m-%d'),
            'proxima_dose': next_dose.strftime('%Y-%m-%d'),
            'status': 'Aplicada',
            'observacoes': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('proxima_dose', form.errors)

    def test_animal_form_rende_data_nascimento_no_formato_compatível(self):
        form = AnimalForm(instance=self.animal)

        self.assertEqual(form['data_nascimento'].value(), self.animal.data_nascimento)
        self.assertIn(f"value=\"{self.animal.data_nascimento.strftime('%Y-%m-%d')}\"", form['data_nascimento'].as_widget())

    def test_animal_form_calcula_idade_automaticamente(self):
        birth_date = timezone.localdate() - timedelta(days=365 * 3 + 100)
        form = AnimalForm(data={
            'rebanho': self.rebanho.id_rebanho,
            'identificacao': 'A-004',
            'raca': 'Holandesa',
            'sexo': Animal.Sexo.MACHO,
            'idade': 0,
            'peso': 150,
            'data_nascimento': birth_date.strftime('%Y-%m-%d'),
            'status_saude': Animal.StatusSaude.SAUDAVEL,
            'observacoes': '',
            'ativo': True,
        })

        self.assertTrue(form.is_valid())
        animal = form.save()
        today = timezone.localdate()
        expected_age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        self.assertEqual(animal.idade, expected_age)
