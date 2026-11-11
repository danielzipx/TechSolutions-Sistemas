"""Casos de teste CT01 a CT20 do controle de equipamentos (pytest).

Como rodar, na mesma pasta do codigo.py:
    pip install pytest
    pytest -v caso_test.py

Cada teste traz no docstring a linha da tabela de casos de teste:
    ID | Funcionalidade | Entrada | Resultado esperado
"""

import pytest

import codigo as app  # <- se o seu arquivo tiver outro nome, troque aqui


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def estoque_limpo():
    """Cada teste começa (e termina) com o estoque vazio."""
    app.estoque.clear()
    yield
    app.estoque.clear()


@pytest.fixture
def executar_menu(monkeypatch, capsys):
    """Roda o menu simulando o teclado e devolve tudo o que foi impresso.

    Cada item da lista é a resposta a um input(). Termine sempre com "0".
    """
    def rodar(entradas):
        respostas = iter(entradas)

        def falso_input(prompt=""):
            resposta = next(respostas)
            print(f"{prompt}{resposta}")  # aparece na saída, ajuda a depurar
            return resposta

        monkeypatch.setattr("builtins.input", falso_input)
        app.menu()
        return capsys.readouterr().out

    return rodar


# ---------------------------------------------------------------------------
# CT01 a CT03 (casos do print)
# ---------------------------------------------------------------------------

def test_ct01_cadastro_dados_validos():
    """CT01 | Cadastro | Dados válidos | Cadastro realizado"""
    app.cadastrar_equipamento("A1", "Projetor", 3)

    assert len(app.estoque) == 1
    assert app.estoque[0].nome == "Projetor"
    assert app.consultar_quantidade("A1") == 3


def test_ct02_emprestimo_estoque_disponivel():
    """CT02 | Empréstimo | Estoque disponível | Sucesso"""
    app.cadastrar_equipamento("A1", "Projetor", 3)

    assert app.emprestar_equipamento("A1") is True
    assert app.consultar_quantidade("A1") == 2


def test_ct03_emprestimo_estoque_zerado():
    """CT03 | Empréstimo | Estoque zerado | Falha"""
    app.cadastrar_equipamento("A1", "Projetor", 0)

    assert app.emprestar_equipamento("A1") is False
    assert app.consultar_quantidade("A1") == 0  # nunca fica negativo


# ---------------------------------------------------------------------------
# CT04 a CT10
# ---------------------------------------------------------------------------

def test_ct04_emprestimo_codigo_inexistente():
    """CT04 | Empréstimo | Código inexistente | Falha, estoque não muda"""
    app.cadastrar_equipamento("A1", "Projetor", 3)

    assert app.emprestar_equipamento("XYZ") is False
    assert app.consultar_quantidade("A1") == 3


def test_ct05_devolucao_equipamento_emprestado():
    """CT05 | Devolução | Equipamento emprestado | Sucesso, quantidade volta"""
    app.cadastrar_equipamento("A1", "Projetor", 2)
    app.emprestar_equipamento("A1")
    assert app.consultar_quantidade("A1") == 1

    assert app.devolver_equipamento("A1") is True
    assert app.consultar_quantidade("A1") == 2


def test_ct06_devolucao_codigo_inexistente():
    """CT06 | Devolução | Código inexistente | Falha"""
    assert app.devolver_equipamento("XYZ") is False
    assert app.estoque == []


def test_ct07_consulta_codigo_existente():
    """CT07 | Consulta | Código existente | Retorna a quantidade atual"""
    app.cadastrar_equipamento("A1", "Projetor", 5)

    quantidade = app.consultar_quantidade("A1")

    assert quantidade == 5
    assert isinstance(quantidade, int)


def test_ct08_consulta_codigo_inexistente():
    """CT08 | Consulta | Código inexistente | Retorna None (e não 0)"""
    app.cadastrar_equipamento("B2", "Cabo HDMI", 0)

    assert app.consultar_quantidade("XYZ") is None
    assert app.consultar_quantidade("B2") == 0  # existe, só está sem unidades


def test_ct09_menu_cadastro_codigo_duplicado(executar_menu):
    """CT09 | Cadastro (menu) | Código duplicado | Recusa com mensagem"""
    saida = executar_menu([
        "1", "A1", "Projetor", "3",   # cadastra
        "1", "A1",                    # tenta o mesmo código
        "0",
    ])

    assert "Já existe um equipamento com esse código." in saida
    assert len(app.estoque) == 1


