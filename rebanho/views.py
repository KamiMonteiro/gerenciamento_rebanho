from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import (
    AlimentoForm,
    AnimalForm,
    EnfermidadeForm,
    ExameForm,
    MedicamentoForm,
    ProdutoForm,
    RebanhoForm,
    SanidadeForm,
    TalhaoForm,
    UsuarioForm,
    VacinaForm,
)
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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'rebanho/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_animais': Animal.objects.filter(ativo=True).count(),
            'animais_em_observacao': Animal.objects.filter(status_saude__in=['Observacao', 'Tratamento', 'Critico']).count(),
            'total_rebanhos': Rebanho.objects.filter(ativo=True).count(),
            'total_talhoes': Talhao.objects.filter(ativo=True).count(),
            'total_produtos': Produto.objects.filter(ativo=True).count(),
            'produtos_baixo_estoque': Produto.objects.filter(ativo=True, quantidade_estoque__lte=5).count(),
            'total_sanidades': Sanidade.objects.count(),
            'tratamentos_abertos': Sanidade.objects.filter(status_sanitario__in=['Em tratamento', 'Critico']).count(),
            'ultimos_animais': Animal.objects.select_related('rebanho').order_by('-data_cadastro')[:5],
        })
        return context


class TabelaListView(LoginRequiredMixin, ListView):
    template_name = 'rebanho/lista.html'
    context_object_name = 'objetos'
    paginate_by = 20
    titulo = 'Registros'
    criar_url_name = ''
    editar_url_name = ''
    detalhe_url_name = ''
    excluir_url_name = ''
    colunas = []
    campos_busca = []
    campos_valores = []
    nav_block = ''

    def get_queryset(self):
        queryset = super().get_queryset()
        ativo = self.request.GET.get('ativo')
        busca = self.request.GET.get('q')

        if ativo in ['0', '1'] and hasattr(self.model, 'ativo'):
            queryset = queryset.filter(ativo=ativo == '1')

        if busca and self.campos_busca:
            filtro = Q()
            for campo in self.campos_busca:
                filtro |= Q(**{f'{campo}__icontains': busca})
            queryset = queryset.filter(filtro)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens = []
        for obj in context['objetos']:
            itens.append({
                'valores': [self.valor_objeto(obj, campo) for campo in self.campos_valores],
                'ativo': getattr(obj, 'ativo', True),
                'detalhe_url': reverse(self.detalhe_url_name, kwargs={'pk': obj.pk}) if self.detalhe_url_name else '#',
                'editar_url': reverse(self.editar_url_name, kwargs={'pk': obj.pk}) if self.editar_url_name else '#',
                'excluir_url': reverse(self.excluir_url_name, kwargs={'pk': obj.pk}) if self.excluir_url_name else '#',
            })
        context.update({
            'titulo': self.titulo,
            'colunas': self.colunas,
            'itens': itens,
            'criar_url': reverse(self.criar_url_name),
            'nav_block': self.nav_block,
        })
        return context

    def valor_objeto(self, obj, campo):
        valor = obj
        for parte in campo.split('__'):
            valor = getattr(valor, parte, '')
            if valor is None:
                return ''
        return valor


class FormMensagemMixin:
    template_name = 'rebanho/form.html'
    titulo = 'Cadastro'
    subtitulo = 'Preencha os dados do registro.'
    cancelar_url_name = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'titulo': self.titulo,
            'subtitulo': self.subtitulo,
            'cancelar_url': reverse(self.cancelar_url_name),
        })
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Registro salvo com sucesso.')
        return super().form_valid(form)


class ExcluirView(LoginRequiredMixin, DeleteView):
    template_name = 'rebanho/confirmar_exclusao.html'
    success_message = 'Registro excluido com sucesso.'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)


