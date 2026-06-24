from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class RegistroBase(models.Model):
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Usuario(AbstractUser):
    class TipoUsuario(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USUARIO = 'USUARIO', 'Usuario'

    id_usuario = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TipoUsuario.choices,
        default=TipoUsuario.USUARIO,
    )
    permissao = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['nome', 'email']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nome']

    def __str__(self):
        return self.nome or self.username


class Produto(RegistroBase):
    id_produto = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=120)
    quantidade_estoque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidade_medida = models.CharField(max_length=30)
    data_validade = models.DateField(null=True, blank=True)
    fornecedor = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('produto_lista')


class Talhao(RegistroBase):
    id_talhao = models.BigAutoField(primary_key=True)
    nome = models.CharField(max_length=120)
    localizacao = models.CharField(max_length=180)
    capacidade = models.PositiveIntegerField(default=0)
    area_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Talhao'
        verbose_name_plural = 'Talhoes'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Rebanho(RegistroBase):
    id_rebanho = models.BigAutoField(primary_key=True)
    talhao = models.OneToOneField(
        Talhao,
        on_delete=models.PROTECT,
        related_name='rebanho',
    )
    nome = models.CharField(max_length=120)
    tipo_criacao = models.CharField(max_length=80)
    observacoes = models.TextField(blank=True)

    @property
    def quantidade_animais(self):
        return self.animais.count()

    class Meta:
        verbose_name = 'Rebanho'
        verbose_name_plural = 'Rebanhos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Alimento(RegistroBase):
    id_alimento = models.BigAutoField(primary_key=True)
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='alimentos',
        null=True,
        blank=True,
    )
    rebanho = models.ForeignKey(
        Rebanho,
        on_delete=models.PROTECT,
        related_name='alimentos',
    )
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=80)
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_fornecimento = models.DateField()
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Alimento'
        verbose_name_plural = 'Alimentos'
        ordering = ['-data_fornecimento', 'nome']

    def __str__(self):
        return self.nome


class Animal(RegistroBase):
    class Sexo(models.TextChoices):
        MACHO = 'Macho', 'Macho'
        FEMEA = 'Femea', 'Femea'

    class StatusSaude(models.TextChoices):
        SAUDAVEL = 'Saudavel', 'Saudavel'
        OBSERVACAO = 'Observacao', 'Observacao'
        TRATAMENTO = 'Tratamento', 'Tratamento'
        CRITICO = 'Critico', 'Critico'

    id_animal = models.BigAutoField(primary_key=True)
    rebanho = models.ForeignKey(
        Rebanho,
        on_delete=models.PROTECT,
        related_name='animais',
    )
    identificacao = models.CharField(max_length=80, unique=True)
    raca = models.CharField(max_length=80)
    sexo = models.CharField(max_length=10, choices=Sexo.choices)
    idade = models.PositiveIntegerField(default=0)
    peso = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_nascimento = models.DateField(null=True, blank=True)
    status_saude = models.CharField(
        max_length=30,
        choices=StatusSaude.choices,
        default=StatusSaude.SAUDAVEL,
    )
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Animal'
        verbose_name_plural = 'Animais'
        ordering = ['identificacao']

    def __str__(self):
        return self.identificacao

    def get_absolute_url(self):
        return reverse('animal_detalhe', kwargs={'pk': self.pk})


class Sanidade(models.Model):
    class StatusSanitario(models.TextChoices):
        SAUDAVEL = 'Saudavel', 'Saudavel'
        OBSERVACAO = 'Em observacao', 'Em observacao'
        TRATAMENTO = 'Em tratamento', 'Em tratamento'
        CRITICO = 'Critico', 'Critico'

    id_sanidade = models.BigAutoField(primary_key=True)
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name='sanidades',
    )
    data_registro = models.DateField()
    status_sanitario = models.CharField(
        max_length=30,
        choices=StatusSanitario.choices,
        default=StatusSanitario.SAUDAVEL,
    )
    observacoes = models.TextField(blank=True)
    criado_por = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        related_name='sanidades_criadas',
    )

    class Meta:
        verbose_name = 'Sanidade'
        verbose_name_plural = 'Sanidades'
        ordering = ['-data_registro']

    def __str__(self):
        return f'{self.animal} - {self.data_registro:%d/%m/%Y}'


class Exame(models.Model):
    id_exame = models.BigAutoField(primary_key=True)
    sanidade = models.ForeignKey(Sanidade, on_delete=models.CASCADE, related_name='exames')
    nome = models.CharField(max_length=120)
    tipo = models.CharField(max_length=80, blank=True)
    data_realizacao = models.DateField(null=True, blank=True)
    resultado = models.CharField(max_length=180, blank=True)
    status = models.CharField(max_length=80, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Exame'
        verbose_name_plural = 'Exames'
        ordering = ['-data_realizacao', 'nome']

    def __str__(self):
        return self.nome


class Vacina(models.Model):
    id_vacina = models.BigAutoField(primary_key=True)
    sanidade = models.ForeignKey(Sanidade, on_delete=models.CASCADE, related_name='vacinas')
    nome = models.CharField(max_length=120)
    dose = models.CharField(max_length=80, blank=True)
    data_aplicacao = models.DateField(null=True, blank=True)
    proxima_dose = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=80, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Vacina'
        verbose_name_plural = 'Vacinas'
        ordering = ['-data_aplicacao', 'nome']

    def __str__(self):
        return self.nome


class Medicamento(models.Model):
    id_medicamento = models.BigAutoField(primary_key=True)
    sanidade = models.ForeignKey(Sanidade, on_delete=models.CASCADE, related_name='medicamentos')
    nome = models.CharField(max_length=120)
    dosagem = models.CharField(max_length=80, blank=True)
    periodo_tratamento = models.CharField(max_length=120, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'
        ordering = ['-data_inicio', 'nome']

    def __str__(self):
        return self.nome


class Enfermidade(models.Model):
    id_enfermidade = models.BigAutoField(primary_key=True)
    sanidade = models.ForeignKey(Sanidade, on_delete=models.CASCADE, related_name='enfermidades')
    nome = models.CharField(max_length=120)
    descricao = models.TextField(blank=True)
    data_diagnostico = models.DateField(null=True, blank=True)
    gravidade = models.CharField(max_length=80, blank=True)
    status_tratamento = models.CharField(max_length=80, blank=True)
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Enfermidade'
        verbose_name_plural = 'Enfermidades'
        ordering = ['-data_diagnostico', 'nome']

    def __str__(self):
        return self.nome

# Create your models here.
