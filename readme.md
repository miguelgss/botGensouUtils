# Bot de lista para o QBGS - Quinta Batalhas Gensou Semanais

## Sobre
Esse é um projeto simples que apoiará a manutenção de um lobby de jogadores orientado por uma lista. **Os dados só permanecem durante o tempo de execução.**
O bot originou como um apoio pro evento semanal de Touhou Hisoutensoku no Gensou Arena, hostado em nosso [servidor do discord](https://discord.gg/pXyRx3ed) e transmitido no [canal da twitch](https://www.twitch.tv/gensouarena).

## Ferramentas Necessárias
Para rodar o projeto usando o código fonte, é necessário:
- Instalar o Python3 e o pip;
- Instalar com o pip as dependências descritas no arquivo "requirements.txt";
- Inicializar o main.py.

Caso só queira executar, siga as configurações abaixo e obtenha o executável [aqui](https://github.com/miguelgss/botGensouUtils/releases). (.exe para Windows, o outro é para Linux)


## Configurações
Também é necessário criar um arquivo com nome "config.txt" na pasta, incluindo nele a linha:
- token = SeuToken

O "SeuToken" é o token gerado pelo seu bot de discord.

A seguinte linha é mandatória a partir da versão 2.0.0. Caso não seja informado, os comandos com permissionamento não poderão ser utilizados:
- roles = role1,role2,role3

Os espaços devem ser respeitados em ambas as linhas.

#### OBS: Também é possível registrar o token no próprio código dentro do bot.py, mas não é recomendado.
