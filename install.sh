#!/bin/bash

# Simple ANSI color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Check if terminal supports color
supports_color() {
    if [ -t 1 ] && [ -n "$TERM" ] && [ "$TERM" != "dumb" ]; then
        return 0
    else
        GREEN=''; RED=''; YELLOW=''; CYAN=''; RESET=''
    fi
}

detect_os() {
    if [ -f /data/data/com.termux/files/usr/bin/pkg ]; then
        echo "termux"
    elif [ -f /etc/os-release ]; then
        . /etc/os-release
        case "$ID" in
            ubuntu|debian) echo "debian" ;;
            kali) echo "kali" ;;
            arch|manjaro) echo "arch" ;;
            *) echo "unknown" ;;
        esac
    else
        echo "unknown"
    fi
}

install_system_packages() {
    case "$1" in
        termux)
            echo -e "${CYAN}Detected: Termux${RESET}"
            pkg update -y
            pkg install -y python ffmpeg yt-dlp
            ;;
        debian|kali)
            echo -e "${CYAN}Detected: $1 (Debian-based)${RESET}"
            sudo apt update
            sudo apt install -y python3 python3-pip ffmpeg yt-dlp
            ;;
        arch)
            echo -e "${CYAN}Detected: Arch-based system${RESET}"
            sudo pacman -Sy --noconfirm python python-pip ffmpeg yt-dlp
            ;;
        *)
            echo -e "${YELLOW}Unknown or unsupported OS. Trying universal install...${RESET}"
            # Attempt basic package installs
            command -v python3 >/dev/null || {
                echo -e "${YELLOW}Trying to install Python...${RESET}"
                curl -s https://www.python.org/ftp/python/3.10.0/Python-3.10.0.tgz | tar xz || echo -e "${RED}Python install failed.${RESET}"
            }

            command -v pip3 >/dev/null || {
                echo -e "${YELLOW}Trying to install pip...${RESET}"
                curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py || echo -e "${RED}pip install failed.${RESET}"
            }

            command -v ffmpeg >/dev/null || echo -e "${YELLOW}ffmpeg not found. Please install it manually.${RESET}"
            command -v yt-dlp >/dev/null || echo -e "${YELLOW}yt-dlp not found. You can try: pip install yt-dlp${RESET}"

            echo -e "\n${YELLOW}If any step above failed, please install these manually:${RESET}"
            echo -e "${CYAN}Python 3, pip, ffmpeg, yt-dlp${RESET}"
            ;;
    esac
}

install_python_packages() {
    echo -e "\n${CYAN}Installing Python packages with pip...${RESET}"
    pip install --upgrade pip
    pip install fontstyle yt_dlp colored requests
}

main() {
    supports_color
    echo -e "${GREEN}Starting YTConverter™ installer...${RESET}"
    os_type=$(detect_os)
    install_system_packages "$os_type"
    install_python_packages
    echo -e "\n${GREEN}All dependencies installed. You can now run YTConverter™!${RESET}"
}

main
