# ytconverter

`ytconverter` is a Python-based project developed by [kaifcodec](https://github.com/kaifcodec) designed to provide a robust tool for converting YouTube videos into various formats. This tool simplifies the process of downloading and converting videos, making it accessible for users who need to handle YouTube content efficiently.
![Screenshot_20250421-091445~3](https://github.com/user-attachments/assets/5e27f2e3-a40d-49dc-87e4-d69ce28d575e)


![Screenshot_20250420-110350](https://github.com/user-attachments/assets/8e9d00ce-b698-4b1f-8870-badd5d274442)


## Contact for any error or issue:
  
- kaif.repo.official@gmail.com

## Features

- **Video Downloading**: Fetch videos directly from YouTube.
- **Format Conversion**: Convert downloaded videos into different formats such as MP3, MP4, etc.
- **Metadata Handling**: Extract and manage metadata associated with YouTube videos.

## Requirements

- Python 3.x
- Required Python libraries (listed in `requirements.txt`)

## Installation Termux


1. Install python and update termux:
   ```bash
    pkg update -y && pkg upgrade -y && pkg install python
    ```
2. Install git:
   ```bash
    pkg install git
    ```
3. Install curl :
   ```bash
    pkg install curl
    ```

4. Clone the repository:
    ```bash
    git clone https://github.com/kaifcodec/ytconverter.git
    ```

5. Give storage permission:
    ```bash
    termux-setup-storage
    ```

    
6. Navigate to the project directory:
    ```bash
    cd ytconverter
    ```

## Usage

1. Run the main script to start the conversion process:
    ```bash
    python ytconverter.py
    ```
2. Follow the on-screen instructions to input the YouTube URL and choose the desired output format.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please open an issue or contact [kaifcodec](https://github.com/kaifcodec).
