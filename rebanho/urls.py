from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('animais/', views.AnimalListView.as_view(), name='animal_lista'),
    path('animais/novo/', views.AnimalCreateView.as_view(), name='animal_criar'),
    path('animais/<int:pk>/', views.AnimalDetailView.as_view(), name='animal_detalhe'),
    path('animais/<int:pk>/editar/', views.AnimalUpdateView.as_view(), name='animal_editar'),
    path('animais/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Animal, success_url='/animais/'), name='animal_excluir'),

    path('rebanhos/', views.RebanhoListView.as_view(), name='rebanho_lista'),
    path('rebanhos/novo/', views.RebanhoCreateView.as_view(), name='rebanho_criar'),
    path('rebanhos/<int:pk>/editar/', views.RebanhoUpdateView.as_view(), name='rebanho_editar'),
    path('rebanhos/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Rebanho, success_url='/rebanhos/'), name='rebanho_excluir'),

    path('talhoes/', views.TalhaoListView.as_view(), name='talhao_lista'),
    path('talhoes/novo/', views.TalhaoCreateView.as_view(), name='talhao_criar'),
    path('talhoes/<int:pk>/editar/', views.TalhaoUpdateView.as_view(), name='talhao_editar'),
    path('talhoes/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Talhao, success_url='/talhoes/'), name='talhao_excluir'),

    path('produtos/', views.ProdutoListView.as_view(), name='produto_lista'),
    path('produtos/novo/', views.ProdutoCreateView.as_view(), name='produto_criar'),
    path('produtos/<int:pk>/editar/', views.ProdutoUpdateView.as_view(), name='produto_editar'),
    path('produtos/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Produto, success_url='/produtos/'), name='produto_excluir'),

    path('alimentos/', views.AlimentoListView.as_view(), name='alimento_lista'),
    path('alimentos/novo/', views.AlimentoCreateView.as_view(), name='alimento_criar'),
    path('alimentos/<int:pk>/editar/', views.AlimentoUpdateView.as_view(), name='alimento_editar'),
    path('alimentos/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Alimento, success_url='/alimentos/'), name='alimento_excluir'),

    path('sanidade/', views.SanidadeListView.as_view(), name='sanidade_lista'),
    path('sanidade/novo/', views.SanidadeCreateView.as_view(), name='sanidade_criar'),
    path('sanidade/<int:pk>/editar/', views.SanidadeUpdateView.as_view(), name='sanidade_editar'),
    path('sanidade/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Sanidade, success_url='/sanidade/'), name='sanidade_excluir'),
    path('sanidade/<int:pk>/', views.SanidadeUpdateView.as_view(), name='sanidade_detalhe'),

    path('exames/', views.ExameListView.as_view(), name='exame_lista'),
    path('exames/novo/', views.ExameCreateView.as_view(), name='exame_criar'),
    path('exames/<int:pk>/editar/', views.ExameUpdateView.as_view(), name='exame_editar'),
    path('exames/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Exame, success_url='/exames/'), name='exame_excluir'),

    path('vacinas/', views.VacinaListView.as_view(), name='vacina_lista'),
    path('vacinas/novo/', views.VacinaCreateView.as_view(), name='vacina_criar'),
    path('vacinas/<int:pk>/editar/', views.VacinaUpdateView.as_view(), name='vacina_editar'),
    path('vacinas/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Vacina, success_url='/vacinas/'), name='vacina_excluir'),

    path('medicamentos/', views.MedicamentoListView.as_view(), name='medicamento_lista'),
    path('medicamentos/novo/', views.MedicamentoCreateView.as_view(), name='medicamento_criar'),
    path('medicamentos/<int:pk>/editar/', views.MedicamentoUpdateView.as_view(), name='medicamento_editar'),
    path('medicamentos/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Medicamento, success_url='/medicamentos/'), name='medicamento_excluir'),

    path('enfermidades/', views.EnfermidadeListView.as_view(), name='enfermidade_lista'),
    path('enfermidades/novo/', views.EnfermidadeCreateView.as_view(), name='enfermidade_criar'),
    path('enfermidades/<int:pk>/editar/', views.EnfermidadeUpdateView.as_view(), name='enfermidade_editar'),
    path('enfermidades/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Enfermidade, success_url='/enfermidades/'), name='enfermidade_excluir'),

    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_lista'),
    path('usuarios/novo/', views.UsuarioCreateView.as_view(), name='usuario_criar'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_editar'),
    path('usuarios/<int:pk>/excluir/', views.ExcluirView.as_view(model=views.Usuario, success_url='/usuarios/'), name='usuario_excluir'),
]
