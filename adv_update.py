import os
os.chdir('/data/data/com.termux/files/home')
os.system('mv ytconverter bytconverter')
os.system('git clone https://github.com/kaifcodec/ytconverter.git')
os.system('rm -r -f $HOME/bytconverter ')
os.system('pip uninstall pytube')
os.system('pip install pytube')
print("\n RESTART YOUR TERMUX APPLICATION AND 'YT Converter' tool.")
print("\n IF STILL ANY ERROR OCCURS THEN OPEN A ISSUE IN GITHUB")
