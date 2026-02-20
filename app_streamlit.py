"""
OPTIPICK - Interface Streamlit Interactive
═══════════════════════════════════════════════════════════════════════════════

Application Web pour visualiser :
1. L'allocation des commandes aux agents
2. La simulation des déplacements dans l'entrepôt
3. Les statistiques d'optimisation (Jour 3-5)

Usage :
    streamlit run app_streamlit.py
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from typing import Dict, List, Tuple, Set
import json
import time

# Imports du projet
from src.models import Agent, Order, Product, Warehouse, Location
from src.utils import JSON_to_py, compute_order_totals, manhattan
from src.constraints import (
    check_capacity, check_incompatibilities, check_robot_restrictions, check_no_zones
)
from src.allocation import allocate_first_fit_day2
from src.suite import TSPOptimizer, AllocationOptimizer, StorageOptimizer


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="OPTIPICK - Simulation Entrepôt",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
    <style>
    .header-title {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    .section-title {
        font-size: 2em;
        font-weight: bold;
        color: #2ca02c;
        border-bottom: 2px solid #2ca02c;
        padding: 10px 0;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .success {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
    }
    .warning {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CHARGEMENT DES DONNÉES
# ═══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def load_data():
    """Charge les données JSON du projet."""
    try:
        import json
        import os
        
        # Déterminer le chemin de base
        base_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(base_path, 'data')
        
        # Charger les fichiers JSON
        with open(os.path.join(data_path, 'warehouse.json'), 'r', encoding='utf-8') as f:
            warehouse_data = json.load(f)
        with open(os.path.join(data_path, 'products.json'), 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        with open(os.path.join(data_path, 'agents.json'), 'r', encoding='utf-8') as f:
            agents_data = json.load(f)
        with open(os.path.join(data_path, 'orders.json'), 'r', encoding='utf-8') as f:
            orders_data = json.load(f)
        
        # Passer les données à JSON_to_py
        warehouse, products, agents, orders = JSON_to_py(
            warehouse_data, 
            products_data, 
            agents_data, 
            orders_data
        )
        return warehouse, products, agents, orders
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement des données: {e}")
        return None, None, None, None


# ═══════════════════════════════════════════════════════════════════════════════
# VISUALISATION DE L'ENTREPÔT
# ═══════════════════════════════════════════════════════════════════════════════

def draw_warehouse_grid(warehouse: Warehouse, products: Dict[str, Product],
                        agent_positions: Dict[str, Tuple[int, int]] = None,
                        highlight_locations: Set[Location] = None,
                        title: str = "Plan d'Entrepôt") -> plt.Figure:
    """
    Dessine le plan de l'entrepôt avec les zones et les emplacements.
    
    Args:
        warehouse: L'entrepôt
        products: Dict des produits
        agent_positions: Positions actuelles des agents {agent_id: (x, y)}
        highlight_locations: Emplacements à surligner
        title: Titre du graphique
        
    Returns:
        Figure matplotlib
    """
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Couleurs des zones
    zone_colors = {
        'A': '#FF6B6B',      # Électronique - Rouge
        'B': '#4ECDC4',      # Livres - Turquoise
        'C': '#45B7D1',      # Alimentaire - Bleu
        'D': '#F7DC6F',      # Chimie - Jaune
        'E': '#BB8FCE',      # Textile - Violet
        '0': '#EEEEEE'       # Allée - Gris
    }
    
    # Initialiser grille
    grid = warehouse.grid
    
    # Dessiner la grille
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            cell = grid[y][x]
            color = zone_colors.get(cell, '#FFFFFF')
            
            rect = patches.Rectangle((x-0.5, y-0.5), 1, 1, 
                                    linewidth=1, edgecolor='black', 
                                    facecolor=color, alpha=0.6)
            ax.add_patch(rect)
            
            # Ajouter label de zone
            if cell != '0':
                ax.text(x, y, cell, ha='center', va='center', 
                       fontsize=10, fontweight='bold', color='white')
    
    # Surligner les emplacements des produits si spécifié
    if highlight_locations:
        for loc in highlight_locations:
            circle = plt.Circle((loc.x, loc.y), 0.15, color='red', alpha=0.8, zorder=5)
            ax.add_patch(circle)
    
    # Ajouter les positions des agents
    if agent_positions:
        colors_agents = {
            'R1': 'blue', 'R2': 'darkblue', 'R3': 'lightblue',
            'H1': 'green', 'H2': 'darkgreen',
            'C1': 'orange', 'C2': 'darkorange'
        }
        
        for agent_id, (x, y) in agent_positions.items():
            color = colors_agents.get(agent_id, 'gray')
            marker = '*' if 'R' in agent_id else ('s' if 'H' in agent_id else '^')
            ax.plot(x, y, marker=marker, markersize=15, color=color, 
                   label=agent_id, zorder=10)
    
    # Entrée
    entry_x, entry_y = warehouse.entry_point.x, warehouse.entry_point.y
    ax.plot(entry_x, entry_y, marker='X', markersize=20, color='gold', 
           label='Entrée', zorder=10)
    
    # Configuration des axes
    ax.set_xlim(-1, len(grid[0]))
    ax.set_ylim(-1, len(grid))
    ax.set_aspect('equal')
    ax.invert_yaxis()
    
    ax.set_xlabel('X (colonne)', fontsize=10)
    ax.set_ylabel('Y (ligne)', fontsize=10)
    ax.set_title(title, fontsize=12, fontweight='bold')
    
    # Légende
    ax.legend(loc='upper left', fontsize=8)
    
    # Grille de référence
    ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    return fig


def draw_agent_route(warehouse: Warehouse, route: List[Location], 
                    agent_id: str, title: str = "Route d'agent") -> plt.Figure:
    """
    Dessine la route d'un agent.
    
    Args:
        warehouse: L'entrepôt
        route: Liste des emplacements dans l'ordre
        agent_id: ID de l'agent
        title: Titre
        
    Returns:
        Figure matplotlib
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Grille simple
    grid = warehouse.grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            rect = patches.Rectangle((x-0.5, y-0.5), 1, 1,
                                    linewidth=0.5, edgecolor='gray',
                                    facecolor='white', alpha=0.3)
            ax.add_patch(rect)
    
    # Tracer la route
    if route:
        x_coords = [loc.x for loc in route]
        y_coords = [loc.y for loc in route]
        
        ax.plot(x_coords, y_coords, 'b-', linewidth=2, alpha=0.6, label='Trajet')
        ax.plot(x_coords, y_coords, 'bo', markersize=8, alpha=0.6)
        
        # Numéroter les étapes
        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            ax.text(x + 0.15, y + 0.15, str(i), fontsize=8, 
                   bbox=dict(boxstyle='circle', facecolor='yellow', alpha=0.7))
    
    # Entrée
    entry_x, entry_y = warehouse.entry_point.x, warehouse.entry_point.y
    ax.plot(entry_x, entry_y, marker='X', markersize=20, color='gold', label='Entrée')
    
    ax.set_xlim(-1, len(grid[0]))
    ax.set_ylim(-1, len(grid))
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.set_title(f"{title} - {agent_id}", fontsize=12, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


# ═══════════════════════════════════════════════════════════════════════════════
# INTERFACE UTILISATEUR
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    # En-tête
    st.markdown("<div class='header-title'>📦 OPTIPICK - Simulation Entrepôt</div>",
               unsafe_allow_html=True)
    st.markdown("---")
    
    # Charger les données
    warehouse, products, agents, orders = load_data()
    
    if not all([warehouse, products, agents, orders]):
        st.error("❌ Impossible de charger les données")
        return
    
    # Barre latérale - Navigation
    st.sidebar.markdown("## 🎯 Navigation")
    page = st.sidebar.radio("Choisir une page", [
        "🏠 Accueil",
        "📋 Allocation des commandes",
        "🚀 Simulation des déplacements",
        "📊 Statistiques & Optimisation",
        "🔍 Analyse Jour 5"
    ])
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PAGE 1 : ACCUEIL
    # ═══════════════════════════════════════════════════════════════════════════════
    
    if page == "🏠 Accueil":
        st.markdown("<div class='section-title'>Bienvenue dans OPTIPICK</div>",
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 📦 Entrepôt
            - Dimensions : 10×8
            - 5 zones spécialisées
            - Point d'entrée : (0, 0)
            """)
        
        with col2:
            st.markdown("""
            ### 👥 Agents
            - 3 Robots (rapides)
            - 2 Humains (polyvalents)
            - 2 Chariots (capacité élevée)
            """)
        
        with col3:
            st.markdown("""
            ### 📑 Commandes
            - """ + str(len(orders)) + """ commandes
            - """ + str(len(products)) + """ produits
            - Multiple zones
            """)
        
        st.markdown("---")
        
        # Afficher le plan d'entrepôt
        st.markdown("### Plan d'Entrepôt")
        fig = draw_warehouse_grid(warehouse, products, title="Vue globale de l'entrepôt")
        st.pyplot(fig)
        
        # Légende des zones
        st.markdown("""
        #### Légende des zones
        - 🔴 **Zone A** : Électronique (rapide)
        - 🔵 **Zone B** : Livres/Médias
        - 🟦 **Zone C** : Alimentaire (frigo - humains seulement)
        - 🟨 **Zone D** : Chimie/Hygiène (humains seulement)
        - 🟪 **Zone E** : Textile (réserve)
        """)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PAGE 2 : ALLOCATION DES COMMANDES
    # ═══════════════════════════════════════════════════════════════════════════════
    
    elif page == "📋 Allocation des commandes":
        st.markdown("<div class='section-title'>Allocation des commandes aux agents</div>",
                   unsafe_allow_html=True)
        
        # Bouton pour lancer allocation
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Lancer l'allocation (Jour 2)", key="allocate"):
                st.info("⏳ Allocation en cours...")
                
                # Exécuter l'allocation
                result = allocate_first_fit_day2(
                    orders, agents, products, warehouse
                )
                
                # Extraire les données du AllocationResult
                assignments = result.assignments
                unassigned = result.unassigned
                order_totals = result.order_totals
                
                # Sauvegarder en session
                st.session_state.assignments = assignments
                st.session_state.order_totals = order_totals
                st.success("✅ Allocation réussie!")
        
        # Afficher résultats si disponibles
        if 'assignments' in st.session_state:
            assignments = st.session_state.assignments
            order_totals = st.session_state.order_totals
            
            st.markdown("### 📊 Résultats de l'allocation")
            
            # Tableau d'allocation
            allocation_data = []
            for agent in agents:
                agent_orders = assignments.get(agent.id, [])
                if agent_orders:
                    total_weight = sum(order_totals.get(oid, (0, 0))[0] for oid in agent_orders)
                    total_volume = sum(order_totals.get(oid, (0, 0))[1] for oid in agent_orders)
                    
                    allocation_data.append({
                        'Agent': agent.id,
                        'Commandes': len(agent_orders),
                        'Poids total (kg)': f"{total_weight:.2f}",
                        'Volume total (dm³)': f"{total_volume:.2f}",
                        'Capacité poids': f"{agent.capacity_weight}kg",
                        'Capacité volume': f"{agent.capacity_volume}dm³"
                    })
            
            if allocation_data:
                df = pd.DataFrame(allocation_data)
                st.dataframe(df, use_container_width=True)
            
            # Détails par agent
            st.markdown("### 📝 Détails des commandes")
            selected_agent = st.selectbox("Sélectionner un agent",
                                         [a.id for a in agents if assignments.get(a.id)])
            
            if selected_agent and selected_agent in assignments:
                agent_orders = assignments[selected_agent]
                st.markdown(f"#### Commandes de {selected_agent}")
                
                for order_id in agent_orders:
                    order = next((o for o in orders if o.id == order_id), None)
                    if order:
                        weight, volume = order_totals.get(order_id, (0, 0))
                        
                        with st.expander(f"📦 {order_id} - Poids: {weight:.1f}kg, Volume: {volume:.1f}dm³"):
                            items_data = []
                            for item in order.items:
                                product = item.product
                                if product:
                                    items_data.append({
                                        'Produit': product.name,
                                        'Quantité': item.quantity,
                                        'Poids (kg)': f"{product.weight * item.quantity:.2f}",
                                        'Volume (dm³)': f"{product.volume * item.quantity:.2f}"
                                    })
                            
                            if items_data:
                                df_items = pd.DataFrame(items_data)
                                st.dataframe(df_items, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PAGE 3 : SIMULATION DES DÉPLACEMENTS
    # ═══════════════════════════════════════════════════════════════════════════════
    
    elif page == "🚀 Simulation des déplacements":
        st.markdown("<div class='section-title'>🎬 Simulation en Temps Réel des Agents</div>",
                   unsafe_allow_html=True)
        
        if 'assignments' not in st.session_state:
            st.warning("⚠️ Veuillez d'abord effectuer une allocation (page précédente)")
            return
        
        assignments = st.session_state.assignments
        
        # Vérifier qu'il y a des allocations
        if not any(assignments.values()):
            st.error("❌ Aucune allocation trouvée. Veuillez allouer des commandes d'abord.")
            return
        
        st.markdown("""
        Cette page simule en **temps réel** les mouvements de **tous les agents** simultanément
        dans l'entrepôt. Chaque agent suit son propre itinéraire depuis l'entrée, en visitant
        tous les emplacements de ses commandes.
        """)
        
        st.markdown("---")
        
        # Initialiser état simulation
        if 'sim_running' not in st.session_state:
            st.session_state.sim_running = False
        
        # Contrôles
        col_btn, col_params = st.columns([1, 3])
        
        with col_btn:
            if st.button("🎬 Lancer Simulation", key="launch_sim_btn", use_container_width=True):
                st.session_state.sim_running = True
                st.rerun()
        
        with col_params:
            col_speed, col_duration, col_frames = st.columns(3)
            with col_speed:
                sim_speed = st.slider("Vitesse", 0.1, 3.0, 1.0, 0.1, key="sim_speed")
            with col_duration:
                duration = st.slider("Durée (s)", 5, 60, 15, key="sim_duration")
            with col_frames:
                nb_frames = st.slider("Frames", 10, 100, 30, key="sim_frames")
        
        # Lancer la simulation si demandé
        if st.session_state.sim_running:
            st.info("🔄 Simulation en cours...")
            simulate_agent_movements(warehouse, products, assignments, orders, agents, 
                                    nb_frames=nb_frames, sim_speed=sim_speed)
            st.session_state.sim_running = False
        
        st.markdown("---")
        st.markdown("### 📊 Informations sur l'Allocation")
        
        # Résumé de l'allocation
        col1, col2, col3, col4 = st.columns(4)
        
        total_orders = sum(len(order_list) for order_list in assignments.values())
        assigned_agents = sum(1 for order_list in assignments.values() if order_list)

        
        with col1:
            st.metric("Total commandes allouées", total_orders)
        with col2:
            st.metric("Agents utilisés", assigned_agents)
        with col3:
            st.metric("Agents disponibles", len(agents))
        with col4:
            utilization = (assigned_agents / len(agents) * 100) if agents else 0
            st.metric("Taux d'utilisation", f"{utilization:.1f}%")
        
        st.markdown("---")
        st.markdown("### 👥 Distribution par Agent")
        
        # Tableau de distribution
        agent_data = []
        for agent in agents:
            agent_id = agent.id
            orders_assigned = len(assignments.get(agent_id, []))
            agent_type = agent.type
            
            agent_data.append({
                'Agent': agent_id,
                'Type': agent_type.upper(),
                'Commandes': orders_assigned,
                'Capacité Poids': f"{agent.capacity_weight}kg",
                'Capacité Volume': f"{agent.capacity_volume}dm³",
                'Vitesse': f"{agent.speed}m/h"
            })
        
        df_agents = pd.DataFrame(agent_data)
        st.dataframe(df_agents, use_container_width=True)
        
        # Graphique de distribution
        fig, ax = plt.subplots(figsize=(12, 5))
        
        agent_ids = [a['Agent'] for a in agent_data]
        orders_counts = [a['Commandes'] for a in agent_data]
        colors = ['#FF6B6B' if 'R' in aid else '#4ECDC4' if 'C' in aid else '#96CEB4' 
                 for aid in agent_ids]
        
        ax.bar(agent_ids, orders_counts, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax.set_xlabel("Agent", fontsize=12, fontweight='bold')
        ax.set_ylabel("Nombre de commandes", fontsize=12, fontweight='bold')
        ax.set_title("📊 Distribution des Commandes par Agent", fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for i, (agent, count) in enumerate(zip(agent_ids, orders_counts)):
            ax.text(i, count + 0.1, str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PAGE 4 : STATISTIQUES & OPTIMISATION
    # ═══════════════════════════════════════════════════════════════════════════════
    
    elif page == "📊 Statistiques & Optimisation":
        st.markdown("<div class='section-title'>Statistiques et métriques d'optimisation</div>",
                   unsafe_allow_html=True)
        
        if 'assignments' not in st.session_state:
            st.warning("⚠️ Veuillez d'abord effectuer une allocation")
            return
        
        assignments = st.session_state.assignments
        order_totals = st.session_state.order_totals
        
        # JOUR 3 : TSP
        st.markdown("### 📍 JOUR 3 - Optimisation des tournées (TSP)")
        
        if st.button("🔄 Analyser Jour 3", key="day3"):
            optimizer = TSPOptimizer(warehouse)
            locations_per_agent = optimizer.extract_locations(assignments, orders, products)
            
            routes = {}
            for agent in agents:
                if agent.id not in assignments or not assignments[agent.id]:
                    continue
                
                locations = list(locations_per_agent.get(agent.id, set()))
                if not locations:
                    continue
                
                route, distance, time_min = optimizer.optimize_agent_route(agent, locations)
                routes[agent.id] = {'distance': distance, 'time_minutes': time_min}
            
            st.session_state.day3_results = routes
        
        if 'day3_results' in st.session_state:
            routes = st.session_state.day3_results
            
            # Graphique distances
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
            
            agents_list = list(routes.keys())
            distances = [routes[a]['distance'] for a in agents_list]
            times = [routes[a]['time_minutes'] for a in agents_list]
            
            ax1.bar(agents_list, distances, color='steelblue', alpha=0.7)
            ax1.set_title("Distance par agent")
            ax1.set_ylabel("Distance (m)")
            ax1.grid(axis='y', alpha=0.3)
            
            ax2.bar(agents_list, times, color='coral', alpha=0.7)
            ax2.set_title("Temps de tournée par agent")
            ax2.set_ylabel("Temps (minutes)")
            ax2.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
        
        # JOUR 4 : Allocation optimale
        st.markdown("---")
        st.markdown("### ⚖️ JOUR 4 - Allocation optimale et regroupement")
        
        if st.button("🔄 Analyser Jour 4", key="day4"):
            opt = AllocationOptimizer()
            
            # Charge par agent
            agent_loads = {}
            for agent in agents:
                if agent.id in assignments:
                    agent_loads[agent.id] = len(assignments[agent.id])
            
            avg_load = np.mean(list(agent_loads.values())) if agent_loads else 0
            std_load = np.std(list(agent_loads.values())) if agent_loads else 0
            
            st.session_state.day4_results = {
                'loads': agent_loads,
                'avg': avg_load,
                'std': std_load
            }
        
        if 'day4_results' in st.session_state:
            day4 = st.session_state.day4_results
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Charge moyenne", f"{day4['avg']:.1f} commandes")
            with col2:
                st.metric("Écart-type", f"{day4['std']:.2f}")
            
            # Graphique charge
            fig, ax = plt.subplots(figsize=(10, 5))
            agents_list = list(day4['loads'].keys())
            loads = [day4['loads'][a] for a in agents_list]
            
            bars = ax.bar(agents_list, loads, color='mediumseagreen', alpha=0.7)
            ax.axhline(y=day4['avg'], color='red', linestyle='--', label=f"Moyenne: {day4['avg']:.1f}")
            ax.set_title("Répartition de charge par agent")
            ax.set_ylabel("Nombre de commandes")
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            
            st.pyplot(fig)
    
    # ═══════════════════════════════════════════════════════════════════════════════
    # PAGE 5 : ANALYSE JOUR 5
    # ═══════════════════════════════════════════════════════════════════════════════
    
    elif page == "🔍 Analyse Jour 5":
        st.markdown("<div class='section-title'>JOUR 5 - Optimisation du stockage</div>",
                   unsafe_allow_html=True)
        
        if st.button("🔄 Analyser le stockage", key="day5"):
            optimizer = StorageOptimizer()
            
            # Fréquence
            frequency = optimizer.compute_product_frequency(orders)
            
            # Affinité
            affinity = optimizer.compute_product_affinity(orders)
            
            # Réorganisation
            reorg = optimizer.suggest_storage_reorganization(products, orders)
            
            st.session_state.day5_results = {
                'frequency': frequency,
                'affinity': affinity,
                'reorganization': reorg
            }
        
        if 'day5_results' in st.session_state:
            day5 = st.session_state.day5_results
            
            # Produits fréquents
            st.markdown("### 📊 Fréquence des produits")
            
            top_products = sorted(day5['frequency'].items(), 
                                 key=lambda x: x[1], reverse=True)[:10]
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            prod_names = []
            prod_freq = []
            for pid, freq in top_products:
                product = products.get(pid)
                if product:
                    prod_names.append(product.name[:20])
                    prod_freq.append(freq)
            
            ax.barh(prod_names, prod_freq, color='royalblue', alpha=0.7)
            ax.set_xlabel("Nombre de fois commandé")
            ax.set_title("Top 10 produits les plus commandés")
            ax.invert_yaxis()
            
            st.pyplot(fig)
            
            # Recommandations
            st.markdown("---")
            st.markdown("### 💡 Recommandations")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("""
                #### 🤖 Stratégie Agents
                - Robots → produits légers
                - Humains → fragiles
                - Chariots → volumes élevés
                """)
            
            with col2:
                st.markdown("""
                #### 🏪 Organisation Zones
                - Zone A : Produits fréquents
                - Zone B-C : Produits moyens
                - Zone D-E : Produits rares
                """)
            
            with col3:
                st.markdown("""
                #### 📈 Investissements
                - +1 Robot rapide
                - Système dynamique
                - Capteurs temps réel
                """)


# ═══════════════════════════════════════════════════════════════════════════════
# SIMULATION EN TEMPS RÉEL DES AGENTS
# ═══════════════════════════════════════════════════════════════════════════════

def simulate_agent_movements(warehouse: Warehouse, products: Dict[str, Product],
                            assignments: Dict[str, List[str]], orders: List[Order],
                            agents: List[Agent], nb_frames: int = 30, sim_speed: float = 1.0) -> None:
    """
    Simule les mouvements de tous les agents en temps réel.
    
    Args:
        warehouse: L'entrepôt
        products: Dictionnaire des produits
        assignments: Allocation {agent_id: [order_ids]}
        orders: Liste des commandes
        agents: Liste des agents
        nb_frames: Nombre de frames pour la simulation
        sim_speed: Multiplicateur de vitesse
    """
    
    # Préparer les données des agents
    agent_dict = {a.id: a for a in agents}
    orders_dict = {o.id: o for o in orders}
    
    # Pour chaque agent, calculer son itinéraire
    agent_routes = {}
    for agent_id, order_ids in assignments.items():
        if not order_ids:
            # Agent sans commandes
            agent_routes[agent_id] = [Location(warehouse.entry_point.x, warehouse.entry_point.y)]
            continue
        
        # Collecter tous les emplacements à visiter
        locations = [Location(warehouse.entry_point.x, warehouse.entry_point.y)]
        for order_id in order_ids:
            order = orders_dict.get(order_id)
            if order:
                for item in order.items:
                    product = item.product
                    if product:
                        locations.append(Location(product.location.x, product.location.y))
        
        # Ajouter retour à l'entrée
        locations.append(Location(warehouse.entry_point.x, warehouse.entry_point.y))
        agent_routes[agent_id] = locations
    
    # Afficher la simulation
    placeholder = st.empty()
    progress_bar = st.progress(0)
    time_display = st.empty()
    
    # Générer les frames
    for frame in range(nb_frames):
        # Calculer la position de chaque agent
        agent_positions = {}
        progress_ratio = frame / nb_frames
        
        for agent_id, route in agent_routes.items():
            if len(route) < 2:
                agent_positions[agent_id] = route[0] if route else Location(0, 0)
                continue
            
            # Calculer la distance totale
            total_distance = 0
            for i in range(len(route) - 1):
                total_distance += manhattan(route[i], route[i + 1])
            
            # Calculer la distance parcourue jusqu'à présent
            distance_traveled = total_distance * progress_ratio
            
            # Trouver la position actuelle sur le trajet
            cumulative = 0
            current_pos = route[0]
            for i in range(len(route) - 1):
                seg_distance = manhattan(route[i], route[i + 1])
                if cumulative + seg_distance >= distance_traveled:
                    # L'agent est dans ce segment
                    progress_in_segment = (distance_traveled - cumulative) / seg_distance if seg_distance > 0 else 0
                    current_pos = Location(
                        int(route[i].x + (route[i + 1].x - route[i].x) * progress_in_segment),
                        int(route[i].y + (route[i + 1].y - route[i].y) * progress_in_segment)
                    )
                    break
                cumulative += seg_distance
            
            agent_positions[agent_id] = current_pos
        
        # Dessiner le graphique
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Grille
        grid_height = warehouse.height
        grid_width = warehouse.width
        grid = np.zeros((grid_height, grid_width))
        
        # Zones - remplir la grille avec les coordonnées des zones
        zone_colors_map = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5
        }
        for zone_id, zone_data in warehouse.zones.items():
            zone_value = zone_colors_map.get(zone_id, 1)
            if isinstance(zone_data, dict) and 'coords' in zone_data:
                for x, y in zone_data['coords']:
                    if 0 <= y < grid_height and 0 <= x < grid_width:
                        grid[y, x] = zone_value
        
        ax.imshow(grid, cmap='Pastel1', alpha=0.5, extent=[0, grid_width, grid_height, 0])
        
        # Produits
        for product in products.values():
            ax.plot(product.location.x, product.location.y, 'o', 
                   color='gray', markersize=8, alpha=0.5)
        
        # Trajet de chaque agent (faint)
        agent_colors = {
            'R1': '#FF6B6B', 'R2': '#FF8E72', 'R3': '#FFA500',
            'C1': '#4ECDC4', 'C2': '#45B7D1',
            'H1': '#96CEB4', 'H2': '#BBDC9E'
        }
        
        for agent_id, route in agent_routes.items():
            color = agent_colors.get(agent_id, '#999999')
            for i in range(len(route) - 1):
                ax.plot([route[i].x, route[i+1].x], 
                       [route[i].y, route[i+1].y],
                       color=color, linewidth=1, alpha=0.3, linestyle='--')
        
        # Positions actuelles des agents
        for agent_id, pos in agent_positions.items():
            agent = agent_dict.get(agent_id)
            marker = 'D' if agent and agent.type == 'robot' else 's' if agent and agent.type == 'cart' else 'P'
            color = agent_colors.get(agent_id, '#999999')
            ax.plot(pos.x, pos.y, marker=marker, markersize=15, color=color,
                   label=agent_id, zorder=10, markeredgecolor='black', markeredgewidth=2)
        
        # Entrée
        ax.plot(warehouse.entry_point.x, warehouse.entry_point.y, marker='X', 
               markersize=20, color='gold', label='Entree', zorder=10, 
               markeredgecolor='black', markeredgewidth=2)
        
        ax.set_xlim(-1, grid_width)
        ax.set_ylim(-1, grid_height)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Simulation Temps Reel - Progression: {progress_ratio*100:.1f}%")
        ax.legend(loc='upper right', fontsize=8, ncol=2)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        with placeholder:
            st.pyplot(fig, use_container_width=True)
        
        # Mise à jour barre de progression
        progress_bar.progress(min(progress_ratio, 1.0))
        
        with time_display:
            st.metric("Progression", f"{progress_ratio*100:.1f}%")
        
        plt.close(fig)
        time.sleep(0.05 / sim_speed)
    
    st.success("Simulation terminee !")


if __name__ == "__main__":
    main()

