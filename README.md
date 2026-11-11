# TechSolutions-Sistemas

Controle de Empréstimo

Programa de console, escrito em Python, que controla o estoque de equipamentos e registra empréstimos e devoluções por meio de um menu interativo. Desenvolvido pela equipe de suporte para a empresa cliente TechSolutions.

Sumário
Requisitos
Como executar
Funcionalidades
Regras de negócio
Estrutura do código
Limitações conhecidas
Testes
Solução de problemas
Histórico de alterações
Equipe
Requisitos
Python 3 (usa f-strings, portanto 3.6 ou superior)
Apenas a biblioteca padrão (csv e os); não há pacotes para instalar
Como executar

Não há instalação nem configuração. Com o Python 3 instalado:

Copie o arquivo codigo.py para uma pasta do computador.
Abra o terminal nessa pasta.
Execute:
bash
   python codigo.py
Use o menu digitando o número da opção e pressionando Enter. A opção 0 encerra o programa.
Funcionalidades

O menu Controle de Equipamentos oferece cinco operações e a opção de sair. Opções fora da lista exibem "Opção inválida" e o menu é mostrado de novo.

Opção	Operação	O que faz	Resultado informado ao usuário
1	Cadastrar equipamento	Pede código, nome e quantidade e adiciona o equipamento ao estoque	Sucesso, código vazio, nome vazio, código já existente ou falha no cadastro
2	Emprestar equipamento	Pede o código e retira 1 unidade do estoque disponível	Sucesso, equipamento não encontrado ou sem unidades disponíveis
3	Devolver equipamento	Pede o código e devolve 1 unidade ao estoque	Sucesso, equipamento não encontrado ou nenhuma unidade emprestada
4	Consultar quantidade	Pede o código e mostra a quantidade disponível	Quantidade disponível ou equipamento não encontrado
5	Listar estoque	Mostra uma tabela com código, nome e quantidade de todos os equipamentos	Tabela ou aviso de que nenhum equipamento está cadastrado
0	Sair	Encerra o programa	Mensagem de despedida

No cadastro, a tela confere os dados nesta ordem: código vazio, código já existente, nome vazio e, por último, a quantidade, que é pedida até ser um número inteiro válido.

Regras de negócio

Cada equipamento guarda duas quantidades: as unidades disponíveis agora e o total cadastrado, que serve de limite para as devoluções.

Cadastro

O código e o nome não podem ser vazios.
A quantidade deve ser um número inteiro maior ou igual a 0.
Não podem existir dois equipamentos com o mesmo código; a comparação diferencia maiúsculas de minúsculas.

Empréstimo

Retira 1 unidade por operação.
É recusado se o código não existe ou se não há unidades disponíveis.

Devolução

Devolve 1 unidade por operação.
É recusada se o código não existe ou se a quantidade disponível já é igual ao total cadastrado, ou seja, não há nada emprestado.

Entrada de dados

Espaços no início e no fim do texto digitado são ignorados.
Ctrl+C ou fim da entrada (Ctrl+D) encerram o programa com uma mensagem, sem erro.
Estrutura do código

O codigo.py separa a lógica do estoque, que só devolve resultados, das funções de menu, que conversam com o usuário e mostram as mensagens.

Elemento	Tipo	Descrição
Equipamento	Classe	Guarda código, nome, quantidade disponível e quantidade total cadastrada
estoque	Lista	Mantém em memória os equipamentos cadastrados
_buscar	Função	Procura um equipamento pelo código e retorna o equipamento ou None
cadastrar_equipamento	Função	Cadastra um equipamento; retorna True se cadastrou e False se recusou
emprestar_equipamento	Função	Retira 1 unidade; retorna True ou False
devolver_equipamento	Função	Devolve 1 unidade; retorna True ou False
consultar_quantidade	Função	Retorna a quantidade disponível, ou None se o código não existe
ler_inteiro	Função	Pede um número inteiro até que seja válido; o mínimo padrão é 0
opcao_cadastrar, opcao_emprestar, opcao_devolver, opcao_consultar, opcao_listar	Funções	Conduzem a conversa com o usuário em cada opção do menu
menu	Função	Mostra o menu, lê a opção e chama a função correspondente
ARQUIVO_CSV e CAMPOS	Constantes	Definem o caminho do estoque.csv e os campos código, nome e quantidade; não são usadas na versão atual
Limitações conhecidas
Os dados ficam só na memória: o estoque é perdido ao encerrar o programa. O código define o arquivo estoque.csv e a lista de campos (código, nome, quantidade) e importa o módulo csv, mas nenhuma função lê ou grava esse arquivo.
O programa não registra quem pegou o equipamento nem a data do empréstimo ou da devolução; controla apenas as quantidades.
Não há opção para editar ou excluir um equipamento cadastrado.
Testes

Cenários que cobrem as regras do código e o resultado esperado de cada um. Os resultados das execuções ainda não foram registrados.

