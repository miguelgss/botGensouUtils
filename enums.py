from enum import Enum

class Color(Enum):
    Erro = 0xEE2B3B
    Alerta = 0xFFC94D
    Sucesso = 0x81E052

class ErrorMessages(Enum):
    SemPermissao = "Você não possui permissão para usar esse comando."
    ComandoNaoEncontrado = "Comando não encontrado. Use {h para verificar os comandos disponíveis."
    UsuarioNaoEncontrado = "Usuário não encontrado. Para adicionar ou remover, é necessário _pingar_ o usuário que deseja adicionar ou remover da lista ou, caso queira entrar ou sair, utilizar o comando addme ou rme."
    SemListaApagavel = "Não é possível apagar uma lista quando há apenas uma!"

    def SemJogadoresSuficientes(indexLista: int):
        return f"Não é possível iniciar a Lista {indexLista} com menos de dois de jogadores"
    
    def ListaJaIniciada(indexLista: int):
        return f"A Lista {indexLista} já foi iniciada!"

class StatusLista(Enum):
    Bloqueada = '🔒 Lista(s) bloqueada(s)!'
    Desbloqueada = '🔓 Lista(s) desbloqueada(s)!'

class CommandNames(list, Enum):
    Ajuda = ['help', 'h', 'ajuda']
    Lista = ['lista','l']
    AdicionaLista = ['adicionalista', 'al']
    Adiciona = ['adiciona', 'add', 'a']
    Adicioname = ['adicioname','addme','am']
    RemoveLista = ['removelista', 'rl']
    Remove = ['remove','r']
    Removeme = ['removeme', 'rme','rm']
    Embaralha = ['embaralha', 'e']
    Reembaralha = ['reembaralha','re']
    EmbaralhaTodos = ['embaralhatodos', 'et']
    Separar = ['separar', 's']
    Move = ['move','m','mv']
    Trocar = ['troca', 't', 'tr']
    Bloquear = ['bloquear', 'b']
    Limpar = ['limpar', 'clear', 'c']

    BonsJogos = ['gg', 'ggs']
    IniciarLista = ['iniciarlista', 'iniciar', 'i']
    PararLista = ['pararLista', 'parar', 'p']

    ajudaBasicoList = [
        "**- De uso livre:**",
        f"**{Ajuda}** - Mostra os comandos do bot;",
        f"**{Lista}** - Mostra a lista atual;",
        f"**{Adicioname}** - Adiciona quem mandou a mensagem para a lista;",
        f"**{Removeme}** - Remove quem mandou a mensagem da lista;",
        f"**{BonsJogos}** - Avança para a próxima partida caso seja um dos jogadores jogando atualmente;"
    ]
    ajudaList = [
        "---------------------------------------------------------",
        "**- Exige cargos com permissão:**",
        f"**{AdicionaLista}** - Cria uma nova lista. Opcionalmente, pessoas podem ser acrescentadas diretamente a essa nova lista.",
        f"**{RemoveLista}** - Remove uma lista e move os nomes contidos nela para outra lista;",
        f"**{Adiciona}** - Recebe um ou mais argumentos para adicionar alguém a lista com menor número de nomes;",
        f"**{Remove}** - Recebe um ou mais argumentos para remover alguém da lista;",
        f"**{Embaralha}** - Move o último para a primeira posição e então embaralha cada lista; _(Desbloqueia a lista e adiciona a lista os nomes em espera)_",
        f"**{Reembaralha}** - Reembaralha todos de cada lista exceto o primeiro; _(Desbloqueia a lista e adiciona a lista os nomes em espera)_",
        f"**{EmbaralhaTodos}** - Embaralha todas as listas de forma totalmente aleatória; _(Desbloqueia a lista e adiciona a lista os nomes em espera)_",
        f"**{Separar} (Opcional - __NumeroLista__)** - Divide a lista, pegando metade de seus membros para criar uma nova. Caso não seja especificado, o comando será executado para a primeira lista;",
        f"**{Move} (Opcional - __NumeroLista__) __X__ (Opcional - __NumeroLista__) __Y__** - Move um nome (posição X) para a posição especificada (Y)",
        "Exemplo: m 1 1 2 1 moverá o lista1-primeiroNome pra posição do lista2-primeiroNome, movendo os outros para baixo;",
        f"**{Trocar} (Opcional - __NumeroLista__) __X__ (Opcional - __NumeroLista__) __Y__** - Troca um nome (posição X) com a posição especificada (Y)",
        "Exemplo: t 1 1 2 1 trocará as posições entre lista1-primeiroNome e lista2-primeiroNome;",
        f"**{Bloquear}** - Bloqueia/desbloqueia as listas. Quando bloqueado, cria a lista de espera. Quando desbloqueado, adiciona a lista os nomes em espera;",
        f"**{Limpar}** (Opcional - __N__) - Limpa as mensagens mais recentes do bot. O 'N' especifica o número de mensagens para apagar, caso necessário;",
        f"**{IniciarLista}** - Começa a(s) lista(s), atualizando os primeiros de cada lista para o estado de 'LUTANDO!';",
        f"**{PararLista}** - Para a(s) lista(s), removendo o estado de 'LUTANDO!' de qualquer jogador que o tenha."
    ]

    def __list__(self) -> list:
        return list.__list__(self)