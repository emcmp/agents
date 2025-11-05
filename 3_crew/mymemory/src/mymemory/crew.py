from crewai import Agent, Crew, Process, Task, LLM  # type: ignore
from crewai.project import CrewBase, agent, crew, task  # type: ignore


@CrewBase
class Mymemory:
    """Mymemory crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # One local LLM for the whole crew (no OpenAI key needed)
    ollama = LLM(
        model="ollama/openhermes:v2.5",     # format: ollama/model_name
        base_url="http://localhost:11434", # your local Ollama endpoint
    )

    # ---- Agents ----
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore[index]
            verbose=True,
            llm=self.ollama,
            memory=True,          # enables agent memory within the run
            max_iter=3,
            allow_delegation=False,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],  # type: ignore[index]
            verbose=True,
            llm=self.ollama,
            memory=True,          # enables agent memory within the run
            max_iter=3,
            allow_delegation=False,
        )

    # ---- Tasks ----
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],  # type: ignore[index]
            output_file="report.md",
        )

    # ---- Crew ----
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,    # auto from @agent
            tasks=self.tasks,      # auto from @task
            process=Process.sequential,
            verbose=True,
        )
