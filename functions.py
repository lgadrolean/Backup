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
            log_message(log_path, f"Ignoring the folder: {s}")
            continue
        try:
            if os.path.isdir(s):
                copytree(s, d, log_path)
            else:
                shutil.copy2(s, d)
        except Exception as e:
            log_message(log_path, f"Error copying {s} to {d}: {e}")

def create_backup(source_path, hot_backup_path, daily_backup_path, backupname, log_path, onedrive_path, keep_count_cloud):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    backup_name = f"{backupname}_{timestamp}.zip"
    backup_path = os.path.join(hot_backup_path, backup_name)
    
    log_message(log_path, "###########################################")
    log_message(log_path, "Starting the backup process.")
    
    temp_path = os.path.join(hot_backup_path, "temp_backup")
    copytree(source_path, temp_path, log_path)
    log_message(log_path, f"Folder copied from {source_path} to {temp_path}.")

    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(temp_path):
            dirs[:] = [d for d in dirs if '.git' not in os.path.join(root, d)]
            files = [f for f in files if '.git' not in os.path.join(root, f)]
            for file in files:
                try:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), temp_path))
                except Exception as e:
                    log_message(log_path, f"Error compressing {file}: {e}")
    log_message(log_path, f"Folder compressed into {backup_path}.")
    shutil.rmtree(temp_path)
    log_message(log_path, f"Temporary folder {temp_path} removed.")

    daily_backup_name = f"{backupname}_{datetime.now().strftime('%Y%m%d')}.zip"
    daily_backup_path_full = os.path.join(daily_backup_path, daily_backup_name)
    if not os.path.exists(daily_backup_path_full):
        shutil.copy2(backup_path, daily_backup_path_full)
        log_message(log_path, f"Daily backup moved to {daily_backup_path_full}.")

    onedrive_backup_path_full = os.path.join(onedrive_path, daily_backup_name)
    if not os.path.exists(onedrive_backup_path_full):
        shutil.copy2(backup_path, onedrive_backup_path_full)
        log_message(log_path, f"Daily backup moved to OneDrive: {onedrive_backup_path_full}.")

    maintain_backups(onedrive_path, backupname, log_path, keep_count_cloud, "cloud")

    # Log existing backup statistics
    log_backup_statistics(daily_backup_path, hot_backup_path, onedrive_path, backupname, log_path)

def maintain_backups(backup_path, backupname, log_path, keep_count, tipo="local"):
    log_message(log_path, f"Checking old backups for removal in {backup_path}.")
    backups = sorted([f for f in os.listdir(backup_path) if f.startswith(backupname) and f.endswith(".zip")], key=lambda x: os.path.getmtime(os.path.join(backup_path, x)), reverse=True)
    for backup in backups[keep_count:]:
        os.remove(os.path.join(backup_path, backup))
        log_message(log_path, f"Old {tipo} backup removed: {backup}")

def log_backup_statistics(daily_backup_path, hot_backup_path, onedrive_path, backupname, log_path):
    daily_backups = [f for f in os.listdir(daily_backup_path) if f.startswith(backupname) and f.endswith(".zip")]
    hot_backups = [f for f in os.listdir(hot_backup_path) if f.startswith(backupname) and f.endswith(".zip")]
    cloud_backups = [f for f in os.listdir(onedrive_path) if f.startswith(backupname) and f.endswith(".zip")]

    log_message(log_path, f"Number of daily backups: {len(daily_backups)}")
    log_message(log_path, f"Number of hot backups: {len(hot_backups)}")
    log_message(log_path, f"Number of cloud backups: {len(cloud_backups)}")
