"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                   OPTIPICK - GUIDE D'UTILISATION COMPLET                     ║
║                    Interface Streamlit Interactive                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝

📚 TABLE DES MATIÈRES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Installation et lancement
2. Pages et fonctionnalités
3. Workflow recommandé
4. Interprétation des résultats
5. Dépannage
6. Personnalisation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


🚀 1. INSTALLATION ET LANCEMENT
═════════════════════════════════════════════════════════════════════════════════

PRÉREQUIS
─────────────────────────────────────────────────────────────────────────────
- Python 3.8+
- Pip (gestionnaire de paquets Python)
- Les fichiers JSON (data/*.json) présents dans le répertoire project


ÉTAPES D'INSTALLATION
─────────────────────────────────────────────────────────────────────────────

Option A : Automatique (Windows)
  1. Double-cliquez sur : launch_app.bat
  ✓ L'application se lance automatiquement

Option B : PowerShell
  1. Ouvrez PowerShell dans le répertoire du projet
  2. Exécutez : .\launch_app.ps1
  3. Si erreur de permission, exécutez d'abord :
     Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Option C : Terminal (tous systèmes)
  1. cd c:\Users\rolan\Documents\HETIC\Deuxième_année\FORGE\Projet_OPTIPICK
  2. streamlit run app_streamlit.py

SORTIE ATTENDUE
─────────────────────────────────────────────────────────────────────────────
  2024-XX-XX XX:XX:XX.XXX
  Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.
  
    You can now view your Streamlit app in your browser.
  
    Local URL: http://localhost:8501
    Network URL: http://XXX.XXX.XXX.XXX:8501

L'application s'ouvre automatiquement dans votre navigateur. Sinon, allez à :
http://localhost:8501


📖 2. PAGES ET FONCTIONNALITÉS
═════════════════════════════════════════════════════════════════════════════════

PAGE 1 : 🏠 ACCUEIL
─────────────────────────────────────────────────────────────────────────────
Affiche : Vue d'ensemble du projet
- Dimensions et zones de l'entrepôt
- Types et nombres d'agents
- Nombre de commandes et produits

Vue interactive de l'entrepôt :
  🔴 Zone A (Électronique)      - Produits rapides/légers
  🔵 Zone B (Livres)            - Produits moyens
  🟦 Zone C (Alimentaire)       - Frigo (accès humains seulement)
  🟨 Zone D (Chimie)            - Produits dangereux (humains seulement)
  🟪 Zone E (Textile)           - Réserve
  ⭐ Entrée (0,0)               - Point de départ/retour

Symboles des agents :
  ● Point bleu   = Robot (rapide, léger)
  ● Point vert   = Humain (polyvalent)
  ● Point orange = Chariot (capacité élevée)


PAGE 2 : 📋 ALLOCATION DES COMMANDES
─────────────────────────────────────────────────────────────────────────────
Fonction : Distribuer les commandes aux agents

ÉTAPES :

  1) Cliquez sur "🔄 Lancer l'allocation (Jour 2)"
     → Exécute l'algorithme First-Fit avec contraintes

  2) Consultez le tableau des résultats :
     ┌─────────────────────────────────────────────────────────────────┐
     │ Agent │ Commandes │ Poids  │ Volume  │ Capacité Poids          │
     ├─────────────────────────────────────────────────────────────────┤
     │ R1    │ 4         │ 12kg   │ 25dm³   │ 20kg / 30dm³            │
     │ R2    │ 4         │ 13kg   │ 27dm³   │ 20kg / 30dm³            │
     │ R3    │ 4         │ 14kg   │ 28dm³   │ 20kg / 30dm³            │
     │ H1    │ 0         │ 0kg    │ 0dm³    │ 35kg / 50dm³            │
     └─────────────────────────────────────────────────────────────────┘

  3) Sélectionnez un agent dans le dropdown pour voir les détails
     → Liste des commandes assignées
     → Produits dans chaque commande
     → Poids et volume individuels


INTERPRÉTATION
─────────────────────────────────────────────────────────────────────────────
✅ BON : Tous les agents utilisés, charge distribuée
❌ MAUVAIS : Un agent surchargé, autres inactifs


PAGE 3 : 🚀 SIMULATION DES DÉPLACEMENTS
─────────────────────────────────────────────────────────────────────────────
Fonction : Optimiser les routes avec TSP (Traveling Salesman Problem)

ÉTAPES :

  1) Cliquez sur "🔄 Optimiser les routes avec TSP"
     → Calcule l'ordre optimal de visite pour chaque agent

  2) Visualisez les métriques globales :
     • Distance totale : Somme distances de tous les agents
     • Temps total : Temps total d'exécution
     • Distance moyenne : Distance par agent

  3) Sélectionnez un agent dans le dropdown
     → Affiche la route sur le plan d'entrepôt
     → Les étapes sont numérotées (0 = entrée, 1-N = emplacements)
     → Tableau du chemin détaillé (X, Y pour chaque étape)


GRAPHIQUE DE ROUTE
─────────────────────────────────────────────────────────────────────────────
Exemple pour agent R1 :
    0
    ├─→ 1 (Premier produit)
    ├─→ 2 (Deuxième produit)
    ├─→ 3 (Troisième produit)
    └─→ 0 (Retour à l'entrée)

Distance : 12.5m
Temps : 6.3 minutes


INTERPRÉTATION
─────────────────────────────────────────────────────────────────────────────
✅ EFFICACE : Route courte, peu d'allers-retours
❌ INEFFICACE : Route longue, zigzags, loin de l'entrée


PAGE 4 : 📊 STATISTIQUES & OPTIMISATION
─────────────────────────────────────────────────────────────────────────────
Fonction : Analyser les résultats des Jours 3 et 4

JOUR 3 : OPTIMISATION DES TOURNÉES
  Cliquez : "🔄 Analyser Jour 3"
  
  Résultats :
  • Graphique 1 : Distance par agent (m)
  • Graphique 2 : Temps de tournée par agent (min)
  
  Exemple :
    R1 : 48m en 24min
    R2 : 52m en 26min
    R3 : 45m en 22.5min

JOUR 4 : ALLOCATION OPTIMALE
  Cliquez : "🔄 Analyser Jour 4"
  
  Résultats :
  • Charge moyenne par agent
  • Écart-type (mesure du déséquilibre)
  • Graphique de répartition
  
  Exemple :
    Charge moyenne : 3.2 commandes
    Écart-type : 0.45 (bon équilibre)
    
  Interprétation :
  - Écart-type faible (< 1) = bonne répartition
  - Écart-type élevé (> 2) = déséquilibre

GRAPHIQUES
─────────────────────────────────────────────────────────────────────────────
  Jour 3 Distance :          Jour 3 Temps :         Jour 4 Charge :
  ┌────────────┐            ┌────────────┐        ┌────────────┐
  │ R1: 48m    │            │ R1: 24min  │        │ R1: 4 com  │
  │ R2: 52m    │            │ R2: 26min  │        │ R2: 3 com  │
  │ R3: 45m    │            │ R3: 22min  │        │ R3: 5 com  │
  └────────────┘            └────────────┘        └────────────┘


PAGE 5 : 🔍 ANALYSE JOUR 5
─────────────────────────────────────────────────────────────────────────────
Fonction : Optimiser le stockage et donner des recommandations

ÉTAPES :

  1) Cliquez sur "🔄 Analyser le stockage"
     → Analyse tous les patterns de commandes

  2) Graphique TOP 10 des produits commandés
     Produit                    | Nombre de fois
     ────────────────────────────────────────────
     USB Cable                  | 45 fois
     Laptop Dell XPS            | 38 fois
     Souris Gaming              | 35 fois
     ...

  3) Recommandations :

     STRATÉGIE AGENTS :
     • Robots → Produits légers (< 10kg)
     • Humains → Produits fragiles
     • Chariots → Volumes élevés (> 50dm³)

     ORGANISATION ZONES :
     • Zone A (proche entrée) : Produits fréquents
     • Zone B-C : Produits moyens
     • Zone D-E (loin) : Produits rares

     INVESTISSEMENTS RECOMMANDÉS :
     • +1 Robot haute vitesse
     • Système d'étagères dynamiques
     • Capteurs d'inventaire temps réel


🎯 3. WORKFLOW RECOMMANDÉ
═════════════════════════════════════════════════════════════════════════════════

SCÉNARIO : Vous arrivez pour la première fois

  ÉTAPE 1 : Accueil (5 min)
  ├─ Lire la vue d'ensemble
  ├─ Comprendre l'entrepôt
  └─ Identifier les zones

  ÉTAPE 2 : Allocation (10 min)
  ├─ Cliquer "Lancer l'allocation"
  ├─ Observer la distribution
  └─ Vérifier capacités respectées

  ÉTAPE 3 : Simulation (10 min)
  ├─ Optimiser les routes
  ├─ Examiner chaque agent
  └─ Comparer distances

  ÉTAPE 4 : Statistiques (10 min)
  ├─ Analyser Jour 3
  ├─ Analyser Jour 4
  └─ Identifier les anomalies

  ÉTAPE 5 : Recommandations (5 min)
  ├─ Lire les suggestions
  ├─ Comprendre l'optimisation
  └─ Proposer améliorations

  ⏱️ TOTAL : ~40 minutes pour compréhension complète


📊 4. INTERPRÉTATION DES RÉSULTATS
═════════════════════════════════════════════════════════════════════════════════

MÉTRIQUES CLÉS
─────────────────────────────────────────────────────────────────────────────

1) DISTANCE TOTALE
   Qu'est-ce que c'est ? Somme des distances parcourues (en mètres)
   Bon score : < 150m
   Mauvais score : > 300m
   Objectif : Minimiser
   
   Exemple :
   ✅ 145m (très bon)
   ⚠️ 250m (acceptable)
   ❌ 400m (à améliorer)

2) TEMPS TOTAL
   Qu'est-ce que c'est ? Temps complet d'exécution (en minutes)
   Bon score : < 30 min
   Mauvais score : > 60 min
   Objectif : Minimiser
   
   Calcul : Distance / Vitesse + Temps picking
   Exemple : 145m / 2m/s = 72.5s par agent

3) ÉQUILIBRE DE CHARGE
   Qu'est-ce que c'est ? Répartition uniforme des commandes
   Bon score : Écart-type < 1.0
   Mauvais score : Écart-type > 2.0
   Objectif : Minimiser écart-type
   
   Exemple :
   Charge moyenne : 3.5 commandes
   ✅ Écart-type 0.5 (bon équilibre)
   ❌ Écart-type 1.8 (déséquilibre)

4) UTILISATION DES ROBOTS
   Qu'est-ce que c'est ? % de commandes gérées par robots
   Bon score : > 80% (robots = moins cher)
   Objectif : Maximiser

5) RESPECT DES CONTRAINTES
   Qu'est-ce que c'est ? Toutes les règles respectées ?
   Bon score : 100% (aucune violation)
   Mauvais score : < 100%
   Objectif : 100% obligatoire


TABLEAU DE BORD IDÉAL
─────────────────────────────────────────────────────────────────────────────

Métrique              │ Jour 1  │ Jour 2  │ Jour 3  │ Jour 4  │ Jour 5
──────────────────────┼─────────┼─────────┼─────────┼─────────┼──────
Distance (m)         │ 450     │ 430     │ 380     │ 350     │ 320
Temps (min)          │ 240     │ 225     │ 195     │ 175     │ 160
Écart-type           │ 1.2     │ 0.8     │ 0.7     │ 0.5     │ 0.4
% Robots             │ 70%     │ 75%     │ 78%     │ 82%     │ 85%
Contraintes OK       │ ✓       │ ✓       │ ✓       │ ✓       │ ✓


🔧 5. DÉPANNAGE
═════════════════════════════════════════════════════════════════════════════════

PROBLÈME : L'application ne se lance pas

Solution 1 : Vérifier Python
  > python --version
  Résultat attendu : Python 3.8 ou supérieur

Solution 2 : Vérifier Streamlit
  > streamlit --version
  Si erreur : pip install streamlit

Solution 3 : Vérifier les fichiers JSON
  - Allez dans data/
  - Vérifiez : warehouse.json, products.json, agents.json, orders.json
  - S'ils manquent, reportez-vous à utils.py

PROBLÈME : "ModuleNotFoundError: No module named 'streamlit'"

Solution :
  > pip install -r requirements_streamlit.txt
  > pip install streamlit

PROBLÈME : "FileNotFoundError: data/warehouse.json"

Solution :
  1. Vérifiez que vous lancez depuis le bon répertoire
  2. Ouvrez app_streamlit.py et vérifiez le chemin JSON
  3. Adaptez si nécessaire

PROBLÈME : Les graphiques ne s'affichent pas

Solution :
  1. Rafraîchissez la page (F5)
  2. Cliquez à nouveau sur le bouton d'analyse
  3. Redémarrez l'application

PROBLÈME : L'allocation échoue

Solution :
  1. Vérifiez qu'il y a des commandes
  2. Vérifiez les fichiers JSON valides
  3. Consultez la console pour le message d'erreur

PROBLÈME : Les routes n'apparaissent pas

Solution :
  1. Faites d'abord une allocation
  2. Cliquez ensuite sur "Optimiser les routes"
  3. Sélectionnez un agent dans le dropdown


🎨 6. PERSONNALISATION
═════════════════════════════════════════════════════════════════════════════════

CHANGER LES COULEURS DES ZONES
─────────────────────────────────────────────────────────────────────────────

Fichier : app_streamlit.py, ligne ~130

Avant :
  zone_colors = {
      'A': '#FF6B6B',      # Rouge
      'B': '#4ECDC4',      # Turquoise
      ...
  }

Après (exemple) :
  zone_colors = {
      'A': '#00FF00',      # Vert
      'B': '#FF00FF',      # Magenta
      ...
  }


MODIFIER LES DIMENSIONS DE L'ENTREPÔT
─────────────────────────────────────────────────────────────────────────────

Fichier : data/warehouse.json

Avant :
  "dimensions": {"width": 10, "height": 8}

Après (exemple) :
  "dimensions": {"width": 15, "height": 12}


AJOUTER DES AGENTS
─────────────────────────────────────────────────────────────────────────────

Fichier : data/agents.json

Ajouter :
  {
    "id": "R4",
    "type": "robot",
    "capacity_weight": 20,
    "capacity_volume": 30,
    "speed": 2.0,
    "cost_per_hour": 5,
    "restrictions": {...}
  }


🎓 CONSEILS PÉDAGOGIQUES
═════════════════════════════════════════════════════════════════════════════════

Pour les étudiants :

1. Comprenez d'abord les concepts :
   - Distance de Manhattan : |x₁-x₂| + |y₁-y₂|
   - TSP : Problème du voyageur de commerce
   - Contraintes : Capacité, incompatibilités, restrictions

2. Expérimentez :
   - Modifiez les données JSON
   - Observez l'impact sur l'allocation
   - Comparez les performances

3. Analysez :
   - Pourquoi cette allocation ?
   - Comment améliorer la route ?
   - Quel agent est le plus efficace ?

4. Documentez :
   - Prenez des screenshots
   - Notez les résultats
   - Justifiez les décisions


📞 SUPPORT
═════════════════════════════════════════════════════════════════════════════════

Documentation complète : README_STREAMLIT.md
Code source : app_streamlit.py, suite.py
Données : data/*.json

Besoin d'aide ? Consultez les docstrings dans le code !


═════════════════════════════════════════════════════════════════════════════════
Dernière mise à jour : Février 2026
OPTIPICK - Interface Streamlit Interactive
═════════════════════════════════════════════════════════════════════════════════
"""
