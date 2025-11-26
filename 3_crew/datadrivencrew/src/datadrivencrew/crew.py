# src/datadrivencrew/crew.py

from crewai import Crew
from .db_loader import load_crew

class DataDrivenCrew:
    def __init__(self):
        # tu peux mettre le code du crew en dur ou le passer au constructeur
        self._crew: Crew = load_crew("DataDrivenCrew")

    def crew(self) -> Crew:
        return self._crew

    def run(self, user_input: str):
        # API simple pour run_crew.py
        return self._crew.kickoff(inputs={"user_input": user_input})
