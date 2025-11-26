# src/crewmaker/tools/project_tools.py

from pathlib import Path
import os
from typing import Any, Optional, Type

from crewai_tools import DirectoryReadTool, FileReadTool
from crewai.tools import BaseTool
from pydantic import BaseModel

# Dossier de config interne de Crewmaker (pour que les agents puissent
# relire leurs propres YAML si nécessaire, sans scanner toute la venv).
CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"

# Outil pour lister les fichiers de config de Crewmaker
project_dir_reader = DirectoryReadTool(
    directory=str(CONFIG_DIR)
)

# Outil générique de lecture de fichier (le LLM doit fournir file_path)
project_file_reader = FileReadTool()


# ---------- Nouveau : FileWriter UTF-8 maison ----------

def _strtobool(val: str) -> bool:
    """Conversion simple string -> bool (compatible avec l'ancien FileWriterTool)."""
    val = str(val).strip().lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Invalid truth value for overwrite: {val!r}")


class Utf8FileWriterToolInput(BaseModel):
    filename: str
    directory: Optional[str] = "./"
    overwrite: str = "True"  # string pour rester compatible avec ce que le LLM pourrait envoyer
    content: str


class Utf8FileWriterTool(BaseTool):
    """
    Tool d'écriture de fichier qui FORCE l'encodage UTF-8.
    Compatible avec les schémas d'appel du FileWriterTool de crewai_tools.
    """
    name: str = "UTF-8 File Writer Tool"
    description: str = (
        "Écrit du contenu texte dans un fichier (encodage UTF-8), "
        "à partir de 'filename', 'content', et éventuellement 'directory' et 'overwrite'."
    )
    args_schema: Type[BaseModel] = Utf8FileWriterToolInput

    def _run(
        self,
        filename: str,
        directory: str = "./",
        overwrite: str = "True",
        content: str = "",
        **kwargs: Any
    ) -> str:
        try:
            # Création du dossier si nécessaire
            directory = directory or "./"
            os.makedirs(directory, exist_ok=True)

            filepath = os.path.join(directory, filename)

            # Gestion du overwrite (string -> bool)
            try:
                overwrite_flag = _strtobool(overwrite)
            except Exception:
                # Si le LLM envoie déjà un bool, on s'adapte
                overwrite_flag = bool(overwrite)

            if os.path.exists(filepath) and not overwrite_flag:
                return f"File {filepath} already exists and overwrite=False."

            mode = "w"  # on écrase par défaut quand overwrite=True
            if not overwrite_flag and not os.path.exists(filepath):
                mode = "x"

            # ⚠️ ICI : encodage imposé UTF-8
            with open(filepath, mode, encoding="utf-8", newline="\n") as f:
                content = normalize_crewai_code(content)
                f.write(content)


            return f"Content successfully written to {filepath}"

        except FileExistsError:
            return f"File {filepath} already exists and overwrite=False."
        except Exception as e:
            return f"An error occurred while writing to the file: {e}"

def normalize_crewai_code(content: str) -> str:
    # Remplace verbose=2 → verbose=True
    content = content.replace("verbose=2", "verbose=True")
    content = content.replace("verbose: 2", "verbose: true")
    return content

# Outil générique d’écriture de fichier pour les agents (Crews générés)
project_file_writer = Utf8FileWriterTool()
