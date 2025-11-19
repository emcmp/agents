# MyMemory Crew – Main Functions & Usage

This document explains the purpose of the MyMemory crew, its architecture, and the console script functions defined in `src/mymemory/main.py` (exposed via entry points in `pyproject.toml`). It complements the root `README.md`.

## 1. Project Overview
MyMemory is a lightweight multi-agent research & reporting workflow built on [crewAI]. It uses two collaborating agents:
- **Researcher** – Gathers fresh factual bullet points about a topic.
- **Reporting Analyst** – Synthesizes findings, recalls earlier details using short-term memory, and produces a structured report.

Core characteristics:
- **Local LLM first**: Configured to use an Ollama-hosted model (`openhermes:v2.5`) – no external API key required to start.
- **Sequential process**: Agents run in order (`Process.sequential`) to make memory hand‑off explicit.
- **Agent memory**: Both agents have memory enabled (in code) so later tasks can recall earlier context.
- **Config‑driven**: Roles & tasks are parameterized through `config/agents.yaml` and `config/tasks.yaml` using `{topic}` and other placeholders.

## 2. Architecture Flow
```
main.py (entry points) --> crew.py (Mymemory class) --> crewAI framework
          |                    |                    |
          |                    |--> Agents (researcher, reporting_analyst)
          |                    |--> Tasks (research_task, reporting_task)
          |--> Inputs dict ----> Kickoff / Train / Test / Replay / Trigger
```
- `main.py` acts as a thin CLI façade translating command line arguments into structured crew operations.
- Each function wraps a method on the instantiated crew: `kickoff`, `train`, `replay`, `test`.

## 3. Inputs Convention
Default inputs in most functions:
```python
{
  "topic": "AI LLMs",
  "current_year": "<dynamic YYYY>"
}
```
These fill placeholders in YAML configs so prompts stay time‑aware. `run_with_trigger` allows full input override via a JSON payload.

## 4. Function Reference (main.py)
Below each function you get: Purpose, When to Use, Arguments, Example.

### 4.1 `run()`
- **Purpose**: Executes a single standard crew run producing `report.md`.
- **When**: Quick research/report generation with default topic.
- **Arguments**: None (inputs constructed internally).
- **Example**:
```powershell
uv run run_crew
# or (same entry point alias)
uv run mymemory
```

### 4.2 `train()`
- **Purpose**: Iteratively runs the crew to refine or accumulate outputs, saving each iteration to a file.
- **When**: You want multiple passes (e.g., evolving memory, collecting comparative outputs).
- **Arguments (CLI)**:
  - `n_iterations` (int) – number of training cycles.
  - `filename` (str) – output file to persist training results/log.
- **Example**:
```powershell
uv run train 5 training_log.md
```
- **Notes**: Uses `crew().train(...)`. Depending on crewAI version, this may support internal evaluation or memory enrichment.

### 4.3 `replay()`
- **Purpose**: Re-run (inspect or reproduce) a past task execution by `task_id`—useful for debugging agent behavior or memory effects.
- **When**: Verifying what an agent did, auditing outputs, or regenerating after environment changes.
- **Arguments**:
  - `task_id` (str) – Identifier of prior task execution (from logs or crewAI output metadata).
- **Example**:
```powershell
uv run replay research_task_2025-11-18T09-30-12
```

### 4.4 `test()`
- **Purpose**: Performs evaluation runs using a specified evaluation LLM (e.g., a deterministic or higher-quality model) over multiple iterations.
- **When**: Benchmarking output quality, regression testing prompt changes, comparing memory retention across runs.
- **Arguments**:
  - `n_iterations` (int) – Number of evaluation runs.
  - `eval_llm` (str) – Model name string passed through to evaluation (e.g. `gpt-4o-mini`, `ollama/openhermes:v2.5`).
- **Example**:
```powershell
uv run test 3 gpt-4o-mini
```
- **Notes**: Produces aggregate evaluation context; pair with version control to track improvements.

