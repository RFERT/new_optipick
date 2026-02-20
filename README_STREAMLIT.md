# 🚀 OPTIPICK - Interface Streamlit Interactive

Interface web interactive pour visualiser et simuler l'optimisation des tournées d'entrepôt.

## 📋 Fonctionnalités

### 1. **🏠 Accueil**

- Vue globale du projet OPTIPICK
- Plan de l'entrepôt avec zones codées par couleur
- Informations sur les agents et les commandes

### 2. **📋 Allocation des commandes**

- Exécuter l'allocation Jour 2 (First-Fit avec contraintes)
- Visualiser les commandes assignées à chaque agent
- Vérifier le respect des capacités et contraintes
- Détails produit par commande

### 3. **🚀 Simulation des déplacements**

- Optimiser les routes avec TSP (Traveling Salesman Problem)
- Visualiser les trajets sur le plan d'entrepôt
- Afficher le chemin détaillé avec numérotation des étapes
- Métriques : distance, temps, nombre d'emplacements

### 4. **📊 Statistiques & Optimisation**

- Résultats Jour 3 : Distances et temps par agent
- Résultats Jour 4 : Équilibre de charge
- Graphiques comparatifs

### 5. **🔍 Analyse Jour 5**

- Fréquence des produits
- Top 10 produits les plus commandés
- Recommandations pour le stockage et les agents
- Stratégies d'optimisation future

## 🛠️ Installation

### 1. Installez les dépendances Streamlit

```bash
pip install -r requirements_streamlit.txt
```

### 2. Assurez-vous que les fichiers JSON sont présents

```
data/
├── warehouse.json
├── products.json
├── agents.json
└── orders.json
```

## 🎯 Utilisation

### Lancer l'application

```bash
cd c:\Users\rolan\Documents\HETIC\Deuxième_année\FORGE\Projet_OPTIPICK
streamlit run app_streamlit.py
```

### Workflow recommandé

1. **Accueil** : Comprendre l'entrepôt
2. **Allocation** : Voir comment les commandes sont distribuées
3. **Simulation** : Optimiser les routes avec TSP
4. **Statistiques** : Analyser les résultats des Jours 3-4
5. **Jour 5** : Obtenir les recommandations d'optimisation

## 🎨 Interface

### Navigation

- Barre latérale : Sélectionner la page
- Boutons interactifs : Lancer les analyses
- Dropdowns : Sélectionner les agents

### Visualisations

#### Plan d'Entrepôt

```
┌──────────────────────────────────────┐
│ 🔴 Électronique  🔵 Livres           │
│ 🟦 Alimentaire   🟨 Chimie           │
│ 🟪 Textile       🟩 Allées           │
└──────────────────────────────────────┘
```

Légende des agents :

- 🔵 Robots (R1, R2, R3)
- 🟢 Humains (H1, H2)
- 🟠 Chariots (C1, C2)
- ⭐ Entrée (0, 0)

#### Routes d'agents

- Ligne bleue : Trajet optimisé
- Points numérotés : Ordre de visite
- X jaune : Entrée (point de départ/retour)

## 📊 Résultats

### Allocation (Jour 2)

```
Agent | Commandes | Poids | Volume | Capacité
------|-----------|-------|--------|----------
R1    | 4         | 12kg  | 25dm³  | 20kg/30dm³
H1    | 3         | 18kg  | 35dm³  | 35kg/50dm³
```

### TSP Optimisé (Jour 3)

- Distance totale minimisée
- Temps de tournée estimé
- Chemin détaillé avec étapes

### Jour 4 : Équilibre

- Charge moyenne par agent
- Écart-type (mesure de déséquilibre)
- Graphique de répartition

### Jour 5 : Stockage

- Top 10 produits fréquents
- Recommandations zones
- Stratégies d'investissement

## 🔧 Configuration

### Modifier les données

Éditez les fichiers JSON dans `data/` :

```json
{
  "id": "Product_001",
  "name": "Laptop",
  "location": [1, 1],
  "frequency": "high"
}
```

### Personnaliser les couleurs

Dans `app_streamlit.py`, modifiez `zone_colors` :

```python
zone_colors = {
    'A': '#FF6B6B',      # Rouge
    'B': '#4ECDC4',      # Turquoise
    ...
}
```

## 🚨 Dépannage

### Erreur : "No such file or directory: data/warehouse.json"

- Vérifiez que vous lancez depuis le bon répertoire
- Vérifiez les chemins JSON dans `utils.py`

### Erreur : "ModuleNotFoundError: No module named 'streamlit'"

```bash
pip install streamlit
```

### L'application est lente

- Utilisez `@st.cache_resource` pour mettre en cache les données
- Limitez la taille des graphiques
- Utilisez moins de points de données

## 📈 Améliorations futures

- [ ] Animation des déplacements en temps réel
- [ ] Export PDF des rapports
- [ ] Simulation multi-jours
- [ ] Intégration OR-Tools CP-SAT
- [ ] Dashboard de performance en direct
- [ ] Gestion d'incidents (panne robot, etc.)

## 📝 Notes

- Les routes sont optimisées avec l'heuristique Nearest Neighbor
- Les distances utilisent la métrique Manhattan
- Les contraintes du Jour 2 sont toutes vérifiées
- Les données sont chargées en cache pour performance

## 👤 Auteur

Projet OPTIPICK - HETIC L2 Informatique
Programmation Logique et par Contraintes

---

**Besoin d'aide ?** Consultez les docstrings dans `app_streamlit.py` et `suite.py`
