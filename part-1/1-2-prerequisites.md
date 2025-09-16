# Prerequisites

Before you begin this workshop, please ensure you have the following:

## Software
- **Python 3.8 or higher**
- **Visual Studio Code** (or another code editor of your choice)
- **Git** (for cloning the repository)

## Python Packages
All required Python packages are listed in the `requirements.txt` files in the `part-1/code/` and `part-2/code/` folders. You can install them using:

```
pip install -r part-1/code/requirements.txt
pip install -r part-2/code/requirements.txt
```

## Setting Up a Virtual Environment in VS Code

It is recommended to use a virtual environment to manage your Python dependencies for this workshop. Here’s how you can set one up using the VS Code Command Palette:

1. **Open the Command Palette**
   - Press <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> (Windows/Linux) or <kbd>Cmd</kbd>+<kbd>Shift</kbd>+<kbd>P</kbd> (macOS).

2. **Create a Virtual Environment**
   - Type `Python: Create Environment` and select it.
   - Choose `Venv` as the environment type and follow the prompts to create the environment in your project folder (recommended: `.venv`).

3. **Select the Interpreter**
   - After creation, VS Code should automatically select the new environment. If not, open the Command Palette again, type `Python: Select Interpreter`, and choose the interpreter from the `.venv` folder.

4. **Activate the Environment (if needed)**
   - If you open a new terminal, VS Code should activate the environment automatically. If not, you can activate it manually:
     - On **Windows** (PowerShell):
       ```powershell
       .venv\Scripts\Activate.ps1
       ```
     - On **macOS/Linux**:
       ```bash
       source .venv/bin/activate
       ```

5. **Install Requirements**
   - With the virtual environment activated, install dependencies:
     ```powershell
     pip install -r part-1/code/requirements.txt
     pip install -r part-2/code/requirements.txt
     ```

This ensures your dependencies are isolated and your environment is reproducible.

## Skills
- Basic understanding of Python (variables, functions, loops)
- Familiarity with running scripts from the command line

## Accounts
- **(Optional)** A GitHub account if you want to fork or contribute to the repository

---
Once you have these prerequisites in place, you're ready to start the workshop!
