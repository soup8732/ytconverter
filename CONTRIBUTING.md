# Contributing to YTConverter™

First off, thank you for considering contributing to **YTConverter™**! Your support is invaluable in making this tool even more robust and user-friendly.

## 🛠️ Getting Started

1.  **Fork the Repository** Click the "Fork" button at the top right of the [repository page](https://github.com/kaifcodec/ytconverter).

2.  **Clone Your Fork**
    ```bash
    git clone https://github.com/your-username/ytconverter.git
    cd ytconverter
    ```

3.  **Set Up the Environment**

    **For Termux:**

    ```bash
    pkg update -y && pkg upgrade -y
    pkg install python git curl
    termux-setup-storage
    pip install -r requirements.txt
    ```

    **For Linux (Ubuntu/Debian/Fedora/Arch):**

    ```bash
    sudo apt update && sudo apt install python3 python3-pip git curl -y
    pip3 install -r requirements.txt
    ```

4.  **Run the Application**

    ```bash
    python ytconverter.py
    ```

## 🧪 Running Tests

Before submitting your changes, ensure that:

* The application runs without errors.
* New features or fixes are covered by tests, if applicable.
* Existing tests pass successfully.

## 📄 Code Style Guidelines

* Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code styling.
* Use descriptive variable and function names.
* Include docstrings for all public functions and classes.
* Maintain consistent indentation and formatting.

## 🔀 Branching Strategy

* `main`: Stable release branch.
* `dev`: Development branch for ongoing work.
* `feature/<your-feature-name>`: Prefix for new feature branches (e.g., `feature/add-download-option`).
* `bugfix/<your-bug-fix>`: Prefix for bug fix branches (e.g., `bugfix/fix-crash-on-startup`).

## ✅ Commit Messages


Use clear and concise commit messages. Follow this format:


**Types:**

* `feat`: New feature
* `fix`: Bug fix
* `docs`: Documentation changes
* `style`: Code style changes (formatting, missing semi colons, etc.)
* `refactor`: Code refactoring
* `test`: Adding or updating tests
* `chore`: Maintenance tasks


**Example:**


feat: add support for batch video downloads
Implemented functionality to allow users to download multiple videos by providing a list of URLs.

## 📬 Submitting a Pull Request

1.  **Ensure your fork is up to date:**

    ```bash
    git checkout main
    git pull upstream main
    ```

2.  **Create a new branch for your feature or fix:**

    ```bash
    git checkout -b feature/your-feature-name
    ```

3.  **Make your changes and commit them:**

    ```bash
    git add .
    git commit -m "feat: add your feature"
    ```

4.  **Push your branch to your fork:**

    ```bash
    git push origin feature/your-feature-name
    ```

5.  **Open a Pull Request on GitHub:**

    * Go to your forked repository.
    * Click on "Compare & pull request".
    * Provide a clear description of your changes.

## 📞 Contact

For any questions or discussions:

* **Email:** kaifcodec@gmail.com
* **Issues:** Submit an issue on [GitHub](https://github.com/kaifcodec/ytconverter/issues)

