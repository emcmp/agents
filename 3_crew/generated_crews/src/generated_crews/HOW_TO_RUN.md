# Comment exécuter votre projet CrewAI avec Docker

Ce guide vous explique comment construire et exécuter votre projet CrewAI dans un conteneur Docker.

## Prérequis

Assurez-vous d'avoir Docker installé sur votre machine.

## 1. Construire l'image Docker

Naviguez jusqu'au répertoire racine de votre projet (là où se trouve le `Dockerfile`) et exécutez la commande suivante :

```bash
docker build -t mon-crew-ia .
```

-   `docker build`: Commande pour construire une image Docker.
-   `-t mon-crew-ia`: Permet de tagger votre image avec un nom (`mon-crew-ia` dans cet exemple). Vous pouvez choisir n'importe quel nom significatif.
-   `.`: Indique que le `Dockerfile` se trouve dans le répertoire courant.

## 2. Lancer le conteneur Docker

Votre CrewAI nécessite des clés API pour interagir avec les modèles LLM (OpenAI ou Google Gemini). Ces clés doivent être fournies via des variables d'environnement lors de l'exécution du conteneur.

### Variables d'environnement requises

*   **`OPENAI_API_KEY`**: Votre clé API pour OpenAI.
*   **`GOOGLE_API_KEY`**: Votre clé API pour Google Gemini.

### Variables d'environnement optionnelles pour la configuration LLM

Le `Dockerfile` définit des valeurs par défaut, mais vous pouvez les surcharger :

*   **`LLM_PROVIDER`**: Spécifie le fournisseur LLM à utiliser. Valeurs possibles : `OPENAI` (par défaut) ou `GEMINI`.
*   **`OPENAI_MODEL`**: Le nom du modèle OpenAI à utiliser (par défaut : `gpt-4o`). Ex: `gpt-4o-mini`, `gpt-3.5-turbo`.
*   **`GEMINI_MODEL`**: Le nom du modèle Google Gemini à utiliser (par défaut : `gemini-1.5-pro`). Ex: `gemini-1.5-flash`.

### Exemples de commandes `docker run`

#### A. Exécuter avec OpenAI (gpt-4o par défaut)

```bash
docker run -e OPENAI_API_KEY="sk-votre_cle_openai_ici" \
           -e LLM_PROVIDER="OPENAI" \
           mon-crew-ia
```

Si vous souhaitez utiliser un modèle OpenAI spécifique (par exemple, `gpt-4o-mini`) :

```bash
docker run -e OPENAI_API_KEY="sk-votre_cle_openai_ici" \
           -e LLM_PROVIDER="OPENAI" \
           -e OPENAI_MODEL="gpt-4o-mini" \
           mon-crew-ia
```

#### B. Exécuter avec Google Gemini (gemini-1.5-pro par défaut)

```bash
docker run -e GOOGLE_API_KEY="votre_cle_google_gemini_ici" \
           -e LLM_PROVIDER="GEMINI" \
           mon-crew-ia
```

Si vous souhaitez utiliser un modèle Google Gemini spécifique (par exemple, `gemini-1.5-flash`) :

```bash
docker run -e GOOGLE_API_KEY="votre_cle_google_gemini_ici" \
           -e LLM_PROVIDER="GEMINI" \
           -e GEMINI_MODEL="gemini-1.5-flash" \
           mon-crew-ia
```

**Note importante :** Remplacez `"sk-votre_cle_openai_ici"` et `"votre_cle_google_gemini_ici"` par vos véritables clés API. Ne partagez jamais vos clés API.

## 3. Exécution du Crew

Une fois le conteneur lancé avec les bonnes variables d'environnement, le script `crew.py` sera exécuté automatiquement et votre CrewAI commencera son travail. Les logs de l'exécution seront affichés dans votre terminal.