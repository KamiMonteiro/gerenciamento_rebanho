from django.db import migrations
from datetime import date
from decimal import Decimal


def criar_dados_iniciais(apps, schema_editor):
    from django.contrib.auth.hashers import make_password

    Usuario     = apps.get_model("rebanho", "Usuario")
    Produto     = apps.get_model("rebanho", "Produto")
    Talhao      = apps.get_model("rebanho", "Talhao")
    Rebanho     = apps.get_model("rebanho", "Rebanho")
    Animal      = apps.get_model("rebanho", "Animal")
    Alimento    = apps.get_model("rebanho", "Alimento")
    Sanidade    = apps.get_model("rebanho", "Sanidade")
    Exame       = apps.get_model("rebanho", "Exame")
    Vacina      = apps.get_model("rebanho", "Vacina")
    Medicamento = apps.get_model("rebanho", "Medicamento")
    Enfermidade = apps.get_model("rebanho", "Enfermidade")

    # ----------------------------------------------------------------
    # 1. USUARIO ADMIN
    # ----------------------------------------------------------------
    usuario = Usuario.objects.create(
        username="admin_fazenda",
        nome="Administrador da Fazenda",
        email="admin@fazenda.com.br",
        password=make_password("Fazenda@2026"),
        tipo_usuario="ADMIN",
        is_staff=True,
        is_superuser=True,
        is_active=True,
    )

    # ----------------------------------------------------------------
    # 2. PRODUTOS / ESTOQUE (35 registros)
    # ----------------------------------------------------------------
    produtos_raw = [
        # (nome, qtd_estoque, unidade, data_validade, fornecedor)
        ("Racao Bovino Engorda",      "1500.00", "kg",   date(2027, 3, 15), "AgroNutri Ltda"),
        ("Racao Bovino Cria",         "800.00",  "kg",   date(2027, 1, 20), "AgroNutri Ltda"),
        ("Silagem de Milho",          "5000.00", "kg",   date(2026, 12, 31),"Fazenda Boa Vista"),
        ("Capim Napier Fardo",        "300.00",  "un",   date(2026, 9, 10), "Pastagens do Sul"),
        ("Farelo de Soja",            "900.00",  "kg",   date(2027, 2, 28), "Cooperativa Grao Verde"),
        ("Sal Mineral Bovino",        "450.00",  "kg",   date(2027, 6, 30), "MineralPet Ind"),
        ("Suplemento Vitaminico A+D", "120.00",  "L",    date(2027, 4, 10), "VetSupri SA"),
        ("Calcario Calcitico",        "2000.00", "kg",   date(2028, 1, 1),  "Calcario Central"),
        ("Milho Grao",                "3500.00", "kg",   date(2026, 11, 15),"Cooperativa Grao Verde"),
        ("Bagaco de Cana",            "1200.00", "kg",   date(2026, 8, 20), "Usina Alegria"),
        ("Torta de Algodao",          "600.00",  "kg",   date(2026, 10, 5), "AgroNutri Ltda"),
        ("Ureia Pecuaria 45%",        "200.00",  "kg",   date(2027, 5, 20), "FertiAgro Brasil"),
        ("Probiotico Bovino",         "50.00",   "L",    date(2026, 12, 10),"VetSupri SA"),
        ("Ivermectina 1%",            "30.00",   "L",    date(2026, 9, 30), "VetPharma Ind"),
        ("Vacina Aftosa Polivalente", "500.00",  "dose", date(2026, 7, 31), "Vallee SA"),
        ("Vacina Brucelose B19",      "200.00",  "dose", date(2026, 8, 15), "Zoetis Brasil"),
        ("Vacina Raiva Bovina",       "150.00",  "dose", date(2026, 10, 20),"Boehringer Ingelheim"),
        ("Vacina Clostridioses",      "180.00",  "dose", date(2027, 1, 10), "Vallee SA"),
        ("Oxitetraciclina 200mg",     "60.00",   "L",    date(2026, 11, 25),"VetPharma Ind"),
        ("Florfenicol 30%",           "40.00",   "L",    date(2027, 3, 5),  "Zoetis Brasil"),
        ("Dipirona Sodica 50%",       "20.00",   "L",    date(2026, 8, 30), "VetPharma Ind"),
        ("Dexametasona 2mg",          "15.00",   "L",    date(2026, 9, 15), "MSD Saude Animal"),
        ("Albendazol 10%",            "80.00",   "L",    date(2027, 2, 10), "Eurofarma Vet"),
        ("Doramectina 1%",            "25.00",   "L",    date(2026, 12, 20),"Zoetis Brasil"),
        ("Penicilina G 20M UI",       "100.00",  "fr",   date(2026, 10, 15),"VetPharma Ind"),
        ("Enrofloxacina 10%",         "35.00",   "L",    date(2027, 4, 25), "MSD Saude Animal"),
        ("Sulfato de Magnesio",       "250.00",  "kg",   date(2028, 6, 1),  "FertiAgro Brasil"),
        ("Soro Fisiologico 0,9%",     "500.00",  "L",    date(2026, 11, 5), "Fresenius Kabi"),
        ("Ringer Lactato",            "200.00",  "L",    date(2027, 1, 30), "Fresenius Kabi"),
        ("Agulha Descartavel 40x12",  "1000.00", "un",   date(2029, 1, 1),  "BD Medical"),
        ("Seringa 20mL",              "500.00",  "un",   date(2029, 6, 1),  "BD Medical"),
        ("Bolsa Colostro Congelado",  "80.00",   "un",   date(2026, 7, 20), "Banco Colostro RS"),
        ("Esperma Bovino Sexado",     "40.00",   "dose", date(2026, 12, 15),"Central Genetica BR"),
        ("Hormonio GnRH",             "20.00",   "L",    date(2026, 8, 25), "Zoetis Brasil"),
        ("Prostaglandina F2alfa",     "18.00",   "L",    date(2026, 9, 5),  "MSD Saude Animal"),
    ]

    produtos = []
    for nome, qtd, un, validade, forn in produtos_raw:
        p = Produto.objects.create(
            nome=nome,
            quantidade_estoque=Decimal(qtd),
            unidade_medida=un,
            data_validade=validade,
            fornecedor=forn,
            ativo=True,
        )
        produtos.append(p)

    # ----------------------------------------------------------------
    # 3. TALHOES (8 registros — maximo 10)
    # ----------------------------------------------------------------
    talhoes_raw = [
        # (nome, localizacao, capacidade, area_total)
        ("Talhao Norte",      "Setor norte da propriedade",         120, "85.50"),
        ("Talhao Sul",        "Setor sul proximo ao rio",            90, "62.00"),
        ("Talhao Leste",      "Divisa leste, pastagem nativa",       80, "55.75"),
        ("Talhao Oeste",      "Proximo a estrada principal",        100, "70.00"),
        ("Talhao Central",    "Area central, irrigada",             150, "98.00"),
        ("Talhao da Represa", "Margem da represa, capim elefante",   60, "42.30"),
        ("Talhao do Brejo",   "Area alagavel, uso sazonal",          40, "28.00"),
        ("Talhao da Serra",   "Area elevada, pastagem de sequeiro",  70, "51.20"),
    ]

    talhoes = []
    for nome, loc, cap, area in talhoes_raw:
        t = Talhao.objects.create(
            nome=nome,
            localizacao=loc,
            capacidade=cap,
            area_total=Decimal(area),
            ativo=True,
        )
        talhoes.append(t)

    # ----------------------------------------------------------------
    # 4. REBANHOS (8 registros — 1 por talhao)
    # ----------------------------------------------------------------
    rebanhos_raw = [
        # (nome, tipo_criacao) — index = talhao index; quantidade_animais calculada após inserir animais
        ("Rebanho Bovino Norte",  "Nelore"),
        ("Rebanho Bovino Sul",    "Angus"),
        ("Rebanho Misto Leste",   "Nelore x Angus"),
        ("Rebanho Zebuino Oeste", "Gir Leiteiro"),
        ("Rebanho Central Elite", "Brahman"),
        ("Rebanho da Represa",    "Simental"),
        ("Rebanho do Brejo",      "Caracu"),
        ("Rebanho da Serra",      "Nelore"),
    ]

    rebanhos = []
    for i, (nome, tipo) in enumerate(rebanhos_raw):
        r = Rebanho.objects.create(
            talhao=talhoes[i],
            nome=nome,
            quantidade_animais=0,
            tipo_criacao=tipo,
            ativo=True,
        )
        rebanhos.append(r)

    # ----------------------------------------------------------------
    # 5. ANIMAIS (35 registros)
    # ----------------------------------------------------------------
    # (identificacao, raca, sexo, data_nascimento, peso, status_saude, rebanho_idx)
    animais_raw = [
        ("FAZ-001", "Nelore",         "Macho",  date(2022, 3, 10), "480.00", "Saudavel",   0),
        ("FAZ-002", "Nelore",         "Femea",  date(2021, 7, 22), "380.00", "Saudavel",   0),
        ("FAZ-003", "Nelore",         "Femea",  date(2023, 1, 5),  "290.00", "Saudavel",   0),
        ("FAZ-004", "Angus",          "Macho",  date(2020, 11, 18),"540.00", "Saudavel",   1),
        ("FAZ-005", "Angus",          "Femea",  date(2022, 5, 30), "410.00", "Observacao", 1),
        ("FAZ-006", "Angus",          "Macho",  date(2021, 9, 14), "510.00", "Saudavel",   1),
        ("FAZ-007", "Nelore x Angus", "Femea",  date(2023, 4, 2),  "320.00", "Saudavel",   2),
        ("FAZ-008", "Nelore x Angus", "Macho",  date(2022, 8, 19), "460.00", "Tratamento", 2),
        ("FAZ-009", "Nelore x Angus", "Femea",  date(2021, 12, 7), "390.00", "Saudavel",   2),
        ("FAZ-010", "Gir Leiteiro",   "Femea",  date(2020, 6, 25), "430.00", "Saudavel",   3),
        ("FAZ-011", "Gir Leiteiro",   "Femea",  date(2021, 2, 14), "410.00", "Saudavel",   3),
        ("FAZ-012", "Gir Leiteiro",   "Macho",  date(2019, 10, 3), "580.00", "Saudavel",   3),
        ("FAZ-013", "Brahman",        "Macho",  date(2022, 1, 28), "520.00", "Saudavel",   4),
        ("FAZ-014", "Brahman",        "Femea",  date(2021, 8, 11), "400.00", "Observacao", 4),
        ("FAZ-015", "Brahman",        "Femea",  date(2023, 6, 3),  "280.00", "Saudavel",   4),
        ("FAZ-016", "Brahman",        "Macho",  date(2020, 4, 17), "560.00", "Saudavel",   4),
        ("FAZ-017", "Brahman",        "Femea",  date(2022, 11, 22),"390.00", "Tratamento", 4),
        ("FAZ-018", "Simental",       "Macho",  date(2021, 3, 9),  "610.00", "Saudavel",   5),
        ("FAZ-019", "Simental",       "Femea",  date(2022, 7, 1),  "450.00", "Saudavel",   5),
        ("FAZ-020", "Simental",       "Femea",  date(2020, 9, 30), "430.00", "Saudavel",   5),
        ("FAZ-021", "Caracu",         "Macho",  date(2023, 2, 15), "300.00", "Saudavel",   6),
        ("FAZ-022", "Caracu",         "Femea",  date(2022, 6, 20), "360.00", "Critico",    6),
        ("FAZ-023", "Nelore",         "Macho",  date(2021, 10, 8), "490.00", "Saudavel",   7),
        ("FAZ-024", "Nelore",         "Femea",  date(2022, 4, 12), "370.00", "Saudavel",   7),
        ("FAZ-025", "Nelore",         "Femea",  date(2020, 12, 25),"400.00", "Saudavel",   7),
        ("FAZ-026", "Angus",          "Femea",  date(2023, 3, 7),  "310.00", "Saudavel",   1),
        ("FAZ-027", "Gir Leiteiro",   "Femea",  date(2021, 5, 16), "420.00", "Observacao", 3),
        ("FAZ-028", "Brahman",        "Macho",  date(2022, 9, 4),  "530.00", "Saudavel",   4),
        ("FAZ-029", "Nelore",         "Femea",  date(2020, 7, 13), "410.00", "Saudavel",   0),
        ("FAZ-030", "Nelore x Angus", "Femea",  date(2023, 5, 21), "270.00", "Saudavel",   2),
        ("FAZ-031", "Brahman",        "Femea",  date(2021, 1, 29), "395.00", "Saudavel",   4),
        ("FAZ-032", "Simental",       "Macho",  date(2019, 8, 6),  "640.00", "Saudavel",   5),
        ("FAZ-033", "Caracu",         "Femea",  date(2022, 12, 18),"355.00", "Tratamento", 6),
        ("FAZ-034", "Angus",          "Macho",  date(2021, 4, 23), "495.00", "Saudavel",   1),
        ("FAZ-035", "Gir Leiteiro",   "Femea",  date(2020, 2, 10), "440.00", "Saudavel",   3),
    ]

    hoje = date(2026, 6, 24)
    animais = []
    for ident, raca, sexo, dn, peso, status, rb_idx in animais_raw:
        idade = (hoje - dn).days // 30
        a = Animal.objects.create(
            rebanho=rebanhos[rb_idx],
            identificacao=ident,
            raca=raca,
            sexo=sexo,
            data_nascimento=dn,
            idade=idade,
            peso=Decimal(peso),
            status_saude=status,
            ativo=True,
        )
        animais.append(a)

    for r in rebanhos:
        r.quantidade_animais = r.animais.count()
        r.save(update_fields=["quantidade_animais"])

    # ----------------------------------------------------------------
    # 6. ALIMENTOS (35 registros)
    # ----------------------------------------------------------------
    # (rebanho_idx, produto_idx_or_None, nome, tipo, quantidade, data_fornecimento)
    alimentos_raw = [
        (0, 0,    "Racao Engorda Lote A",   "Concentrado", "150.00", date(2026, 6, 20)),
        (0, 2,    "Silagem Manha",          "Volumoso",    "800.00", date(2026, 6, 21)),
        (0, 5,    "Sal Mineral Semanal",    "Mineral",     "45.00",  date(2026, 6, 18)),
        (1, 0,    "Racao Engorda Lote B",   "Concentrado", "120.00", date(2026, 6, 22)),
        (1, 4,    "Farelo de Soja",         "Concentrado", "90.00",  date(2026, 6, 19)),
        (1, 3,    "Capim Fardo Tarde",      "Volumoso",    "50.00",  date(2026, 6, 23)),
        (2, 2,    "Silagem Tarde",          "Volumoso",    "600.00", date(2026, 6, 21)),
        (2, 5,    "Suplemento Mineral",     "Mineral",     "30.00",  date(2026, 6, 20)),
        (2, 8,    "Milho Grao Moido",       "Concentrado", "200.00", date(2026, 6, 17)),
        (3, 1,    "Racao Cria Manha",       "Concentrado", "80.00",  date(2026, 6, 22)),
        (3, 5,    "Sal Mineral Lote Gir",   "Mineral",     "40.00",  date(2026, 6, 16)),
        (3, 9,    "Bagaco de Cana",         "Volumoso",    "500.00", date(2026, 6, 14)),
        (4, 0,    "Racao Brahman Elite",    "Concentrado", "300.00", date(2026, 6, 23)),
        (4, 4,    "Farelo Soja Novilhas",   "Concentrado", "180.00", date(2026, 6, 21)),
        (4, 2,    "Silagem Central",        "Volumoso",    "1200.00",date(2026, 6, 20)),
        (4, 7,    "Calcario Pasto",         "Mineral",     "50.00",  date(2026, 6, 15)),
        (5, 0,    "Racao Simental",         "Concentrado", "180.00", date(2026, 6, 22)),
        (5, 3,    "Capim Fardo Noite",      "Volumoso",    "60.00",  date(2026, 6, 23)),
        (5, 6,    "Suplemento Vitaminico",  "Suplemento",  "10.00",  date(2026, 6, 18)),
        (6, 1,    "Racao Cria Caracu",      "Concentrado", "50.00",  date(2026, 6, 22)),
        (6, None, "Capim Nativo Picado",    "Volumoso",    "300.00", date(2026, 6, 21)),
        (7, 0,    "Racao Serra Lote A",     "Concentrado", "140.00", date(2026, 6, 23)),
        (7, 2,    "Silagem Serra",          "Volumoso",    "700.00", date(2026, 6, 20)),
        (7, 5,    "Mineral Serra",          "Mineral",     "35.00",  date(2026, 6, 19)),
        (0, 10,   "Torta de Algodao",       "Concentrado", "100.00", date(2026, 6, 10)),
        (1, 11,   "Ureia Pecuaria",         "Concentrado", "20.00",  date(2026, 6, 5)),
        (2, 4,    "Farelo Soja Misto",      "Concentrado", "110.00", date(2026, 6, 12)),
        (3, 8,    "Milho Grao Gir",         "Concentrado", "160.00", date(2026, 6, 8)),
        (4, 9,    "Bagaco Cana Central",    "Volumoso",    "800.00", date(2026, 6, 6)),
        (5, None, "Palhada de Soja",        "Volumoso",    "400.00", date(2026, 6, 4)),
        (6, 5,    "Mineral Brejo",          "Mineral",     "20.00",  date(2026, 6, 3)),
        (0, None, "Pasto Rotacionado",      "Volumoso",    "0.00",   date(2026, 5, 30)),
        (1, 6,    "Vitaminas Angus",        "Suplemento",  "8.00",   date(2026, 5, 28)),
        (3, 12,   "Probiotico Gir",         "Suplemento",  "5.00",   date(2026, 5, 25)),
        (4, 7,    "Calcario Central 2",     "Mineral",     "60.00",  date(2026, 5, 20)),
    ]

    for rb_idx, prod_idx, nome, tipo, qtd, data_f in alimentos_raw:
        produto = produtos[prod_idx] if prod_idx is not None else None
        Alimento.objects.create(
            rebanho=rebanhos[rb_idx],
            produto=produto,
            nome=nome,
            tipo=tipo,
            quantidade=Decimal(qtd),
            data_fornecimento=data_f,
            ativo=True,
        )

    # ----------------------------------------------------------------
    # 7. SANIDADES (35 registros — 1 por animal)
    # ----------------------------------------------------------------
    status_map = {
        "Saudavel":   "Saudavel",
        "Observacao": "Em observacao",
        "Tratamento": "Em tratamento",
        "Critico":    "Critico",
    }

    sanidades = []
    for animal in animais:
        san_status = status_map.get(animal.status_saude, "Saudavel")
        s = Sanidade.objects.create(
            animal=animal,
            data_registro=date(2026, 6, 24),
            status_sanitario=san_status,
            observacoes="Registro sanitario inicial do animal " + animal.identificacao + ".",
            criado_por=usuario,
        )
        sanidades.append(s)

    # ----------------------------------------------------------------
    # 8. EXAMES (20 registros)
    # ----------------------------------------------------------------
    # (sanidade_idx, nome, tipo, data_realizacao, resultado, status)
    exames_raw = [
        (0,  "Hemograma Completo",     "Laboratorial", date(2026, 6, 10), "Valores normais",            "Concluido"),
        (1,  "Brucelose BAB",          "Sorologico",   date(2026, 5, 15), "Negativo",                   "Concluido"),
        (2,  "Tuberculose PPD",        "Intradermico", date(2026, 4, 20), "Negativo",                   "Concluido"),
        (3,  "Hemograma",              "Laboratorial", date(2026, 6, 5),  "Anemia leve identificada",   "Concluido"),
        (4,  "Exame Parasitologico",   "OPG",          date(2026, 5, 30), "1200 OPG - Tratamento req.", "Concluido"),
        (5,  "Hemograma",              "Laboratorial", date(2026, 6, 1),  "Valores normais",            "Concluido"),
        (6,  "Brucelose BAB",          "Sorologico",   date(2026, 3, 10), "Negativo",                   "Concluido"),
        (7,  "Exame de Fezes",         "Laboratorial", date(2026, 6, 15), "Positivo para Eimeria",      "Concluido"),
        (8,  "Hemograma Completo",     "Laboratorial", date(2026, 4, 5),  "Valores normais",            "Concluido"),
        (9,  "California Mastite CMT", "CMT",          date(2026, 6, 18), "Negativo",                   "Concluido"),
        (10, "Brucelose BAB",          "Sorologico",   date(2026, 5, 20), "Negativo",                   "Concluido"),
        (11, "Hemograma",              "Laboratorial", date(2026, 3, 25), "Valores normais",            "Concluido"),
        (12, "Exame Parasitologico",   "OPG",          date(2026, 6, 12), "800 OPG - Limite aceitavel", "Concluido"),
        (13, "Hemograma Completo",     "Laboratorial", date(2026, 6, 20), "Leucocitose detectada",      "Concluido"),
        (14, "Brucelose BAB",          "Sorologico",   date(2026, 4, 15), "Negativo",                   "Concluido"),
        (15, "Hemograma",              "Laboratorial", date(2026, 5, 10), "Valores normais",            "Concluido"),
        (16, "Exame de Fezes",         "Laboratorial", date(2026, 6, 22), "Presenca de vermes",         "Concluido"),
        (20, "Hemograma Completo",     "Laboratorial", date(2026, 6, 16), "Valores criticos",           "Concluido"),
        (21, "Tuberculose PPD",        "Intradermico", date(2026, 5, 5),  "Negativo",                   "Concluido"),
        (32, "Exame Parasitologico",   "OPG",          date(2026, 6, 18), "600 OPG - Normal",           "Concluido"),
    ]

    for s_idx, nome, tipo, data_r, resultado, status in exames_raw:
        Exame.objects.create(
            sanidade=sanidades[s_idx],
            nome=nome,
            tipo=tipo,
            data_realizacao=data_r,
            resultado=resultado,
            status=status,
        )

    # ----------------------------------------------------------------
    # 9. VACINAS (20 registros)
    # ----------------------------------------------------------------
    # (sanidade_idx, nome, dose, data_aplicacao, proxima_dose, status)
    vacinas_raw = [
        (0,  "Aftosa Polivalente", "2a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (1,  "Aftosa Polivalente", "1a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (2,  "Clostridioses",      "Reforco",  date(2026, 3, 10), date(2026, 9, 10),  "Aplicada"),
        (3,  "Aftosa Polivalente", "2a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (4,  "Raiva Bovina",       "Anual",    date(2026, 2, 20), date(2027, 2, 20),  "Aplicada"),
        (5,  "Clostridioses",      "Reforco",  date(2026, 4, 5),  date(2026, 10, 5),  "Aplicada"),
        (6,  "Brucelose B19",      "Unica",    date(2023, 7, 1),  None,               "Aplicada"),
        (7,  "Aftosa Polivalente", "1a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (8,  "Raiva Bovina",       "Anual",    date(2025, 6, 10), date(2026, 6, 10),  "Vencida"),
        (9,  "Brucelose B19",      "Unica",    date(2022, 4, 12), None,               "Aplicada"),
        (10, "Clostridioses",      "1a dose",  date(2026, 1, 20), date(2026, 7, 20),  "Aplicada"),
        (11, "Aftosa Polivalente", "2a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (12, "Raiva Bovina",       "Anual",    date(2025, 8, 25), date(2026, 8, 25),  "Aplicada"),
        (13, "Aftosa Polivalente", "1a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (14, "Clostridioses",      "Reforco",  date(2026, 3, 30), date(2026, 9, 30),  "Aplicada"),
        (16, "Aftosa Polivalente", "2a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
        (17, "Raiva Bovina",       "Anual",    date(2026, 1, 15), date(2027, 1, 15),  "Aplicada"),
        (18, "Clostridioses",      "1a dose",  date(2025, 12, 5), date(2026, 6, 5),   "Vencida"),
        (22, "Clostridioses",      "Reforco",  date(2026, 4, 10), date(2026, 10, 10), "Aplicada"),
        (33, "Aftosa Polivalente", "2a dose",  date(2026, 5, 15), date(2026, 11, 15), "Aplicada"),
    ]

    for s_idx, nome, dose, data_a, prox, status in vacinas_raw:
        Vacina.objects.create(
            sanidade=sanidades[s_idx],
            nome=nome,
            dose=dose,
            data_aplicacao=data_a,
            proxima_dose=prox,
            status=status,
        )

    # ----------------------------------------------------------------
    # 10. MEDICAMENTOS (15 registros)
    # ----------------------------------------------------------------
    # (sanidade_idx, nome, dosagem, periodo_tratamento, data_inicio, data_fim)
    medicamentos_raw = [
        (4,  "Ivermectina 1%",        "1 mL/50kg SC",   "Dose unica", date(2026, 5, 30), date(2026, 5, 30)),
        (7,  "Sulfato de Zinco",      "50mg/kg VO",      "7 dias",     date(2026, 6, 15), date(2026, 6, 22)),
        (8,  "Clostridioses Reforco", "2 mL SC",         "Dose unica", date(2026, 6, 1),  date(2026, 6, 1)),
        (13, "Oxitetraciclina 200mg", "10 mL IM",        "3 dias",     date(2026, 6, 20), date(2026, 6, 23)),
        (16, "Albendazol 10%",        "1 mL/10kg VO",    "Dose unica", date(2026, 6, 22), date(2026, 6, 22)),
        (17, "Dexametasona 2mg",      "5 mL IM",         "3 dias",     date(2026, 6, 18), date(2026, 6, 21)),
        (20, "Florfenicol 30%",       "20 mL/100kg IM",  "2 doses",    date(2026, 6, 16), date(2026, 6, 18)),
        (20, "Dipirona Sodica 50%",   "10 mL IV",        "Conforme dor",date(2026, 6, 16),date(2026, 6, 20)),
        (21, "Penicilina G 20M UI",   "20000 UI/kg IM",  "5 dias",     date(2026, 6, 10), date(2026, 6, 15)),
        (22, "Doramectina 1%",        "1 mL/50kg SC",    "Dose unica", date(2026, 6, 16), date(2026, 6, 16)),
        (26, "Enrofloxacina 10%",     "5 mL/100kg SC",   "3-5 dias",   date(2026, 5, 30), date(2026, 6, 4)),
        (27, "Ivermectina 1%",        "1 mL/50kg SC",    "Dose unica", date(2026, 6, 12), date(2026, 6, 12)),
        (30, "Oxitetraciclina 200mg", "10 mL IM",        "3 dias",     date(2026, 6, 15), date(2026, 6, 18)),
        (32, "Albendazol 10%",        "1 mL/10kg VO",    "Dose unica", date(2026, 6, 18), date(2026, 6, 18)),
        (34, "Florfenicol 30%",       "15 mL/100kg IM",  "2 doses",    date(2026, 6, 20), date(2026, 6, 22)),
    ]

    for s_idx, nome, dosagem, periodo, di, df in medicamentos_raw:
        Medicamento.objects.create(
            sanidade=sanidades[s_idx],
            nome=nome,
            dosagem=dosagem,
            periodo_tratamento=periodo,
            data_inicio=di,
            data_fim=df,
        )

    # ----------------------------------------------------------------
    # 11. ENFERMIDADES (10 registros)
    # ----------------------------------------------------------------
    # (sanidade_idx, nome, descricao, data_diagnostico, gravidade, status_tratamento)
    enfermidades_raw = [
        (4,  "Verminose",         "Alta carga parasitaria identificada em exame OPG",
              date(2026, 5, 30), "Moderada", "Em tratamento"),
        (7,  "Eimeriose",         "Coccidiose bovina, presenca de Eimeria spp.",
              date(2026, 6, 15), "Leve",     "Em tratamento"),
        (13, "Pneumonia",         "Pneumonia bacteriana, tosse produtiva e febre 40C",
              date(2026, 6, 20), "Severa",   "Em tratamento"),
        (16, "Verminose",         "OPG elevado, emagrecimento progressivo",
              date(2026, 6, 22), "Moderada", "Em tratamento"),
        (17, "Mastite Subclinica","CMT positivo, queda na producao leiteira",
              date(2026, 6, 18), "Leve",     "Em tratamento"),
        (20, "Febre Catarral",    "Febre, mucosas congestionadas, secrecao nasal",
              date(2026, 6, 16), "Critica",  "Em tratamento"),
        (21, "Actinomicose",      "Inchaço mandibular, fistula com secrecao",
              date(2026, 6, 10), "Moderada", "Em tratamento"),
        (22, "Timpanismo",        "Distensao abdominal esquerda recorrente",
              date(2026, 6, 16), "Critica",  "Em tratamento"),
        (30, "Diarreia Neonatal", "Diarreia profusa, desidratacao moderada",
              date(2026, 6, 15), "Leve",     "Em tratamento"),
        (32, "Verminose",         "Exame OPG com carga parasitaria controlavel",
              date(2026, 6, 18), "Leve",     "Recuperado"),
    ]

    for s_idx, nome, desc, data_d, grav, status_t in enfermidades_raw:
        Enfermidade.objects.create(
            sanidade=sanidades[s_idx],
            nome=nome,
            descricao=desc,
            data_diagnostico=data_d,
            gravidade=grav,
            status_tratamento=status_t,
        )


def reverter_dados_iniciais(apps, schema_editor):
    Enfermidade = apps.get_model("rebanho", "Enfermidade")
    Medicamento = apps.get_model("rebanho", "Medicamento")
    Vacina      = apps.get_model("rebanho", "Vacina")
    Exame       = apps.get_model("rebanho", "Exame")
    Sanidade    = apps.get_model("rebanho", "Sanidade")
    Alimento    = apps.get_model("rebanho", "Alimento")
    Animal      = apps.get_model("rebanho", "Animal")
    Rebanho     = apps.get_model("rebanho", "Rebanho")
    Talhao      = apps.get_model("rebanho", "Talhao")
    Produto     = apps.get_model("rebanho", "Produto")
    Usuario     = apps.get_model("rebanho", "Usuario")

    Enfermidade.objects.all().delete()
    Medicamento.objects.all().delete()
    Vacina.objects.all().delete()
    Exame.objects.all().delete()
    Sanidade.objects.all().delete()
    Alimento.objects.all().delete()
    Animal.objects.all().delete()
    Rebanho.objects.all().delete()
    Talhao.objects.all().delete()
    Produto.objects.all().delete()
    Usuario.objects.filter(username="admin_fazenda").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("rebanho", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(criar_dados_iniciais, reverter_dados_iniciais),
    ]