def test_ct10_menu_cadastro_quantidade_invalida(executar_menu):
    """CT10 | Cadastro (menu) | Quantidade inválida ("abc") | Pede de novo, sem quebrar"""
    saida = executar_menu([
        "1", "A1", "Projetor", "abc",  # entrada inválida
        "3",                           # o menu deve pedir de novo
        "0",
    ])

    assert "Entrada inválida" in saida
    assert app.consultar_quantidade("A1") == 3


# ---------------------------------------------------------------------------
# CT11 a CT20 (novos)
# ---------------------------------------------------------------------------

def test_ct11_menu_cadastro_quantidade_negativa(executar_menu):
    """CT11 | Cadastro (menu) | Quantidade negativa ("-5") | Recusa e pede de novo"""
    executar_menu([
        "1", "A1", "Projetor", "-5",   # inválida
        "3",                           # válida
        "0",
    ])

    assert app.consultar_quantidade("A1") == 3


def test_ct12_devolucao_sem_emprestimo_nao_passa_do_total():
    """CT12 | Devolução | Nada emprestado | Falha, quantidade não passa do cadastrado"""
    app.cadastrar_equipamento("A1", "Projetor", 3)

    assert app.devolver_equipamento("A1") is False
    assert app.consultar_quantidade("A1") == 3


def test_ct13_menu_devolucao_sem_emprestimo(executar_menu):
    """CT13 | Devolução (menu) | Nada emprestado | Mensagem clara, sem "sucesso" """
    saida = executar_menu([
        "1", "A1", "Projetor", "3",
        "3", "A1",
        "0",
    ])

    assert "Todas as unidades já estão no estoque" in saida
    assert "Devolução registrada com sucesso" not in saida
    assert app.consultar_quantidade("A1") == 3


def test_ct14_cadastro_codigo_duplicado_pela_funcao():
    """CT14 | Cadastro | Código duplicado (função) | Falha, o original é mantido"""
    assert app.cadastrar_equipamento("A1", "Projetor", 3) is True
    assert app.cadastrar_equipamento("A1", "Outro", 5) is False

    assert len(app.estoque) == 1
    assert app.estoque[0].nome == "Projetor"
    assert app.consultar_quantidade("A1") == 3


def test_ct15_cadastro_quantidade_negativa_pela_funcao():
    """CT15 | Cadastro | Quantidade negativa (função) | Falha, nada é cadastrado"""
    assert app.cadastrar_equipamento("A1", "Projetor", -5) is False
    assert app.estoque == []


def test_ct16_ciclo_emprestar_e_devolver_tudo():
    """CT16 | Empréstimo/Devolução | Emprestar e devolver todas | Volta ao total"""
    app.cadastrar_equipamento("A1", "Projetor", 2)

    assert app.emprestar_equipamento("A1") is True
    assert app.emprestar_equipamento("A1") is True
    assert app.emprestar_equipamento("A1") is False   # acabou
    assert app.consultar_quantidade("A1") == 0

    assert app.devolver_equipamento("A1") is True
    assert app.devolver_equipamento("A1") is True
    assert app.devolver_equipamento("A1") is False    # já está tudo de volta
    assert app.consultar_quantidade("A1") == 2


def test_ct17_menu_cadastro_nome_vazio(executar_menu):
    """CT17 | Cadastro (menu) | Nome só com espaços | Recusa com mensagem"""
    saida = executar_menu([
        "1", "A1", "   ",
        "0",
    ])

    assert "O nome não pode ser vazio." in saida
    assert app.estoque == []


@pytest.mark.parametrize("erro", [EOFError, KeyboardInterrupt])
def test_ct18_menu_encerra_com_ctrl_c_ou_ctrl_d(monkeypatch, capsys, erro):
    """CT18 | Menu | Ctrl+C ou Ctrl+D | Encerra com mensagem, sem erro na tela"""
    def input_com_erro(prompt=""):
        raise erro

    monkeypatch.setattr("builtins.input", input_com_erro)

    app.menu()  # não deve levantar exceção

    assert "Encerrando o programa" in capsys.readouterr().out


def test_ct19_menu_opcao_invalida(executar_menu):
    """CT19 | Menu | Opção inexistente ("9") | "Opção inválida" e o menu continua"""
    saida = executar_menu(["9", "0"])

    assert "Opção inválida" in saida
    assert "Até logo" in saida


def test_ct20_menu_listar_e_consultar(executar_menu):
    """CT20 | Listar/Consultar (menu) | Item existente e inexistente | Mostra dados ou aviso"""
    saida = executar_menu([
        "1", "A1", "Projetor", "3",
        "5",                  # listar
        "4", "A1",            # consultar existente
        "4", "XYZ",           # consultar inexistente
        "0",
    ])

    assert "Projetor" in saida
    assert "Quantidade disponível: 3" in saida
    assert "Equipamento não encontrado." in saida