class AnimalListView(TabelaListView):
    model = Animal
    template_name = 'rebanho/animal_lista.html'
    context_object_name = 'animais'

    def get_queryset(self):
        queryset = Animal.objects.select_related('rebanho')
        busca = self.request.GET.get('q')
        rebanho = self.request.GET.get('rebanho')
        if busca:
            queryset = queryset.filter(
                Q(identificacao__icontains=busca)
                | Q(raca__icontains=busca)
                | Q(status_saude__icontains=busca)
            )
        if rebanho:
            queryset = queryset.filter(rebanho_id=rebanho)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListView, self).get_context_data(**kwargs)
        context['animais'] = self.get_queryset()
        context['rebanhos'] = Rebanho.objects.filter(ativo=True)
        return context


class AnimalDetailView(LoginRequiredMixin, DetailView):
    model = Animal
    template_name = 'rebanho/animal_detalhe.html'
    context_object_name = 'animal'

    def get_queryset(self):
        return Animal.objects.select_related('rebanho')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sanidades'] = self.object.sanidades.select_related('criado_por')
        return context


class SanidadeCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Sanidade
    form_class = SanidadeForm
    titulo = 'Registro sanitario'
    subtitulo = 'Controle o historico sanitario de cada animal.'
    cancelar_url_name = 'sanidade_lista'
    success_url = reverse_lazy('sanidade_lista')

    def get_initial(self):
        initial = super().get_initial()
        animal_id = self.request.GET.get('animal')
        if animal_id:
            initial['animal'] = animal_id
        return initial

    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)


class SanidadeUpdateView(FormMensagemMixin, LoginRequiredMixin, UpdateView):
    model = Sanidade
    form_class = SanidadeForm
    titulo = 'Editar registro sanitario'
    subtitulo = 'Atualize as informacoes sanitarias.'
    cancelar_url_name = 'sanidade_lista'
    success_url = reverse_lazy('sanidade_lista')


class ProdutoListView(TabelaListView):
    model = Produto
    titulo = 'Produtos'
    criar_url_name = 'produto_criar'
    editar_url_name = 'produto_editar'
    detalhe_url_name = 'produto_editar'
    excluir_url_name = 'produto_excluir'
    colunas = ['Nome', 'Quantidade', 'Unidade', 'Validade', 'Fornecedor']
    campos_busca = ['nome', 'fornecedor']
    campos_valores = ['nome', 'quantidade_estoque', 'unidade_medida', 'data_validade', 'fornecedor']


class AlimentoListView(TabelaListView):
    model = Alimento
    titulo = 'Alimentos'
    criar_url_name = 'alimento_criar'
    editar_url_name = 'alimento_editar'
    detalhe_url_name = 'alimento_editar'
    excluir_url_name = 'alimento_excluir'
    colunas = ['Nome', 'Tipo', 'Rebanho', 'Quantidade', 'Fornecimento']
    campos_busca = ['nome', 'tipo', 'rebanho__nome']
    campos_valores = ['nome', 'tipo', 'rebanho', 'quantidade', 'data_fornecimento']

    def get_queryset(self):
        return super().get_queryset().select_related('rebanho', 'produto')


class RebanhoListView(TabelaListView):
    model = Rebanho
    titulo = 'Rebanhos'
    criar_url_name = 'rebanho_criar'
    editar_url_name = 'rebanho_editar'
    detalhe_url_name = 'rebanho_editar'
    excluir_url_name = 'rebanho_excluir'
    colunas = ['Nome', 'Talhao', 'Quantidade', 'Tipo de criacao']
    campos_busca = ['nome', 'tipo_criacao', 'talhao__nome']
    campos_valores = ['nome', 'talhao', 'quantidade_animais', 'tipo_criacao']

    def get_queryset(self):
        return super().get_queryset().select_related('talhao')


class TalhaoListView(TabelaListView):
    model = Talhao
    titulo = 'Talhoes'
    criar_url_name = 'talhao_criar'
    editar_url_name = 'talhao_editar'
    detalhe_url_name = 'talhao_editar'
    excluir_url_name = 'talhao_excluir'
    colunas = ['Nome', 'Localizacao', 'Capacidade', 'Area total']
    campos_busca = ['nome', 'localizacao']
    campos_valores = ['nome', 'localizacao', 'capacidade', 'area_total']


