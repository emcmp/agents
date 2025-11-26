# src/crewmaker/main.py

import logging
from pathlib import Path

from crewmaker.crew import CrewBuilder

# --- Logging : console + fichier ---
LOG_PATH = Path(__file__).resolve().parents[2] / "crewmaker_run.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_PATH, encoding="utf-8"),
    ],
)

logger = logging.getLogger("crewmaker")


def run():
    """
    Lance Crewmaker pour générer un nouveau crew.
    """
    # Tu peux modifier la spec ici :
    spec = (
        "Je veux un crew qui crée d'autres crews pour des tâches de "
        "programmation, avec support OpenAI et/ou Google Gemini, et un "
        "Dockerfile pour l’exécuter en conteneur."
    )

    # Dossier cible par défaut : le projet generated_crews que tu as déjà créé.
    default_target = (
        Path(__file__).resolve().parents[3]
        / "generated_crews"
        / "src"
        / "generated_crews"
    )

    target_dir = default_target

    logger.info("=== Lancement Crewmaker ===")
    logger.info("Spec: %s", spec)
    logger.info("Target dir: %s", target_dir)

    inputs = {
        "spec": spec,
        "target_dir": str(target_dir),
    }

    builder = CrewBuilder()      # instancie
    crew = builder.crew()        # récupère l’objet Crew
    result = crew.kickoff(inputs=inputs)


    # Affiche le résultat brut (souvent un résumé / dernier output)
    print("\n=== Résultat Crewmaker ===")
    print(result)


if __name__ == "__main__":
    run()
