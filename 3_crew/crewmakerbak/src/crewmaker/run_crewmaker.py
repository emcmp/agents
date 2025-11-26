
# run_crewmaker.py
import logging
from pathlib import Path
from crewmaker.crew import CrewBuilder

LOG_DIR = Path("./logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / "crewmaker_run.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ],
)

logger = logging.getLogger("crewmaker")


def run():
    spec = "Je veux un crew qui crée d'autres crews pour des tâches de programmation"

    logger.info("=== Lancement Crewmaker ===")
    logger.info("Spec: %s", spec)

    crew = CrewBuilder().crew()
    result = crew.kickoff(
        inputs={
            "spec": spec,
            "target_dir": r"P:\Projects\AI\EMagents\3_crew\generated_crews"
        }
    )

    # On logge le raw (long) dans le fichier uniquement
    logger.info("Result.raw:\n%s", result.raw)

    print("Execution terminée. Log :", LOG_FILE)
    return result


if __name__ == "__main__":
    run()
