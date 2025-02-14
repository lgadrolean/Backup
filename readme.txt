# Script de Backup Automatizado

Este script realiza backups automáticos de um diretório de origem para um diretório de destino, mantendo backups diários e quentes separados e garantindo que apenas os 10 backups mais recentes sejam mantidos.

## Estrutura do Projeto

- `main.py`: Arquivo principal que executa a lógica do backup.
- `functions.py`: Contém funções auxiliares para a criação de backups, manutenção dos backups e logging.
- `config.ini`: Arquivo de configuração contendo os caminhos dos diretórios e nomes de backup.
- `requirements.txt`: Lista de dependências necessárias para o script.

## Configuração

Antes de executar o script, certifique-se de ter os seguintes arquivos na estrutura correta:

### `config.ini`

Especifique os caminhos dos diretórios e configurações de backup.

### `requirements.txt`

Lista de dependências necessárias para o script.

## Uso

1. Certifique-se de que todos os arquivos (`main.py`, `functions.py`, `config.ini`, `requirements.txt`) estejam no diretório do projeto (`project_dir`).

2. Execute o `main.py`. O script irá instalar automaticamente as dependências necessárias e criar os backups conforme a configuração no `config.ini`.

### Comandos

Para executar o script, use:

```sh
python main.py