class SanidadeListView(TabelaListView):
    model = Sanidade
    titulo = 'Sanidade'
    criar_url_name = 'sanidade_criar'
    editar_url_name = 'sanidade_editar'
    detalhe_url_name = 'sanidade_editar'
    excluir_url_name = 'sanidade_excluir'
    colunas = ['Animal', 'Data', 'Status', 'Responsavel']
    campos_busca = ['animal__identificacao', 'status_sanitario', 'criado_por__nome']
    campos_valores = ['animal', 'data_registro', 'status_sanitario', 'criado_por']

    def get_queryset(self):
        return super().get_queryset().select_related('animal', 'criado_por')


class UsuarioListView(TabelaListView):
    model = Usuario
    titulo = 'Usuarios'
    criar_url_name = 'usuario_criar'
    editar_url_name = 'usuario_editar'
    detalhe_url_name = 'usuario_editar'
    excluir_url_name = 'usuario_excluir'
    colunas = ['Nome', 'Usuario', 'Email', 'Tipo']
    campos_busca = ['nome', 'username', 'email', 'tipo_usuario']
    campos_valores = ['nome', 'username', 'email', 'tipo_usuario']


class DetalheSaudeListView(TabelaListView):
    tipo = ''


class ExameListView(DetalheSaudeListView):
    model = Exame
    titulo = 'Exames'
    criar_url_name = 'exame_criar'
    editar_url_name = 'exame_editar'
    detalhe_url_name = 'exame_editar'
    excluir_url_name = 'exame_excluir'
    colunas = ['Nome', 'Animal', 'Tipo', 'Data', 'Status']
    campos_busca = ['nome', 'tipo', 'sanidade__animal__identificacao']
    campos_valores = ['nome', 'sanidade__animal', 'tipo', 'data_realizacao', 'status']

    def get_queryset(self):
        return super().get_queryset().select_related('sanidade__animal')


class VacinaListView(DetalheSaudeListView):
    model = Vacina
    titulo = 'Vacinas'
    criar_url_name = 'vacina_criar'
    editar_url_name = 'vacina_editar'
    detalhe_url_name = 'vacina_editar'
    excluir_url_name = 'vacina_excluir'
    colunas = ['Nome', 'Animal', 'Dose', 'Aplicacao', 'Proxima dose']
    campos_busca = ['nome', 'dose', 'sanidade__animal__identificacao']
    campos_valores = ['nome', 'sanidade__animal', 'dose', 'data_aplicacao', 'proxima_dose']

    def get_queryset(self):
        return super().get_queryset().select_related('sanidade__animal')


class MedicamentoListView(DetalheSaudeListView):
    model = Medicamento
    titulo = 'Medicamentos'
    criar_url_name = 'medicamento_criar'
    editar_url_name = 'medicamento_editar'
    detalhe_url_name = 'medicamento_editar'
    excluir_url_name = 'medicamento_excluir'
    colunas = ['Nome', 'Animal', 'Dosagem', 'Inicio', 'Fim']
    campos_busca = ['nome', 'dosagem', 'sanidade__animal__identificacao']
    campos_valores = ['nome', 'sanidade__animal', 'dosagem', 'data_inicio', 'data_fim']

    def get_queryset(self):
        return super().get_queryset().select_related('sanidade__animal')


