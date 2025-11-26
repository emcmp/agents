# src/crewmaker/crew.py
from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew
from crewai import LLM  # si tu utilises la nouvelle API LLM

from .tools.project_tools import (
    project_dir_reader,
    project_file_reader,
    project_file_writer,
    code_interpreter,
)


@CrewBase
class CrewBuilder:
    """Crew qui conçoit ET matérialise d'autres crews sur disque."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # --- Agents ---

    @agent
    def request_interpreter(self) -> Agent:
        return Agent(
            config=self.agents_config["request_interpreter"],
            # llm=LLM(model="gpt-4.1-mini"),  # adapte ton modèle
            verbose=True,
            tools=[project_dir_reader, project_file_reader],
        )

    @agent
    def crew_architect(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_architect"],
            # llm=LLM(model="gpt-4.1-mini"),
            verbose=True,
            tools=[project_dir_reader, project_file_reader],
        )

    @agent
    def yaml_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["yaml_generator"],
            # llm=LLM(model="gpt-4.1-mini"),
            verbose=True,
            tools=[project_dir_reader, project_file_reader, project_file_writer],
        )

    @agent
    def quality_validator(self) -> Agent:
        return Agent(
            config=self.agents_config["quality_validator"],
            # llm=LLM(model="gpt-4.1-mini"),
            verbose=True,
            tools=[project_dir_reader, project_file_reader],
        )

    @agent
    def crew_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_creator"],
            # llm=LLM(model="gpt-4.1-mini"),
            verbose=True,
            tools=[project_dir_reader, project_file_reader, project_file_writer],
        )

    @agent
    def crew_tester(self) -> Agent:
        return Agent(
            config=self.agents_config["crew_tester"],
            # llm=LLM(model="gpt-4.1-mini"),
            verbose=True,
            tools=[project_dir_reader, project_file_reader, code_interpreter],
        )

    # --- Tasks ---

    @task
    def interpret_request(self) -> Task:
        return Task(config=self.tasks_config["interpret_request"])

    @task
    def design_crew_architecture(self) -> Task:
        return Task(config=self.tasks_config["design_crew_architecture"])

    @task
    def generate_yaml_files(self) -> Task:
        return Task(config=self.tasks_config["generate_yaml_files"])

    @task
    def validate_crew_configuration(self) -> Task:
        return Task(config=self.tasks_config["validate_crew_configuration"])

    @task
    def create_new_crew(self) -> Task:
        return Task(config=self.tasks_config["create_new_crew"])

    @task
    def test_created_crew(self) -> Task:
        return Task(config=self.tasks_config["test_created_crew"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.request_interpreter(),
                self.crew_architect(),
                self.yaml_generator(),
                self.quality_validator(),
                self.crew_creator(),
                self.crew_tester(),
            ],
            tasks=[
                self.interpret_request(),
                self.design_crew_architecture(),
                self.generate_yaml_files(),
                self.validate_crew_configuration(),
                self.create_new_crew(),
                self.test_created_crew(),
            ],
            process=Process.sequential,
            verbose=True,
        )
