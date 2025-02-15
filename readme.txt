# Script de Backup Automatizado

Este script realiza backups automáticos de um diretório de origem para um diretório de destino, mantendo backups diários e quentes separados e garantindo que apenas os backups mais recentes sejam mantidos.

## Estrutura do Projeto

- main.py: Arquivo principal que executa a lógica do backup.
- functions.py: Contém funções auxiliares para a criação de backups, manutenção dos backups e logging.
- config.ini: Arquivo de configuração contendo os caminhos dos diretórios e nomes de backup.
- requirements.txt: Lista de dependências necessárias para o script.

## Configuração

Antes de executar o script, certifique-se de ter os seguintes arquivos na estrutura correta:

### config.ini

Especifique os caminhos dos diretórios e configurações de backup.

[Paths]
source_path = C:/users/lgadr/Projetos
destination_path = C:/users/lgadr/Backups
project_dir = C:/users/lgadr/Projetos/Backup

[Backup]
backupname = Backup_Projetos
daily_backup_path = backup_diario
hot_backup_path = backup_quente
keep_count_daily = 7
keep_count_hot = 10
keep_count_cloud = 5

[Cloud]
onedrive_path = C:/users/lgadr/OneDrive/Backups

### requirements.txt

Lista de dependências necessárias para o script.

## Uso

1. Certifique-se de que todos os arquivos (main.py, functions.py, config.ini, requirements.txt) estejam no diretório do projeto (project_dir).

2. Execute o main.py. O script irá instalar automaticamente as dependências necessárias e criar os backups conforme a configuração no config.ini.

### Comandos

Para executar o script, use:

python main.py

### Log

O script irá gerar um log detalhado no caminho especificado (log_path), incluindo informações sobre o processo de backup, backups movidos para o OneDrive e estatísticas de backups existentes.

## Estatísticas dos Backups

No final do processo de backup, o script registra as estatísticas dos backups existentes:
- Número de backups diários
- Número de backups quentes
- Número de backups na nuvem
