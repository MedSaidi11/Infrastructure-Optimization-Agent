# Choix Techniques et Architecturaux

## Architecture

L'application utilise une architecture découplée en deux parties :
- Un serveur MCP (Model Context Protocol) qui expose les outils d'analyse
- Un agent d'analyse qui orchestre le workflow via LangGraph

Cette séparation permet de faire évoluer indépendamment les outils et la logique métier.

## Langage et environnement

**Python 3.12** a été choisi pour ses nouvelles fonctionnalités de typing et sa performance améliorée.

**UV** remplace pip/poetry pour la gestion des dépendances. Il est beaucoup plus rapide et génère automatiquement un fichier de lock pour garantir la reproductibilité.

## Modèle de langage

**Mistral Large** via l'API Mistral AI pour plusieurs raisons :
- Excellentes capacités d'analyse technique
- Intégration simple avec LangChain

## Bibliothèques principales

**LangGraph** gère le workflow d'analyse en 4 étapes :
1. Lecture du rapport JSON
2. Détection d'anomalies 
3. Génération de recommandations
4. Présentation des résultats

Cette approche permet une gestion d'erreurs robuste et facilite le débogage.

**Pydantic** structure les réponses du LLM avec des modèles de données typés. Cela évite les erreurs de format et valide automatiquement les sorties.

**FastMCP** implémente le serveur d'outils selon le protocole MCP standard, permettant une intégration propre avec les agents IA.

## Gestion des données

Les modèles Pydantic définissent la structure des anomalies et recommandations :

```python
class Anomaly(BaseModel):
    metric: str
    timestamp: list[str] 
    value: list[str]
    description: str
    potential_impact: str
```

L'état du workflow est géré via `TypedDict` pour la compatibilité avec LangGraph.

## Outils et déploiement

Un `Makefile` simple automatise l'installation et le lancement :
- `make install` : installe les dépendances avec uv
- `make run` : démarre le serveur MCP puis l'agent

Le serveur MCP démarre en arrière-plan, on attend 3 secondes qu'il soit prêt, puis on lance l'analyse.

## Gestion d'erreurs

Chaque étape du workflow est protégée par un try/catch. En cas d'erreur, l'état global est mis à jour et le workflow s'arrête proprement.

Les logs utilisent Loguru pour un affichage coloré et structuré facilitant le débogage.

## Évolutions possibles

L'architecture modulaire permet d'ajouter facilement :
- De nouveaux outils d'analyse dans le serveur MCP
- Des étapes supplémentaires dans le workflow LangGraph  
