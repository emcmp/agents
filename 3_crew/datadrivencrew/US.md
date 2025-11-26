🧩 Backlog – User Stories (CrewViewer)
🟦 1. Gestion des Crews (CRUD complet)
US-001 — Voir tous les crews

En tant qu’utilisateur, je veux voir une liste claire des crews stockés dans la base SQLite afin de naviguer rapidement vers le détail d’un crew.

US-002 — Voir le blueprint d’un crew

En tant qu’utilisateur, je veux voir le blueprint d’un crew (structure, tâches, agents, pipeline visuel) afin de comprendre comment il fonctionne.

US-003 — Créer un nouveau crew à partir de zéro

En tant qu’utilisateur, je veux créer un nouveau crew vide depuis l’interface afin de commencer à le modifier.

US-004 — Cloner un crew existant

En tant qu’utilisateur, je veux dupliquer un crew existant pour créer une nouvelle version sans repartir de zéro.

US-005 — Modifier un crew existant

En tant qu’utilisateur, je veux modifier le nom, la description, l’orchestration, les agents liés et les tasks afin d’ajuster la logique du crew.

US-006 — Supprimer un crew

En tant qu’utilisateur, je veux supprimer un crew afin de garder la base propre.

🟧 2. Gestion des Agents
US-010 — Voir la liste des agents

En tant qu’utilisateur, je veux voir la liste des agents de la base et leurs propriétés (nom, rôle, LLM…).

US-011 — Modifier un agent

En tant qu’utilisateur, je veux ajuster le rôle, la backstory, la température, les paramètres LLM, etc.

US-012 — Ajouter un agent

En tant qu’utilisateur, je veux créer de nouveaux agents pour les réutiliser dans différents crews.

US-013 — Définir agents de chaque tâche d’un crew

En tant qu’utilisateur, je veux choisir quel agent prend quelle tâche dans un crew.

🟩 3. Gestion des Tâches
US-020 — Gérer les tasks (CRUD)

En tant qu’utilisateur, je veux créer, modifier et supprimer des tasks globales pour les réutiliser dans des crews.

US-021 — Ordonner les tasks dans un crew

En tant qu’utilisateur, je veux modifier l’ordre d’exécution des tasks d’un crew (drag & drop ou boutons ↑ ↓).

🟪 4. Exécution d’un crew
US-030 — Exécuter un crew depuis l’interface

En tant qu’utilisateur, je veux lancer l’exécution complète d’un crew en lui passant des paramètres.

US-031 — Voir la progression en temps réel

En tant qu’utilisateur, je veux visualiser en temps réel les réponses des agents pendant l’exécution.

US-032 — Sauvegarder les outputs dans la base

En tant qu’utilisateur, je veux que chaque output de task soit sauvegardé dans une table ExecutionOutputs.

US-033 — Télécharger un rapport d’exécution (.md ou .txt)

En tant qu’utilisateur, je veux télécharger le résultat final sous forme de fichier Markdown ou ZIP.

US-034 — Rejouer une exécution passée

En tant qu’utilisateur, je veux relancer un crew avec les mêmes paramètres qu’une exécution précédente.

🟥 5. Gestion des Tools
US-040 — Voir la liste des tools disponibles

En tant qu’utilisateur, je veux voir la liste des tools configurés pour CrewAI.

US-041 — Ajouter un Tool

En tant qu’utilisateur, je veux ajouter un nouveau tool (Python, HTTP, DB, File…).

US-042 — Associer des Tools à des agents

En tant qu’utilisateur, je veux choisir quels tools un agent peut utiliser.

US-043 — Tester un Tool depuis l’interface

En tant qu’utilisateur, je veux exécuter un tool manuellement pour m’assurer qu’il fonctionne.

🟨 6. Gestion des modèles LLM
US-050 — Voir les modèles LLM disponibles

En tant qu’utilisateur, je veux voir tous les modèles supportés (OpenAI, Groq, Anthropic, Local / Ollama).

US-051 — Modifier le LLM d’un agent

En tant qu’utilisateur, je veux modifier rapidement le modèle utilisé par un agent.

US-052 — Configurer la connexion aux LLM locaux

En tant qu’utilisateur, je veux paramétrer l’URL d’un endpoint local (ex: http://localhost:11434).

🟫 7. Gestion des fichiers & outputs
US-060 — Définir un répertoire local pour stocker les outputs

En tant qu’utilisateur, je veux définir un chemin où les outputs d’un crew seront stockés automatiquement.

US-061 — Visualiser les fichiers générés

En tant qu’utilisateur, je veux voir directement dans le viewer les fichiers générés (markdown, JSON, images…).

US-062 — Télécharger l’ensemble des outputs d’une exécution

En tant qu’utilisateur, je veux télécharger un ZIP de tous les résultats générés par le crew.

🟫 8. UX & Visualisation avancée
US-070 — Pipeline visual

En tant qu’utilisateur, je veux un pipeline visuel animé (flowchart) pour comprendre le déroulement du crew.

US-071 — Mouse-over sur les agents

En tant qu’utilisateur, je veux afficher des détails sur un agent en survolant son nom.

US-072 — Mode clair / foncé

En tant qu’utilisateur, je veux pouvoir basculer entre un thème sombre et clair.

US-073 — Recherche / Filtre

En tant qu’utilisateur, je veux filtrer les crews, agents ou tasks par nom ou tag.