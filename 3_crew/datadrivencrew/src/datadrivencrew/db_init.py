# src/datadriven/db_init.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "crews.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

schema_sql = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS llm_provider (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  name          TEXT NOT NULL,        -- 'openai', 'ollama', etc.
  base_url      TEXT,
  api_key_env   TEXT                  -- nom de la variable d'env, ex: 'OPENAI_API_KEY'
);

CREATE TABLE IF NOT EXISTS llm_model (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  provider_id     INTEGER NOT NULL,
  code            TEXT NOT NULL UNIQUE,  -- ex: 'gpt-4.1-mini', 'llama3.1:8b'
  name            TEXT NOT NULL,
  description     TEXT,
  FOREIGN KEY (provider_id) REFERENCES llm_provider(id)
);

CREATE TABLE IF NOT EXISTS agent (
  id               INTEGER PRIMARY KEY AUTOINCREMENT,
  code             TEXT NOT NULL UNIQUE,   -- ex: 'analyst_agent'
  name             TEXT NOT NULL,
  role             TEXT NOT NULL,
  goal             TEXT NOT NULL,
  backstory        TEXT,
  llm_model_id     INTEGER,
  temperature      REAL,
  max_tokens       INTEGER,
  verbose          INTEGER NOT NULL DEFAULT 1,   -- 0/1
  allow_delegation INTEGER NOT NULL DEFAULT 0,   -- 0/1
  is_active        INTEGER NOT NULL DEFAULT 1,
  FOREIGN KEY (llm_model_id) REFERENCES llm_model(id)
);

CREATE TABLE IF NOT EXISTS crew (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  code          TEXT NOT NULL UNIQUE, -- 'DataDrivenCrew'
  name          TEXT NOT NULL,
  description   TEXT,
  orchestration TEXT NOT NULL DEFAULT 'sequential',  -- 'sequential', 'hierarchical', ...
  is_active     INTEGER NOT NULL DEFAULT 1,
  created_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS crew_agent (
  crew_id    INTEGER NOT NULL,
  agent_id   INTEGER NOT NULL,
  is_lead    INTEGER NOT NULL DEFAULT 0,
  sort_order INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (crew_id, agent_id),
  FOREIGN KEY (crew_id) REFERENCES crew(id),
  FOREIGN KEY (agent_id) REFERENCES agent(id)
);

CREATE TABLE IF NOT EXISTS task (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  code            TEXT NOT NULL UNIQUE,    -- ex: 'analyze_request'
  name            TEXT NOT NULL,
  description     TEXT NOT NULL,           -- description / prompt
  expected_output TEXT NOT NULL,
  output_file     TEXT,
  is_active       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS crew_task (
  id             INTEGER PRIMARY KEY AUTOINCREMENT,
  crew_id        INTEGER NOT NULL,
  task_id        INTEGER NOT NULL,
  agent_id       INTEGER,                 -- si NULL, utiliser agent défaut du task plus tard
  sort_order     INTEGER NOT NULL DEFAULT 0,
  is_entry_point INTEGER NOT NULL DEFAULT 0,
  input_template TEXT,                    -- ex: "User request: {user_input}"
  FOREIGN KEY (crew_id) REFERENCES crew(id),
  FOREIGN KEY (task_id) REFERENCES task(id),
  FOREIGN KEY (agent_id) REFERENCES agent(id)
);
"""

def main():
    print(f"Creating DB at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(schema_sql)
        conn.commit()
    finally:
        conn.close()
    print("Schema created.")

if __name__ == "__main__":
    main()