Nº	Cenário	Resultado esperado
1	Cadastrar equipamento com código, nome e quantidade válidos	"Equipamento cadastrado com sucesso!"
2	Cadastrar com código vazio	"O código não pode ser vazio."
3	Cadastrar com nome vazio	"O nome não pode ser vazio."
4	Cadastrar com código já existente	"Já existe um equipamento com esse código."
5	Informar quantidade com letras ou valor decimal	"Entrada inválida. Digite um número inteiro." e nova pergunta
6	Informar quantidade negativa	"Digite um valor maior ou igual a 0." e nova pergunta
7	Emprestar equipamento com unidades disponíveis	"Empréstimo realizado com sucesso!" e quantidade diminui em 1
8	Emprestar equipamento com quantidade 0	"Sem unidades disponíveis para empréstimo."
9	Emprestar com código inexistente	"Equipamento não encontrado."
10	Devolver equipamento que está emprestado	"Devolução registrada com sucesso!" e quantidade aumenta em 1
11	Devolver quando todas as unidades já estão no estoque	Mensagem de que não há empréstimo a devolver
12	Consultar quantidade de código existente e de código inexistente	Quantidade disponível; "Equipamento não encontrado."
13	Listar estoque vazio e com equipamentos	"Nenhum equipamento cadastrado."; tabela com código, nome e quantidade
14	Digitar opção inexistente no menu	"Opção inválida. Tente novamente."
15	Encerrar com a opção 0 ou com Ctrl+C	Mensagem de encerramento, sem erro
Erros encontrados nos testes

Os testes encontraram seis erros, dois de gravidade alta, três média e um baixa. O codigo.py atual já trata os seis.

#	Gravidade	Erro	Como se manifesta	Situação no código atual
1	Alta	O cadastro quebra com texto na quantidade (int(input(...)) sem tratamento)	Digitar abc derruba o programa com ValueError (CT10)	Tratado: ler_inteiro repete a pergunta até receber um número inteiro
2	Alta	A devolução ultrapassa o total cadastrado	Cadastrar 3 e devolver sem ter emprestado deixa 4 unidades, com "sucesso" (CT12, CT13, CT16)	Tratado: a devolução é recusada quando a quantidade disponível já é igual ao total cadastrado
3	Média	O cadastro aceita quantidade negativa	-5 é aceito e o estoque fica negativo (CT11, CT15)	Tratado: quantidade negativa é recusada
4	Média	cadastrar_equipamento aceita código duplicado	Só o menu barrava; uma chamada direta cria dois itens com o mesmo código (CT14)	Tratado: a própria função recusa código já existente
5	Média	Ctrl+C e Ctrl+D não são tratados	O menu fecha com erro na tela, e no pytest o Ctrl+C derrubou a própria execução (CT18)	Tratado: o menu encerra com mensagem em vez de erro
6	Baixa	A mensagem de devolução enganava	"Equipamento não encontrado" aparecia como única falha possível, sem distinguir o caso de nada emprestado (CT13)	Tratado: a mensagem diferencia equipamento não encontrado de nada emprestado
Solução de problemas
Mensagem ou situação	Causa	O que fazer
"Entrada inválida. Digite um número inteiro."	A quantidade tem letras, decimais ou está em branco	Digitar apenas números inteiros, como 5
"Digite um valor maior ou igual a 0."	A quantidade é negativa	Informar 0 ou um valor positivo
"Já existe um equipamento com esse código."	O código já foi cadastrado, e maiúsculas e minúsculas contam como diferentes	Usar outro código ou consultar o estoque na opção 5
"Equipamento não encontrado."	O código digitado não existe	Conferir o código na opção 5 e digitar exatamente igual
"Sem unidades disponíveis para empréstimo."	Todas as unidades já foram emprestadas	Aguardar uma devolução
Mensagem de que não há empréstimo a devolver	Todas as unidades já estão no estoque	Nenhuma ação necessária
Equipamentos sumiram ao reabrir o programa	O estoque não é salvo em arquivo	Cadastrar novamente; ver Limitações conhecidas
Histórico de alterações

O codigo.py atual reúne seis mudanças feitas a partir do relatório de erros.

#	Alteração	Erros corrigidos
1	Quantidade inválida: novo ler_inteiro, que pede o valor de novo quando é texto ou negativo	1 e 3
2	Limite da devolução: Equipamento guarda quantidade_total, e devolver_equipamento retorna False quando já está tudo no estoque	2
3	Validação no cadastro: cadastrar_equipamento retorna True ou False e recusa código ou nome vazio, quantidade negativa e código duplicado	3 e 4
4	Ctrl+C e Ctrl+D: o menu encerra com uma mensagem em vez de erro	5
5	Mensagem de devolução: distingue "Equipamento não encontrado" de "Todas as unidades já estão no estoque"	6
6	Busca interna: nova função _buscar, que evita repetir o laço nas funções	Nenhum (melhoria interna)

A versão do programa e as datas das mudanças ainda não foram informadas.

Equipe

Empresa cliente: TechSolutions.

Função	Responsável
Líder Técnico	Daniel Suhett
Analista de Testes	Daniel Suhett
Desenvolvedor	Daniel Suhett, Matheus Luis
Documentador	Matheus Luis
