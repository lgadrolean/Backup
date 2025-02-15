import os
import subprocess
import sys
import configparser
from functions import create_backup, maintain_backups, log_message

def install_requirements():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

try:
    import configparser
    from functions import create_backup, maintain_backups, log_message
except ImportError:
    install_requirements()
    import configparser
    from functions import create_backup, maintain_backups, log_message

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(script_dir, 'config.ini')
    config = configparser.ConfigParser()
    config.read(config_path)

    source_path = config['Paths']['source_path']
    destination_path = config['Paths']['destination_path']
    project_dir = config['Paths']['project_dir']
    daily_backup_path = os.path.join(destination_path, config['Backup']['daily_backup_path'])
    hot_backup_path = os.path.join(destination_path, config['Backup']['hot_backup_path'])
    backupname = config['Backup']['backupname']
    keep_count_daily = int(config['Backup']['keep_count_daily'])
    keep_count_hot = int(config['Backup']['keep_count_hot'])
    keep_count_cloud = int(config['Backup']['keep_count_cloud'])
    onedrive_path = config['Cloud']['onedrive_path']
    log_path = os.path.join(project_dir, f"{backupname}.log")

    for path in [destination_path, daily_backup_path, hot_backup_path]:
        if not os.path.exists(path):
            os.makedirs(path)

    try:
        create_backup(source_path, hot_backup_path, daily_backup_path, backupname, log_path, onedrive_path, keep_count_cloud)
        maintain_backups(daily_backup_path, backupname, log_path, keep_count_daily)
        maintain_backups(hot_backup_path, backupname, log_path, keep_count_hot)
        log_message(log_path, "Backup concluído com sucesso.")
    except Exception as e:
        log_message(log_path, f"Erro durante o processo de backup: {e}")

if __name__ == "__main__":
    main()
