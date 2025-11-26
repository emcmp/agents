
# src/datadrivencrew/db_tools.py
import json
import sqlite3
from pydantic import BaseModel, Field
from typing import List, Optional

from crewai_tools import BaseTool  # ou crewai.tools.BaseTool selon ta version


DB_PATH = "data/crews.db"  # ou via variable d'env / config


class AgentSpec(BaseModel):
    code: str
    name: str
    role: str
    goal: str
    backstory: Optional[str] = None
    verbose: bool = True
    allow_delegation: bool = False
    is_active: bool = True


class TaskSpec(BaseModel):
    code: str
    name: str
    description: str
    expected_output: str
    is_entry_point: bool = False
    sort_order: int = 1
    agent_code: str
    input_template: Optional[str] = None


class CrewSpec(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    orchestration: str = "sequential"
    is_active: bool = True


class InsertCrewArgs(BaseModel):
    spec_json: str = Field(
        ...,
        description="JSON décrivant le crew, ses agents et ses tâches."
    )


class InsertCrewConfigTool(BaseTool):
    name: str = "insert_crew_config"
    description: str = (
        "Insère un nouveau crew avec ses agents et ses tâches dans la base SQLite. "
        "Attends un JSON conforme au schéma: { crew, agents[], tasks[] }."
    )
    args_schema = InsertCrewArgs

    def _run(self, spec_json: str) -> str:
        data = json.loads(spec_json)

        crew_spec = CrewSpec(**data["crew"])
        agents_spec = [AgentSpec(**a) for a in data.get("agents", [])]
        tasks_spec = [TaskSpec(**t) for t in data.get("tasks", [])]

        conn = sqlite3.connect(DB_PATH)
        try:
            cur = conn.cursor()

            # 1) Crew
            cur.execute(
                """
                INSERT INTO crew (code, name, description, orchestration, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (
                    crew_spec.code,
                    crew_spec.name,
                    crew_spec.description,
                    crew_spec.orchestration,
                    1 if crew_spec.is_active else 0,
                ),
            )
            crew_id = cur.lastrowid

            # 2) Agents (avec dictionnaire code → id)
            agent_id_by_code = {}
            for a in agents_spec:
                cur.execute(
                    """
                    INSERT INTO agent
                      (code, name, role, goal, backstory, verbose, allow_delegation, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        a.code,
                        a.name,
                        a.role,
                        a.goal,
                        a.backstory,
                        1 if a.verbose else 0,
                        1 if a.allow_delegation else 0,
                        1 if a.is_active else 0,
                    ),
                )
                agent_id = cur.lastrowid
                agent_id_by_code[a.code] = agent_id

                # lien crew_agent
                cur.execute(
                    "INSERT INTO crew_agent (crew_id, agent_id, is_lead, sort_order) VALUES (?, ?, ?, ?)",
                    (crew_id, agent_id, 0, 1),
                )

            # 3) Tasks + crew_task
            for t in tasks_spec:
                cur.execute(
                    """
                    INSERT INTO task (code, name, description, expected_output, is_active)
                    VALUES (?, ?, ?, ?, 1)
                    """,
                    (
                        t.code,
                        t.name,
                        t.description,
                        t.expected_output,
                    ),
                )
                task_id = cur.lastrowid

                agent_id = agent_id_by_code.get(t.agent_code)

                cur.execute(
                    """
                    INSERT INTO crew_task
                      (crew_id, task_id, agent_id, sort_order, is_entry_point, input_template)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        crew_id,
                        task_id,
                        agent_id,
                        t.sort_order,
                        1 if t.is_entry_point else 0,
                        t.input_template,
                    ),
                )

            conn.commit()
        finally:
            conn.close()

        return f"Crew '{crew_spec.code}' inséré avec succès (id={crew_id})."
