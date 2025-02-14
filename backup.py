import os
import shutil
import zipfile
from datetime import datetime

# Caminhos de origem e destino
source_path = "C:/users/lgadr/Projetos"
destination_path = "C:/users/lgadr/Backups"
backupname = "Backup_Projeto"  # Defina aqui o nome do backup

# Nome do backup com data e hora
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
backup_name = f"{backupname}_{timestamp}.zip"
backup_path = os.path.join(destination_path, backup_name)
log_path = os.path.join(destination_path, f"{backupname}.log")  # Log único

# Verificar e criar o diretório de destino, se necessário
if not os.path.exists(destination_path):
    os.makedirs(destination_path)

# Função para criar o log
def log_message(message):
    with open(log_path, 'a') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

# Função para criar o backup
def create_backup():
    log_message("###########################################")
    log_message("Iniciando o processo de backup.")
    
    # Caminho temporário para copiar a pasta
    temp_path = os.path.join(destination_path, "temp_backup")
    
    def copytree(src, dst, symlinks=False, ignore=None):
        os.makedirs(dst, exist_ok=True)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if '.git' in s.split(os.sep):
                log_message(f"Ignorando a pasta: {s}")
                continue  # Ignorar pastas .git e seu conteúdo
            try:
                if os.path.isdir(s):
                    copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)
            except Exception as e:
                log_message(f"Erro ao copiar {s} para {d}: {e}")

    copytree(source_path, temp_path)
    log_message(f"Pasta copiada de {source_path} para {temp_path}.")

    # Compactar a pasta copiada
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_path):
            # Ignorar diretórios e arquivos .git
            dirs[:] = [d for d in dirs if '.git' not in os.path.join(root, d)]
            files = [f for f in files if '.git' not in os.path.join(root, f)]
            for file in files:
                try:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_path))
                except Exception as e:
                    log_message(f"Erro ao compactar {file}: {e}")
    log_message(f"Pasta compactada em {backup_path}.")

    # Remover a pasta temporária
    shutil.rmtree(temp_path)
    log_message(f"Pasta temporária {temp_path} removida.")

# Função para manter apenas os 10 backups mais recentes
def maintain_backups():
    log_message("Verificando backups antigos para remoção.")
    backups = sorted([f for f in os.listdir(destination_path) if f.startswith(backupname) and f.endswith(".zip")], key=lambda x: os.path.getmtime(os.path.join(destination_path, x)), reverse=True)
    for backup in backups[10:]:
        os.remove(os.path.join(destination_path, backup))
        log_message(f"Backup antigo removido: {backup}")

# Criar o backup e manter apenas os 10 mais recentes
try:
    create_backup()
    maintain_backups()
    log_message("Backup concluído com sucesso.")
except Exception as e:
    log_message(f"Erro durante o processo de backup: {e}")
