#!/usr/bin/env python
import sys
import warnings
import os
from datetime import datetime

from crewmaker.crew import CrewBuilder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

def run():
    spec = "Je veux un crew qui crée d'autres crews pour des tâches de programmation"
    result = CrewBuilder().crew().kickoff(
        inputs={
            "spec": spec,
            "target_dir": r"P:\Projects\AI\EMagents\3_crew\generated_crews"
        }
    )
    print(result.raw)