class EnfermidadeListView(DetalheSaudeListView):
    model = Enfermidade
    titulo = 'Enfermidades'
    criar_url_name = 'enfermidade_criar'
    editar_url_name = 'enfermidade_editar'
    detalhe_url_name = 'enfermidade_editar'
    excluir_url_name = 'enfermidade_excluir'
    colunas = ['Nome', 'Animal', 'Diagnostico', 'Gravidade', 'Tratamento']
    campos_busca = ['nome', 'gravidade', 'status_tratamento', 'sanidade__animal__identificacao']
    campos_valores = ['nome', 'sanidade__animal', 'data_diagnostico', 'gravidade', 'status_tratamento']

    def get_queryset(self):
        return super().get_queryset().select_related('sanidade__animal')


class ProdutoCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Produto
    form_class = ProdutoForm
    titulo = 'Cadastro de produto'
    cancelar_url_name = 'produto_lista'
    success_url = reverse_lazy('produto_lista')


class ProdutoUpdateView(ProdutoCreateView, UpdateView):
    titulo = 'Editar produto'


class AlimentoCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Alimento
    form_class = AlimentoForm
    titulo = 'Cadastro de alimento'
    cancelar_url_name = 'alimento_lista'
    success_url = reverse_lazy('alimento_lista')


class AlimentoUpdateView(AlimentoCreateView, UpdateView):
    titulo = 'Editar alimento'


class RebanhoCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Rebanho
    form_class = RebanhoForm
    titulo = 'Cadastro de rebanho'
    cancelar_url_name = 'rebanho_lista'
    success_url = reverse_lazy('rebanho_lista')


class RebanhoUpdateView(RebanhoCreateView, UpdateView):
    titulo = 'Editar rebanho'


class TalhaoCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Talhao
    form_class = TalhaoForm
    titulo = 'Cadastro de talhao'
    cancelar_url_name = 'talhao_lista'
    success_url = reverse_lazy('talhao_lista')


class TalhaoUpdateView(TalhaoCreateView, UpdateView):
    titulo = 'Editar talhao'


class AnimalCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalForm
    titulo = 'Cadastro de animal'
    cancelar_url_name = 'animal_lista'
    success_url = reverse_lazy('animal_lista')


class AnimalUpdateView(AnimalCreateView, UpdateView):
    titulo = 'Editar animal'


class UsuarioCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    titulo = 'Cadastro de usuario'
    cancelar_url_name = 'usuario_lista'
    success_url = reverse_lazy('usuario_lista')


class UsuarioUpdateView(FormMensagemMixin, LoginRequiredMixin, UpdateView):
    model = Usuario
    fields = ['username', 'nome', 'email', 'tipo_usuario', 'permissao', 'is_active']
    template_name = 'rebanho/form.html'
    titulo = 'Editar usuario'
    cancelar_url_name = 'usuario_lista'
    success_url = reverse_lazy('usuario_lista')


class ExameCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Exame
    form_class = ExameForm
    titulo = 'Cadastro de exame'
    cancelar_url_name = 'exame_lista'
    success_url = reverse_lazy('exame_lista')


class ExameUpdateView(ExameCreateView, UpdateView):
    titulo = 'Editar exame'


class VacinaCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Vacina
    form_class = VacinaForm
    titulo = 'Cadastro de vacina'
    cancelar_url_name = 'vacina_lista'
    success_url = reverse_lazy('vacina_lista')


class VacinaUpdateView(VacinaCreateView, UpdateView):
    titulo = 'Editar vacina'


class MedicamentoCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    titulo = 'Cadastro de medicamento'
    cancelar_url_name = 'medicamento_lista'
    success_url = reverse_lazy('medicamento_lista')


class MedicamentoUpdateView(MedicamentoCreateView, UpdateView):
    titulo = 'Editar medicamento'


class EnfermidadeCreateView(FormMensagemMixin, LoginRequiredMixin, CreateView):
    model = Enfermidade
    form_class = EnfermidadeForm
    titulo = 'Cadastro de enfermidade'
    cancelar_url_name = 'enfermidade_lista'
    success_url = reverse_lazy('enfermidade_lista')


class EnfermidadeUpdateView(EnfermidadeCreateView, UpdateView):
    titulo = 'Editar enfermidade'

# Create your views here.
