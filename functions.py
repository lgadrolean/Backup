import os
import shutil
import zipfile
from datetime import datetime

def log_message(log_path, message):
    with open(log_path, 'a', encoding='utf-8') as log_file:
        log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def copytree(src, dst, log_path):
    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if '.git' in s.split(os.sep):
            log_message(log_path, f"Ignorando a pasta: {s}")
            continue
        try:
            if os.path.isdir(s):
                copytree(s, d, log_path)
            else:
                shutil.copy2(s, d)
        except Exception as e:
            log_message(log_path, f"Erro ao copiar {s} para {d}: {e}")

def create_backup(source_path, hot_backup_path, daily_backup_path, backupname, log_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_name = f"{backupname}_{timestamp}.zip"
    backup_path = os.path.join(hot_backup_path, backup_name)
    
    log_message(log_path, "###########################################")
    log_message(log_path, "Iniciando o processo de backup.")
    
    temp_path = os.path.join(hot_backup_path, "temp_backup")
    copytree(source_path, temp_path, log_path)
    log_message(log_path, f"Pasta copiada de {source_path} para {temp_path}.")

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_path):
            dirs[:] = [d for d in dirs if '.git' not in os.path.join(root, d)]
            files = [f for f in files if '.git' not in os.path.join(root, f)]
            for file in files:
                try:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_path))
                except Exception as e:
                    log_message(log_path, f"Erro ao compactar {file}: {e}")
    log_message(log_path, f"Pasta compactada em {backup_path}.")
    shutil.rmtree(temp_path)
    log_message(log_path, f"Pasta temporária {temp_path} removida.")

    daily_backup_name = f"{backupname}_{datetime.now().strftime('%Y%m%d')}.zip"
    daily_backup_path_full = os.path.join(daily_backup_path, daily_backup_name)
    if not os.path.exists(daily_backup_path_full):
        shutil.copy2(backup_path, daily_backup_path_full)
        log_message(log_path, f"Backup diário movido para {daily_backup_path_full}.")

def maintain_backups(backup_path, backupname, log_path, keep_count):
    log_message(log_path, f"Verificando backups antigos para remoção em {backup_path}.")
    backups = sorted([f for f in os.listdir(backup_path) if f.startswith(backupname) and f.endswith(".zip")], key=lambda x: os.path.getmtime(os.path.join(backup_path, x)), reverse=True)
    for backup in backups[keep_count:]:
        os.remove(os.path.join(backup_path, backup))
        log_message(log_path, f"Backup antigo removido: {backup}")
