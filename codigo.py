import csv
import os

ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "estoque.csv")
CAMPOS = ["codigo", "nome", "quantidade"]


class Equipamento:
    def __init__(self, codigo, nome, quantidade):
        self.codigo = codigo
        self.nome = nome
        self.quantidade = quantidade          # unidades disponíveis agora
        self.quantidade_total = quantidade    # total cadastrado (limite da devolução)


estoque = []


# ---------------------------------------------------------------------------
# Funções do estoque
# ---------------------------------------------------------------------------

def _buscar(codigo):
    for equipamento in estoque:
        if equipamento.codigo == codigo:
            return equipamento
    return None


def cadastrar_equipamento(codigo, nome, quantidade):
    """Cadastra um equipamento. Retorna True se cadastrou, False se recusou
    (código ou nome vazio, quantidade inválida/negativa ou código já existente)."""
    if not codigo or not nome:
        return False
    if not isinstance(quantidade, int) or quantidade < 0:
        return False
    if _buscar(codigo) is not None:
        return False
    estoque.append(Equipamento(codigo, nome, quantidade))
    return True


def emprestar_equipamento(codigo):
    equipamento = _buscar(codigo)
    if equipamento is None or equipamento.quantidade <= 0:
        return False
    equipamento.quantidade -= 1
    return True


def devolver_equipamento(codigo):
    """Devolve 1 unidade. Falha se o código não existe ou se não há nada
    emprestado (a quantidade nunca passa do total cadastrado)."""
    equipamento = _buscar(codigo)
    if equipamento is None:
        return False
    if equipamento.quantidade >= equipamento.quantidade_total:
        return False
    equipamento.quantidade += 1
    return True


def consultar_quantidade(codigo):
    equipamento = _buscar(codigo)
    if equipamento is None:
        return None
    return equipamento.quantidade


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def ler_inteiro(mensagem, minimo=0):
    """Pede um número inteiro ao usuário até que seja válido."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return valor


def opcao_cadastrar():
    print("\n--- Cadastrar equipamento ---")
    codigo = input("Código: ").strip()
    if not codigo:
        print("O código não pode ser vazio.")
        return
    if consultar_quantidade(codigo) is not None:
        print("Já existe um equipamento com esse código.")
        return
    nome = input("Nome: ").strip()
    if not nome:
        print("O nome não pode ser vazio.")
        return
    quantidade = ler_inteiro("Quantidade: ")
    if cadastrar_equipamento(codigo, nome, quantidade):
        print(f"Equipamento '{nome}' cadastrado com sucesso!")
    else:
        print("Não foi possível cadastrar o equipamento.")


def opcao_emprestar():
    print("\n--- Emprestar equipamento ---")
    codigo = input("Código: ").strip()
    if emprestar_equipamento(codigo):
        print("Empréstimo realizado com sucesso!")
    elif consultar_quantidade(codigo) is None:
        print("Equipamento não encontrado.")
    else:
        print("Sem unidades disponíveis para empréstimo.")


def opcao_devolver():
    print("\n--- Devolver equipamento ---")
    codigo = input("Código: ").strip()
    if devolver_equipamento(codigo):
        print("Devolução registrada com sucesso!")
    elif consultar_quantidade(codigo) is None:
        print("Equipamento não encontrado.")
    else:
        print("Todas as unidades já estão no estoque; não há empréstimo a devolver.")


def opcao_consultar():
    print("\n--- Consultar quantidade ---")
    codigo = input("Código: ").strip()
    quantidade = consultar_quantidade(codigo)
    if quantidade is None:
        print("Equipamento não encontrado.")
    else:
        print(f"Quantidade disponível: {quantidade}")


def opcao_listar():
    print("\n--- Estoque atual ---")
    if not estoque:
        print("Nenhum equipamento cadastrado.")
        return
    print(f"{'Código':<12}{'Nome':<25}{'Qtd':>5}")
    print("-" * 42)
    for e in estoque:
        print(f"{e.codigo:<12}{e.nome:<25}{e.quantidade:>5}")


def menu():
    opcoes = {
        "1": opcao_cadastrar,
        "2": opcao_emprestar,
        "3": opcao_devolver,
        "4": opcao_consultar,
        "5": opcao_listar,
    }
    try:
        while True:
            print("\n===== CONTROLE DE EQUIPAMENTOS =====")
            print("1 - Cadastrar equipamento")
            print("2 - Emprestar equipamento")
            print("3 - Devolver equipamento")
            print("4 - Consultar quantidade")
            print("5 - Listar estoque")
            print("0 - Sair")
            escolha = input("Escolha uma opção: ").strip()

            if escolha == "0":
                print("Encerrando o programa. Até logo!")
                break
            acao = opcoes.get(escolha)
            if acao:
                acao()
            else:
                print("Opção inválida. Tente novamente.")
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrando o programa.")


if __name__ == "__main__":
    menu()
