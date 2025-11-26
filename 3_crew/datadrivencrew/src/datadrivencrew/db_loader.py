# src/datadrivencrew/db_loader.py

import sqlite3
from pathlib import Path
from typing import Dict, List

from crewai import Crew, Agent, Task

# DB = <racine du projet>/data/crews.db
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "crews.db"


def _connect() -> sqlite3.Connection:
    """Ouvre une connexion SQLite avec row_factory sur Row."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _build_llm_for_model(conn: sqlite3.Connection, llm_model_id: int | None):
    """
    V1 : on ne passe pas de LLM explicite à l'agent.
    CrewAI utilisera le modèle par défaut (config globale / env).
    Cette fonction est là pour le futur (Ollama / Groq, etc.).
    """
    return None


def load_crew(crew_code: str) -> Crew:
    """
    Charge un Crew CrewAI complet à partir du code de crew
    (ex: 'DataDrivenCrew') stocké dans la table `crew`.
    """
    conn = _connect()
    cur = conn.cursor()

    # 1) Récupérer le crew
    cur.execute(
        "SELECT * FROM crew WHERE code = ? AND is_active = 1",
        (crew_code,),
    )
    crew_row = cur.fetchone()
    if crew_row is None:
        conn.close()
        raise ValueError(f"Crew '{crew_code}' not found or inactive in DB.")

    crew_id = crew_row["id"]

    # 2) Récupérer les agents du crew
    cur.execute(
        """
        SELECT a.*
        FROM agent a
        JOIN crew_agent ca ON ca.agent_id = a.id
        WHERE ca.crew_id = ? AND a.is_active = 1
        ORDER BY ca.sort_order, a.id
        """,
        (crew_id,),
    )
    agent_rows = cur.fetchall()

    agents_by_id: Dict[int, Agent] = {}

    for a in agent_rows:
        # V1 : pas de paramètre llm => CrewAI applique son LLM par défaut
        agent_obj = Agent(
            name=a["name"],
            role=a["role"],
            goal=a["goal"],
            backstory=a["backstory"] or "",
            verbose=bool(a["verbose"]),
            allow_delegation=bool(a["allow_delegation"]),
        )
        agents_by_id[a["id"]] = agent_obj

    # 3) Récupérer les tasks du crew
    cur.execute(
        """
        SELECT
            ct.*,
            t.code AS task_code,
            t.name AS task_name,
            t.description AS task_desc,
            t.expected_output
        FROM crew_task ct
        JOIN task t ON t.id = ct.task_id
        WHERE ct.crew_id = ?
        ORDER BY ct.sort_order, ct.id
        """,
        (crew_id,),
    )
    task_rows = cur.fetchall()

    tasks: List[Task] = []

    for t in task_rows:
        agent_id = t["agent_id"]
        if agent_id is None:
            conn.close()
            raise ValueError(
                f"CrewTask id={t['id']} has no agent_id set "
                "(V1 loader requires agent_id not NULL)."
            )

        agent_for_task = agents_by_id.get(agent_id)
        if agent_for_task is None:
            conn.close()
            raise ValueError(
                f"No Agent found for crew_task id={t['id']} (agent_id={agent_id})."
            )

        # ⚠️ IMPORTANT : on NE met PAS input_template dans la description,
        # sinon CrewAI essaie de résoudre {analysis_output} dès le kickoff.
        description = t["task_desc"]

        task_obj = Task(
            description=description,
            expected_output=t["expected_output"],
            agent=agent_for_task,
        )
        tasks.append(task_obj)

    process = crew_row["orchestration"]  # 'sequential', 'hierarchical', etc.

    crew = Crew(
        agents=list(agents_by_id.values()),
        tasks=tasks,
        process=process,
    )

    conn.close()
    return crew
