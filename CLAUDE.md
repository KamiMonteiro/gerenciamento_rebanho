# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server
python manage.py runserver

# Run all tests
python manage.py test rebanho

# Run a single test
python manage.py test rebanho.tests.FormValidationTests.test_animal_form_rejeita_peso_negativo

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser
```

## Architecture

This is a Django 5.2 web app for livestock management (`gerenciamento_rebanho`). There is a single Django app called `rebanho`; the project config lives in `config/`.

**Language/locale:** Portuguese (pt-br), timezone `America/Sao_Paulo`. Model names, field names, URL names, and template text are all in Portuguese.

**Database:** SQLite (`db.sqlite3`). `AUTH_USER_MODEL = 'rebanho.Usuario'` — the custom user model extends `AbstractUser`.

### Model hierarchy

```
Talhao (farm plot) 1──1 Rebanho (herd) 1──N Animal
                                        └──N Alimento (feeding record, optionally linked to Produto)
Produto (stock item) ──────────────────────────┘

Animal 1──N Sanidade (health record, has criado_por → Usuario)
              └──N Exame
              └──N Vacina
              └──N Medicamento
              └──N Enfermidade
```

Most models inherit from `RegistroBase` (`rebanho/models.py`), which adds `data_cadastro` (auto timestamp) and `ativo` (soft-delete flag). `Sanidade` and its children do not use `RegistroBase`.

### View patterns

All views are class-based and require login (`LoginRequiredMixin`).

- **`TabelaListView`** (`views.py:54`) — generic list view supporting `?q=` text search across `campos_busca` fields and `?ativo=0|1` filtering. Subclasses declare `colunas`, `campos_busca`, and `campos_valores` as class attributes; the generic `templates/rebanho/lista.html` template renders everything.
- **`FormMensagemMixin`** (`views.py:113`) — adds success message and shared template (`rebanho/form.html`) to Create/Update views. Subclasses set `titulo`, `subtitulo`, and `cancelar_url_name`.
- **`ExcluirView`** (`views.py:133`) — shared delete view; instantiated inline in `urls.py` via `.as_view(model=..., success_url=...)`.
- Update views inherit from their corresponding Create view (e.g., `ProdutoUpdateView(ProdutoCreateView, UpdateView)`).

### Form patterns

All forms extend `StyledModelForm` (`forms.py:21`), which:
- Applies Bulma CSS classes (`input`, `textarea`, `select`) automatically to every widget.
- Enforces shared cross-field validations: no negative numeric fields (`quantidade_estoque`, `peso`, `area_total`, `quantidade`), no future `data_nascimento`, no expired `data_validade`, `data_fim >= data_inicio`, `proxima_dose >= data_aplicacao`.

`AnimalForm.clean()` overrides the base to auto-calculate `idade` from `data_nascimento`.

`SanidadeCreateView.form_valid()` automatically sets `criado_por = request.user` — this field is never shown in the form.

### Templates

Global base template: `templates/base.html`. App templates: `templates/rebanho/`. The generic `lista.html` and `form.html` are shared across all entities; entity-specific templates exist only for `Animal` (detail and list views have custom layouts).
