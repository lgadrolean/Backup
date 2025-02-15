Automated Backup Script

This script automatically backs up a source directory to a destination directory, maintaining separate daily and hot backups and ensuring that only the most recent backups are kept.

Project Structure

- main.py: Main file that executes the backup logic.
- functions.py: Contains helper functions for creating backups, maintaining backups, and logging.
- config.ini: Configuration file containing directory paths and backup names.
- requirements.txt: List of dependencies required for the script.

Configuration

Before running the script, ensure you have the following files in the correct structure:

config.ini

Specify the directory paths and backup settings.

[Paths]
source_path = C:/users/lgadr/Projects
destination_path = C:/users/lgadr/Backups
project_dir = C:/users/lgadr/Projects/Backup

[Backup]
backupname = Backup_Projects
daily_backup_path = daily_backup
hot_backup_path = hot_backup
keep_count_daily = 7
keep_count_hot = 10
keep_count_cloud = 5

[Cloud]
onedrive_path = C:/users/lgadr/OneDrive/Backups

requirements.txt

List of dependencies required for the script.

Usage

1. Ensure that all files (main.py, functions.py, config.ini, requirements.txt) are in the project directory (project_dir).

2. Run main.py. The script will automatically install the required dependencies and create the backups as per the configuration in config.ini.

Commands

To run the script, use:

python main.py

Log

The script will generate a detailed log at the specified path (log_path), including information about the backup process, backups moved to OneDrive, and statistics of existing backups.

Backup Statistics

At the end of the backup process, the script logs statistics of the existing backups:
- Number of daily backups
- Number of hot backups
- Number of cloud backups

Contribution

I hope you use and enjoy this automated backup script. If you encounter any issues or have suggestions for improvements, feel free to open an issue or leave your feedback. Your contribution is very welcome and appreciated!
