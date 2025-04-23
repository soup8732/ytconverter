import os
import shutil
import subprocess

# Define paths
home_dir = '/data/data/com.termux/files/home'
project_dir = os.path.join(home_dir, 'ytconverter')
backup_dir = os.path.join(home_dir, 'bytconverter')

os.chdir(home_dir)

# Backup existing folder
if os.path.exists(project_dir):
    os.rename(project_dir, backup_dir)

# Clone the latest version
try:
    subprocess.run(['git', 'clone', 'https://github.com/kaifcodec/ytconverter.git'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error cloning repository: {e}")
    # Rollback to backup
    if os.path.exists(backup_dir):
        os.rename(backup_dir, project_dir)
        print("Restored previous version from backup.")
    exit()

# Remove backup after successful clone
if os.path.exists(backup_dir):
    shutil.rmtree(backup_dir, ignore_errors=True)

# Update yt_dlp
try:
    subprocess.run(['pip', 'uninstall', '-y', 'yt_dlp'], check=True)
    subprocess.run(['pip', 'install', 'yt_dlp', '--upgrade'], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error updating yt_dlp: {e}")
    exit()

print("\nUpdate complete. RESTART TERMUX and run 'ytconverter' again.")
print("If you face issues, report on GitHub or email: kaif.repo.official@gmail.com")
