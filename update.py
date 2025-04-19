import os
import shutil

# Change to the home directory of Termux
os.chdir('/data/data/com.termux/files/home')

# Rename the existing ytconverter directory to a backup name
if os.path.exists('ytconverter'):
    os.rename('ytconverter', 'bytconverter')

# Clone the latest version of the ytconverter repository
try:
    os.system('git clone https://github.com/kaifcodec/ytconverter.git')
except Exception as e:
    print(f"Error cloning repository: {e}")
    exit()

# Remove the backup directory
if os.path.exists('bytconverter'):
    shutil.rmtree('bytconverter', ignore_errors=True)

# Ensure yt_dlp is installed and updated
try:
    os.system('pip uninstall -y yt_dlp')
    os.system('pip install yt_dlp --upgrade')
except Exception as e:
    print(f"Error updating yt_dlp: {e}")
    exit()

print("\nRESTART YOUR TERMUX APPLICATION AND 'YT Converter' tool.")
print("\nIF STILL ANY ERROR OCCURS, OPEN AN ISSUE ON GITHUB. OR EMAIL:kaif.repo.official@gmail.com")

