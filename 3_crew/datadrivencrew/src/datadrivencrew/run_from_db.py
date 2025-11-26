from __future__ import annotations

import argparse
import base64
import json
import sqlite3
from datetime import datetime
from pathlib import Path

from .db_loader import load_crew


# === Paths ===
BASE_DIR = Path(__file__).resolve().parents[2]  # .../datadrivencrew
DB_PATH = BASE_DIR / "data" / "crews.db"
OUTPUT_DIR = BASE_DIR / "outputs"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _extract_text(result) -> str:
    """
    Essaie d'extraire le texte du résultat CrewAI, peu importe la version.
    """
    if hasattr(result, "raw"):
        return result.raw
    return str(result)

import json
import base64

def parse_inputs(s: str | None) -> dict:
    """
    Tente d'abord de parser s comme du JSON brut.
    Si ça échoue, tente de considérer s comme une chaîne base64
    contenant du JSON UTF-8 encodé.
    """
    if not s:
        return {}

    s = s.strip()

    # 1) Essayer JSON brut
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass  # on tente base64 après

    # 2) Essayer base64 -> JSON
    try:
        decoded = base64.b64decode(s).decode("utf-8")
        return json.loads(decoded)
    except Exception as ex:
        raise ValueError(
            f"input_json invalide : ni JSON brut, ni base64 de JSON ({ex})"
        )


def run_execution(crew_code: str, input_json: str) -> int:
    """
    Exécute un crew à partir du code, enregistre l'exécution dans la table `execution`
    et écrit un fichier .md avec le résultat final.

    Retourne: execution_id (int)
    """
    OUTPUT_DIR.mkdir(exist_ok=True)

    conn = _connect()
    try:
        # 1) Récupérer le crew_id
        row = conn.execute(
            "SELECT id FROM crew WHERE code = ?", (crew_code,)
        ).fetchone()
        if row is None:
            raise RuntimeError(f"Crew '{crew_code}' non trouvé dans la table crew.")

        crew_id = row["id"]

        # 2) Créer une entrée dans execution (status = running)
        started_at = datetime.now().isoformat()
        cur = conn.execute(
            """
            INSERT INTO execution (crew_id, started_at, status, input_json)
            VALUES (?, ?, ?, ?)
            """,
            (crew_id, started_at, "running", input_json),
        )
        execution_id = cur.lastrowid
        conn.commit()

        print(f"[run_from_db] Started execution #{execution_id} for crew '{crew_code}'")

        # 3) Charger le crew depuis la DB
        crew = load_crew(crew_code)

        # 4) Exécuter le crew
        import base64
        import json

        inputs = parse_inputs(input_json)


        # 4) Préparer les inputs
        if input_json:
            # On essaie d'abord de traiter comme du JSON brut
            try:
                inputs = json.loads(input_json)
            except json.JSONDecodeError:
                # Si ça échoue, on essaie base64 -> JSON
                try:
                    decoded = base64.b64decode(input_json).decode("utf-8")
                    inputs = json.loads(decoded)
                except Exception as ex:
                    raise RuntimeError(
                        f"Impossible d'interpréter input_json ni comme JSON ni comme base64 JSON: {ex!r}"
                    )
        else:
            inputs = {}
        
        # 5) Exécuter le crew
        result = crew.kickoff(inputs=inputs)


        output_text = _extract_text(result)

        # 5) Écrire un fichier .md avec le résultat global
        md_path = OUTPUT_DIR / f"execution_{execution_id}.md"
        md_path.write_text(output_text, encoding="utf-8")

        # 6) Mettre à jour l'exécution en succès
        finished_at = datetime.now().isoformat()
        conn.execute(
            """
            UPDATE execution
               SET finished_at = ?,
                   status = ?,
                   output_summary = ?,
                   output_file_path = ?
             WHERE id = ?
            """,
            (finished_at, "success", output_text, str(md_path), execution_id),
        )
        conn.commit()

        print(f"[run_from_db] Execution #{execution_id} success. Output -> {md_path}")
        return execution_id

    except Exception as ex:
        # 7) En cas d'erreur, mettre à jour la ligne execution
        finished_at = datetime.now().isoformat()
        conn.execute(
            """
            UPDATE execution
               SET finished_at = ?,
                   status = 'error',
                   error_message = ?
             WHERE id = ?
            """,
            (finished_at, repr(ex), execution_id),
        )
        conn.commit()
        print(f"[run_from_db] Execution #{execution_id} ERROR: {ex!r}")
        raise

    finally:
        conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a CrewAI crew from SQLite config.")
    parser.add_argument("--crew-code", required=True, help="Code du crew (colonne crew.code)")
    parser.add_argument(
        "--input-json",
        required=True,
        help='JSON des inputs pour crew.kickoff, ex: {"user_input": "Bonjour"}',
    )
    args = parser.parse_args()

    run_execution(args.crew_code, args.input_json)


if __name__ == "__main__":
    main()
