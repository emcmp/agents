# src/datadriven/seed_datadriven.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "crews.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Provider OpenAI
    cur.execute("""
        INSERT INTO llm_provider (name, base_url, api_key_env)
        VALUES ('openai', NULL, 'OPENAI_API_KEY')
    """)
    provider_id = cur.lastrowid

    # Modèle
    cur.execute("""
        INSERT INTO llm_model (provider_id, code, name, description)
        VALUES (?, 'gpt-4.1-mini', 'GPT-4.1 Mini', 'Default small model')
    """, (provider_id,))
    model_id = cur.lastrowid

    # Agents
    cur.execute("""
        INSERT INTO agent (code, name, role, goal, backstory, llm_model_id, temperature, verbose)
        VALUES (
          'analyst',
          'Analyste de requêtes',
          'Tu es un analyste de requêtes de programmation.',
          'Comprendre précisément ce que l’utilisateur veut faire en code.',
          'Ancien prof de C#, très pédagogue.',
          ?, 0.3, 1
        )
    """, (model_id,))
    analyst_id = cur.lastrowid

    cur.execute("""
        INSERT INTO agent (code, name, role, goal, backstory, llm_model_id, temperature, verbose)
        VALUES (
          'architect',
          'Architecte de solution',
          'Tu es un architecte logiciel senior.',
          'Concevoir la meilleure structure de crew, d’agents, et de tâches.',
          'Tu adores faire des diagrammes mentaux et simplifier les systèmes complexes.',
          ?, 0.4, 1
        )
    """, (model_id,))
    architect_id = cur.lastrowid

    # Crew
    cur.execute("""
        INSERT INTO crew (code, name, description, orchestration)
        VALUES ('DataDrivenCrew', 'Data Driven Crew', 'Crew construit depuis SQLite', 'sequential')
    """)
    crew_id = cur.lastrowid

    # CrewAgent
    cur.execute("""
        INSERT INTO crew_agent (crew_id, agent_id, is_lead, sort_order)
        VALUES (?, ?, 0, 1)
    """, (crew_id, analyst_id))
    cur.execute("""
        INSERT INTO crew_agent (crew_id, agent_id, is_lead, sort_order)
        VALUES (?, ?, 1, 2)
    """, (crew_id, architect_id))

    # Tasks
    cur.execute("""
        INSERT INTO task (code, name, description, expected_output)
        VALUES (
          'analyze_request',
          'Analyser la requête',
          'Analyse la requête de l’utilisateur et clarifie le besoin.',
          'Un résumé structuré de la demande utilisateur et des contraintes.'
        )
    """)
    task_analyze_id = cur.lastrowid

    cur.execute("""
        INSERT INTO task (code, name, description, expected_output)
        VALUES (
          'design_solution',
          'Concevoir la solution',
          'À partir de l’analyse, propose une architecture de crew, agents et tâches.',
          'Une proposition de structure de crew, avec agents, tâches et relations.'
        )
    """)
    task_design_id = cur.lastrowid

    # CrewTask (ordre séquentiel)
    cur.execute("""
        INSERT INTO crew_task (crew_id, task_id, agent_id, sort_order, is_entry_point, input_template)
        VALUES (?, ?, ?, 1, 1, 'User request: {user_input}')
    """, (crew_id, task_analyze_id, analyst_id))
    cur.execute("""
        INSERT INTO crew_task (crew_id, task_id, agent_id, sort_order, is_entry_point, input_template)
        VALUES (?, ?, ?, 2, 0, 'Analysis: {analysis_output}')
    """, (crew_id, task_design_id, architect_id))

    conn.commit()
    conn.close()
    print("Seed done.")

if __name__ == "__main__":
    main()
