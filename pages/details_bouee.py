import streamlit as st
import pandas as pd
import numpy as np
import datetime

# 1. Données des bouées
bouees = {
    'MAREL - Entrée de la rade de Brest': {'lat': 48.35796, 'lon': -4.55175, 'id': 1},
    'SMART - Fond de la rade de Brest': {'lat': 48.318, 'lon': -4.336, 'id': 2},
    'ASTAN - Roscoff': {'lat': 48.7777, 'lon': -3.9375, 'id': 3},
    'SMILE - Luc-Sur-Mer': {'lat': 49.3438, 'lon': -0.3074, 'id': 4},
    'SCENES - Baie de Seine': {'lat': 49.481, 'lon': 0.032, 'id': 5},
    'MAREL - CARNOT - Boulogne-Sur-Mer': {'lat': 50.7405, 'lon': 1.5677, 'id': 6},
    'MOLIT - Baie de Vilaine': {'lat': 47.4600, 'lon': -2.6567, 'id': 7},
    'FERRET - Arcachon Ferret': {'lat': 44.6330, 'lon': -1.2330, 'id': 8},
    'SOLA - Banyuls-Sur-Mer': {'lat': 42.48333, 'lon': 3.13333, 'id': 9},
    'POEM - Perpignan': {'lat': 42.70416, 'lon': 3.06724, 'id': 10},
    'BESSète - Sète': {'lat': 43.33416, 'lon': 3.64389, 'id': 11},
    'MESURHO - Estuaire du Rhône': {'lat': 43.3189, 'lon': 4.8662, 'id': 12},
    'SOLEMIO - Marseille': {'lat': 43.23877, 'lon': 5.28526, 'id': 13},
    'EOL - Villefranche-Sur-Mer': {'lat': 43.683, 'lon': 7.317, 'id': 14},
    }

# 2. Configuration de la page
def page_details():
    # 2.1 Configuration de la mise en page
    st.set_page_config(layout="wide")

    # 2.2 Récupérer la bouée sélectionnée 
    if "bouee_selectionnee" not in st.session_state or not st.session_state.bouee_selectionnee:
        st.warning("Aucune bouée sélectionnée")
        if st.button("← Retour à l'accueil"):
            st.switch_page("accueil.py")
    bouee_selectionnee = st.session_state.bouee_selectionnee

    # 2.3 Création de deux colonnes principales
    col_menu, col_principal = st.columns([1, 3])
    
    # 2.4 Colonne de gauche (menu)
    with col_menu:
        #2.4.1 Titre
        st.sidebar.title("Navigation")               

        #2.4.2Sélecteur de bouée      
        # Ajout d'une option "Sélectionner une bouée" par défaut
        options = ["Sélectionner une bouée..."] + list(bouees.keys())
        
        # Si une bouée est sélectionnée via l'URL, la présélectionner
        default_index = options.index(bouee_selectionnee) if bouee_selectionnee in options else 0
        
        # Donner un ID spécifique au selectbox
        selected_bouee = st.sidebar.selectbox(
            "Sélectionner une bouée:", 
            options,
            index=default_index,
            key="bouee_selector"
        )
        if selected_bouee != default_index:
            bouee_selectionnee = selected_bouee
        
        # 2.4.2 Bouton retour accueil
        if st.sidebar.button("← Retour à l'accueil"):
            st.switch_page("accueil.py")

        # 2.4.3 Informations sur la bouée
        st.sidebar.subheader("Informations")
        st.sidebar.write(f"""
          **Position:** {bouees[bouee_selectionnee]['lat']}°N, {bouees[bouee_selectionnee]['lon']}°E
             
         [Plus d'informations sur Coast-HF](https://coast-hf.fr)
        """)
        
        # 2.4.4 Formulaire de sélection des données
        with st.sidebar.form("selection_donnees"):
            st.subheader("Sélection des données")
            
            parametres = st.multiselect(
                "Paramètres à afficher",
                ["Température", "Salinité", "Turbidité", "Fluorescence", "Hauteur d'eau"],
                default=["Température", "Salinité"]
            )
            
            periode = st.selectbox(
                "Période",
                ["Dernières 24h", "Semaine dernière", "Mois dernier", "Année dernière"]
            )
            
            if st.form_submit_button("Actualiser"):
                st.rerun()

    # 2.5 Colonne principale (dashboard)
    with col_principal:
        st.title("En bref pour :")
        st.title(f"{bouee_selectionnee}")
     
        # Métriques principales
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Température (veille)", "17.5 °C", "0.2 °C")
        with col2:
            st.metric("Salinité (veille)", "35.2 PSU", "-0.1 PSU")
            
        # Graphique température 15 derniers jours
        st.subheader("Évolution de la température (15 derniers jours)")
        # Données fictives pour l'exemple
        dates = pd.date_range(end=datetime.datetime.now(), periods=15, freq='D')
        temp_data = pd.DataFrame({
            'Date': dates,
            'Température': np.random.normal(18, 0.5, 15)
        }).set_index('Date')
        st.line_chart(temp_data)
            
            # # Espace pour les graphiques supplémentaires selon la sélection
            # if parametres:
            #     st.subheader(f"Données sélectionnées - {periode}")
            #     for param in parametres:
            #         if param not in ["Température", "Salinité"]:  # Évite la duplication
            #             st.subheader(param)
            #             # Exemple de graphique pour chaque paramètre
            #             data = pd.DataFrame({
            #                 'Date': dates,
            #                 param: np.random.normal(10, 2, 15)
            #             }).set_index('Date')
            #             st.line_chart(data)

    
page_details() 