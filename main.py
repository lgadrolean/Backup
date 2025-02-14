import os
import subprocess
import sys

# Instalar pacotes necessários do requirements.txt
def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Verificar se os pacotes estão instalados
try:
    import configparser
    from functions import create_backup, maintain_backups, log_message
except ImportError:
    install_requirements()
    import configparser
    from functions import create_backup, maintain_backups, log_message

# Obter o caminho completo do diretório onde o script está localizado
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ler as configurações do arquivo config.ini
config_path = os.path.join(script_dir, 'config.ini')
config = configparser.ConfigParser()
config.read(config_path)

source_path = config['Paths']['source_path']
destination_path = config['Paths']['destination_path']
project_dir = config['Paths']['project_dir']
daily_backup_path = os.path.join(destination_path, config['Backup']['daily_backup_path'])
hot_backup_path = os.path.join(destination_path, config['Backup']['hot_backup_path'])
backupname = config['Backup']['backupname']
keep_count = int(config['Backup']['keep_count'])
log_path = os.path.join(project_dir, f"{backupname}.log")

# Verificar e criar os diretórios de destino, se necessário
for path in [destination_path, daily_backup_path, hot_backup_path]:
    if not os.path.exists(path):
        os.makedirs(path)

# Criar o backup e manter apenas os 10 mais recentes
try:
    create_backup(source_path, hot_backup_path, daily_backup_path, backupname, log_path)
    maintain_backups(daily_backup_path, backupname, log_path, keep_count)
    maintain_backups(hot_backup_path, backupname, log_path, keep_count)
    log_message(log_path, "Backup concluído com sucesso.")
except Exception as e:
    log_message(log_path, f"Erro durante o processo de backup: {e}")
