
# src/datadrivencrew/test_db_loader.py

from .db_loader import load_crew


def main():
    crew = load_crew("DataDrivenCrew")

    print("=== Agents ===")
    for agent in crew.agents:
        # .role n’est pas toujours exposé en propriété, donc on affiche au moins name
        print(" -", getattr(agent, "name", agent))

    print("\n=== Tasks ===")
    for i, task in enumerate(crew.tasks, start=1):
        print(f"Task {i}:")
        print("  description:", task.description.split("\n")[0][:80], "...")
        print("  expected_output:", task.expected_output.split("\n")[0][:80], "...\n")

    # Test complet : lancer un kickoff si tu as bien ton OPENAI_API_KEY
    print("\n=== Kickoff ===")
    result = crew.kickoff(
        inputs={
            "user_input": "Explique comment ce crew data-driven est construit à partir de SQLite."
        }
    )
    print(result)


if __name__ == "__main__":
    main()