### 4.5 `run_with_trigger()`
- **Purpose**: Programmatic kickoff with dynamic JSON payload (e.g., event-driven pipeline, webhook, scheduler).
- **When**: External system passes runtime parameters (topic, year, custom flags) at invocation time.
- **Arguments**:
  - Single CLI arg: JSON string (`trigger_payload`).
- **Input Construction**: Wraps payload in `inputs` under key `crewai_trigger_payload` (other placeholders left blank if not provided).
- **Example**:
```powershell
uv run run_with_trigger '{"topic":"Open Source LLMs","current_year":"2025","custom_flag":true}'
```
- **Return**: Returns the run result (can be captured if called programmatically).

## 5. Error Handling Pattern
Each function wraps crew calls in `try/except` and re-raises with contextual message:
```python
except Exception as e:
    raise Exception("An error occurred while <action>: {e}")
```
Reasoning: surfaces origin (run/train/replay/test/trigger) while preserving stack trace for upstream logging.

## 6. Customization Guide
- **Change Default Topic**: Edit the `inputs` dictionaries in `main.py` or supply via `run_with_trigger`.
- **Add More Inputs**: Introduce new placeholders in YAML (`{industry}`, `{region}`) then add keys to `inputs` before kickoff.
- **Extend Agents**: Add methods with `@agent` in `crew.py` and reference them in tasks YAML.
- **Parallelization**: Switch `process=Process.sequential` to `Process.parallel` (if tasks independent and memory usage is adapted).
- **Alternate Models**: Replace `ollama/openhermes:v2.5` with any local model you have pulled via Ollama (`ollama pull llama3`).

## 7. Typical Workflows
| Goal | Command | Notes |
|------|---------|-------|
| Single report | `uv run run_crew` | Creates/updates `report.md` |
| Iterative refinement | `uv run train 4 iteration_log.md` | Observe changes per pass |
| Debug past task | `uv run replay <task_id>` | Requires stored ID |
| Benchmark quality | `uv run test 5 gpt-4o-mini` | Compare model outputs |
| Event-driven run | `uv run run_with_trigger '{"topic":"MLOps"}'` | Integrate with CI/CD |

## 8. Choosing the Right Function
- Use **`run`** for standard single execution.
- Use **`train`** when you need multiple passes and output accumulation.
- Use **`test`** for evaluation/regression benchmarking with a chosen model.
- Use **`replay`** for forensic analysis of a prior run.
- Use **`run_with_trigger`** inside automations or systems passing runtime parameters.

## 9. Programmatic Invocation
Instead of console scripts:
```python
from mymemory.main import run, train
run()                  # default single execution
train()                # requires CLI args when called as script; programmatic adaptation recommended
```
For custom programmatic train invocation, adapt `train()` to accept explicit parameters (recommended if embedding in a larger app).

## 10. Next Extensions (Ideas)
- Add persistent vector memory (e.g., Chroma) per agent.
- Introduce a quality gate that aborts reporting if research bullet count < threshold.
- Add `export_json` function wrapping results for downstream pipelines.

## 11. Troubleshooting Quick Tips
| Issue | Cause | Fix |
|-------|-------|-----|
| Empty `report.md` | Model or tasks misconfigured | Verify YAML placeholders & model availability |
| Ollama connection error | Base URL wrong / server not running | Start Ollama: `ollama serve` and confirm port 11434 |
| Replay fails | Invalid `task_id` | List available IDs from stored run metadata/logs |
| Test model mismatch | `eval_llm` not installed locally | Pull or switch to available model |

## 12. Why Separate Functions?
- **Clear entry points**: Each user goal is mapped to a distinct command—simplifies observability & scripting.
- **Operational segregation**: Training/evaluation runs have different performance and logging needs than standard runs.
- **Composable automation**: `run_with_trigger` supports external orchestration without modifying internal logic.
- **Maintainability**: Changes in crew construction (`crew.py`) do not require altering top-level function semantics.

---
**Summary**: `main.py` provides a focused, intention-revealing CLI surface for orchestrating a memory-enabled, sequential research-reporting crew. Choose the function matching your operational goal (single run, iterative refinement, replay, benchmarking, or triggered execution) and customize inputs/configs as needed.
