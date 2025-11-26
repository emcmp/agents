from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew

from crewmaker.tools.project_tools import (
    project_dir_reader,
    project_file_reader,
    project_file_writer,
)

# Utiliser CrewBase comme DÉCORATEUR de la classe
@CrewBase
class CrewBuilder:
    """Crewmaker : un crew qui génère d'autres crews."""

    # Chemins vers les fichiers YAML de config (depuis la racine du projet crewmaker)
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ─────────────────────────
    #         AGENTS
    # ─────────────────────────

    @agent
    def request_interpreter(self) -> Agent:
        return Agent(
            config=self.agents_config["request_interpreter"],
            tools=[project_dir_reader],
            verbose=True,
        )

    @agent
    def crew_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_architect"],
            tools=[project_dir_reader, project_file_reader],
            verbose=True,
        )

    @agent
    def llm_strategy_designer(self) -> Agent:
        """Agent qui conçoit la stratégie LLM (OpenAI / Gemini) et Docker high-level."""
        return Agent(
            config=self.agents_config["llm_strategy_designer"],
            verbose=True,
        )

    @agent
    def yaml_generator(self) -> Agent:
        """Agent qui génère et écrit les fichiers YAML + crew.py dans le target_dir."""
        return Agent(
            config=self.agents_config["yaml_generator"],
            tools=[project_dir_reader, project_file_writer, project_file_reader],
            verbose=True,
        )

    @agent
    def docker_packager(self) -> Agent:
        """Agent qui crée Dockerfile + HOW_TO_RUN.md dans le target_dir."""
        return Agent(
            config=self.agents_config["docker_packager"],
            tools=[project_file_writer],
            verbose=True,
        )

    @agent
    def quality_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_validator"],
            tools=[project_dir_reader, project_file_reader],
            verbose=True,
        )

    @agent
    def crew_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_creator"],
            tools=[project_file_writer, project_dir_reader, project_file_reader],
            verbose=True,
        )

    @agent
    def crew_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_tester"],
            verbose=True,
        )

    # ─────────────────────────
    #         TÂCHES
    # ─────────────────────────

    @task
    def interpret_request(self) -> Task:
        return Task(
            config=self.tasks_config["interpret_request"],
        )

    @task
    def design_crew_architecture(self) -> Task:
        return Task(
            config=self.tasks_config["design_crew_architecture"],
        )

    @task
    def choose_llm_and_docker_strategy(self) -> Task:
        return Task(
            config=self.tasks_config["choose_llm_and_docker_strategy"],
        )

    @task
    def generate_core_files(self) -> Task:
        """Génère config/agents.yaml, config/tasks.yaml et crew.py dans le target_dir."""
        return Task(
            config=self.tasks_config["generate_core_files"],
        )

    @task
    def generate_docker_support(self) -> Task:
        """Génère Dockerfile + HOW_TO_RUN.md dans le target_dir."""
        return Task(
            config=self.tasks_config["generate_docker_support"],
        )

    @task
    def validate_crew_configuration(self) -> Task:
        return Task(
            config=self.tasks_config["validate_crew_configuration"],
        )

    @task
    def create_new_crew(self) -> Task:
        return Task(
            config=self.tasks_config["create_new_crew"],
        )

    @task
    def test_created_crew(self) -> Task:
        return Task(
            config=self.tasks_config["test_created_crew"],
        )

    # ─────────────────────────
    #          CREW
    # ─────────────────────────

    @crew
    def crew(self) -> Crew:
        """Assemble le Crewmaker lui-même."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
