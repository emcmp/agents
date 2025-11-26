# src/crewmaker/tools/project_tools.py
import os
from pathlib import Path

from crewai_tools import (
    DirectoryReadTool,
    FileReadTool,
    FileWriterTool,
    CodeInterpreterTool,
)

# On limite Crewmaker à un dossier racine, passé en variable d'environnement
# ou via défaut local.
DEFAULT_TARGET_DIR = os.getenv(
    "CREWMAKER_TARGET_DIR",
    "./generated_crews"  # à adapter si tu veux un chemin absolu
)
TARGET_PATH = Path(DEFAULT_TARGET_DIR).resolve()
TARGET_PATH.mkdir(parents=True, exist_ok=True)

# --- Tools de base ---

# Liste récursive des fichiers du dossier cible (et sous-dossiers)
project_dir_reader = DirectoryReadTool(directory=str(TARGET_PATH))

# Lecture de fichiers individuels (on précise dans les prompts de rester dans TARGET_PATH)
project_file_reader = FileReadTool()

# Écriture de fichiers dans un sous-dossier de TARGET_PATH
# FileWriterTool prend (filename, content, directory) côté agent.
project_file_writer = FileWriterTool()

# Execution de code Python (avec Docker si dispo)
code_interpreter = CodeInterpreterTool()
