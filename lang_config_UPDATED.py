"""
================================================================================
LANGUAGE CONFIGURATION MODULE - WITH LISA TRANSLATIONS
================================================================================

Centralized translation dictionary for bilingual dashboard.
Supports English and French with easy switching.

NEW: Added complete translations for LISA Analysis page

Usage:
    from lang_config import translations, get_text
    
    # Get translated text
    text = get_text('total_cases', language='en')  # Returns "Total Cases"
    text = get_text('total_cases', language='fr')  # Returns "Cas Totaux"

================================================================================
"""

# ============================================================================
# TRANSLATION DICTIONARY
# ============================================================================

translations = {
    # ========================================================================
    # MAIN DASHBOARD
    # ========================================================================
    'dashboard_title': {
        'en': 'Meningitis Surveillance Dashboard',
        'fr': 'Tableau de Bord de Surveillance de la Méningite'
    },
    'dashboard_subtitle': {
        'en': 'DLMEP/MINSANTE - Cameroon Health Districts',
        'fr': 'DLMEP/MINSANTE - Districts Sanitaires du Cameroun'
    },
    'select_language': {
        'en': '🌐 Language',
        'fr': '🌐 Langue'
    },
    'data_loaded': {
        'en': 'Data loaded successfully!',
        'fr': 'Données chargées avec succès!'
    },
    'records_ready': {
        'en': 'records ready for analysis',
        'fr': 'enregistrements prêts pour l\'analyse'
    },
    
    # ========================================================================
    # NAVIGATION
    # ========================================================================
    'quick_overview': {
        'en': 'Quick Overview',
        'fr': 'Aperçu Rapide'
    },
    'dashboard_navigation': {
        'en': 'Dashboard Navigation',
        'fr': 'Navigation du Tableau de Bord'
    },
    'available_pages': {
        'en': 'Available Pages',
        'fr': 'Pages Disponibles'
    },
    'use_sidebar': {
        'en': 'Use the sidebar (← left) to navigate between pages',
        'fr': 'Utilisez la barre latérale (← gauche) pour naviguer entre les pages'
    },
    'system_status': {
        'en': 'System Status',
        'fr': 'État du Système'
    },
    'getting_started': {
        'en': 'Getting Started',
        'fr': 'Démarrage'
    },
    
    # ========================================================================
    # PAGE TITLES
    # ========================================================================
    'overview': {
        'en': 'Overview',
        'fr': 'Aperçu'
    },
    'spatial_analysis': {
        'en': 'Spatial Analysis',
        'fr': 'Analyse Spatiale'
    },
    'temporal_analysis': {
        'en': 'Temporal Analysis',
        'fr': 'Analyse Temporelle'
    },
    'predictions': {
        'en': 'Predictions',
        'fr': 'Prédictions'
    },
    'data_explorer': {
        'en': 'Data Explorer',
        'fr': 'Explorateur de Données'
    },
    'about': {
        'en': 'About',
        'fr': 'À Propos'
    },
    'lisa_analysis': {
        'en': 'LISA Analysis',
        'fr': 'Analyse LISA'
    },
    
    # ========================================================================
    # METRICS & KPIs
    # ========================================================================
    'total_cases': {
        'en': 'Total Cases',
        'fr': 'Cas Totaux'
    },
    'total_deaths': {
        'en': 'Total Deaths',
        'fr': 'Décès Totaux'
    },
    'case_fatality_rate': {
        'en': 'Case Fatality Rate',
        'fr': 'Taux de Létalité'
    },
    'overall_cfr': {
        'en': 'Overall CFR',
        'fr': 'TL Global'
    },
    'health_districts': {
        'en': 'Health Districts',
        'fr': 'Districts Sanitaires'
    },
    'regions': {
        'en': 'Regions',
        'fr': 'Régions'
    },
    'affected_districts': {
        'en': 'Affected Districts',
        'fr': 'Districts Affectés'
    },
    'active_outbreaks': {
        'en': 'Active Outbreaks',
        'fr': 'Épidémies Actives'
    },
    'districts_reporting': {
        'en': 'Districts Reporting',
        'fr': 'Districts Déclarants'
    },
    'incidence_rate': {
        'en': 'Incidence Rate',
        'fr': 'Taux d\'Incidence'
    },
    'attack_rate': {
        'en': 'Attack Rate',
        'fr': 'Taux d\'Attaque'
    },
    'per_100k': {
        'en': 'per 100,000',
        'fr': 'pour 100 000'
    },
    
    # ========================================================================
    # TIME & GEOGRAPHY
    # ========================================================================
    'year': {
        'en': 'Year',
        'fr': 'Année'
    },
    'years': {
        'en': 'Years',
        'fr': 'Années'
    },
    'week': {
        'en': 'Week',
        'fr': 'Semaine'
    },
    'week_number': {
        'en': 'Week Number',
        'fr': 'Numéro de Semaine'
    },
    'month': {
        'en': 'Month',
        'fr': 'Mois'
    },
    'quarter': {
        'en': 'Quarter',
        'fr': 'Trimestre'
    },
    'date_range': {
        'en': 'Date Range',
        'fr': 'Plage de Dates'
    },
    'time_period': {
        'en': 'Time Period',
        'fr': 'Période'
    },
    'region': {
        'en': 'Region',
        'fr': 'Région'
    },
    'district': {
        'en': 'District',
        'fr': 'District'
    },
    'population': {
        'en': 'Population',
        'fr': 'Population'
    },
    
    # ========================================================================
    # ANALYSIS TERMS
    # ========================================================================
    'temporal_trends': {
        'en': 'Temporal Trends',
        'fr': 'Tendances Temporelles'
    },
    'seasonal_pattern': {
        'en': 'Seasonal Pattern',
        'fr': 'Schéma Saisonnier'
    },
    'geographic_distribution': {
        'en': 'Geographic Distribution',
        'fr': 'Distribution Géographique'
    },
    'regional_distribution': {
        'en': 'Regional Distribution',
        'fr': 'Distribution Régionale'
    },
    'top_districts': {
        'en': 'Top Districts',
        'fr': 'Principaux Districts'
    },
    'high_risk_districts': {
        'en': 'High-Risk Districts',
        'fr': 'Districts à Haut Risque'
    },
    'hotspots': {
        'en': 'Hotspots',
        'fr': 'Points Chauds'
    },
    'outbreak_pattern': {
        'en': 'Outbreak Pattern',
        'fr': 'Schéma d\'Épidémie'
    },
    
    # ========================================================================
    # LISA ANALYSIS - NEW TRANSLATIONS
    # ========================================================================
    'lisa_title': {
        'en': 'LISA Cluster Analysis - Spatial Hotspot Detection',
        'fr': 'Analyse LISA - Détection des Points Chauds Spatiaux'
    },
    'lisa_description': {
        'en': 'Local Indicators of Spatial Association (LISA) identifies statistically significant spatial clusters of meningitis cases.',
        'fr': 'Les Indicateurs Locaux d\'Association Spatiale (LISA) identifient les grappes spatiales statistiquement significatives de cas de méningite.'
    },
    'lisa_helps_identify': {
        'en': 'This analysis helps identify:',
        'fr': 'Cette analyse aide à identifier:'
    },
    'lisa_hotspots_desc': {
        'en': 'Hotspots (High-High): Areas with high cases surrounded by high-case neighbors',
        'fr': 'Points Chauds (Élevé-Élevé): Zones avec cas élevés entourées de voisins à cas élevés'
    },
    'lisa_coldspots_desc': {
        'en': 'Coldspots (Low-Low): Areas with low cases surrounded by low-case neighbors',
        'fr': 'Points Froids (Faible-Faible): Zones avec cas faibles entourées de voisins à cas faibles'
    },
    'lisa_outliers_desc': {
        'en': 'Outliers: Areas with values different from their neighbors',
        'fr': 'Valeurs Aberrantes: Zones avec des valeurs différentes de leurs voisins'
    },
    'lisa_configuration': {
        'en': 'LISA Configuration',
        'fr': 'Configuration LISA'
    },
    'analysis_mode': {
        'en': 'Analysis Mode',
        'fr': 'Mode d\'Analyse'
    },
    'single_year': {
        'en': 'Single Year',
        'fr': 'Année Unique'
    },
    'multi_year_comparison': {
        'en': 'Multi-Year Comparison',
        'fr': 'Comparaison Multi-Années'
    },
    'all_years_grid': {
        'en': 'All Years Grid',
        'fr': 'Grille de Toutes les Années'
    },
    'select_year': {
        'en': 'Select Year',
        'fr': 'Sélectionner l\'Année'
    },
    'select_years_to_compare': {
        'en': 'Select Years to Compare',
        'fr': 'Sélectionner les Années à Comparer'
    },
    'choose_analysis_mode': {
        'en': 'Choose how to visualize LISA clusters',
        'fr': 'Choisir comment visualiser les grappes LISA'
    },
    'choose_single_year': {
        'en': 'Choose a single year to analyze',
        'fr': 'Choisir une année unique à analyser'
    },
    'choose_multiple_years': {
        'en': 'Choose multiple years to compare side-by-side',
        'fr': 'Choisir plusieurs années à comparer côte à côte'
    },
    'significance_level': {
        'en': 'Significance Level (α)',
        'fr': 'Niveau de Signification (α)'
    },
    'pvalue_threshold': {
        'en': 'P-value threshold for statistical significance',
        'fr': 'Seuil de valeur p pour la signification statistique'
    },
    'current_configuration': {
        'en': 'Current Configuration',
        'fr': 'Configuration Actuelle'
    },
    'mode': {
        'en': 'Mode',
        'fr': 'Mode'
    },
    'avg_neighbors': {
        'en': 'Avg neighbors',
        'fr': 'Voisins moy'
    },
    'computing_lisa': {
        'en': 'Computing LISA Clusters...',
        'fr': 'Calcul des Grappes LISA...'
    },
    'processing_year': {
        'en': 'Processing',
        'fr': 'Traitement'
    },
    'successfully_computed': {
        'en': 'Successfully computed LISA for',
        'fr': 'LISA calculé avec succès pour'
    },
    'year_s': {
        'en': 'year(s)',
        'fr': 'année(s)'
    },
    'no_lisa_results': {
        'en': 'No LISA results computed. Check data availability.',
        'fr': 'Aucun résultat LISA calculé. Vérifier la disponibilité des données.'
    },
    'lisa_cluster_maps': {
        'en': 'LISA Cluster Maps',
        'fr': 'Cartes de Grappes LISA'
    },
    'lisa_clusters': {
        'en': 'LISA Clusters',
        'fr': 'Grappes LISA'
    },
    'hotspots_hh': {
        'en': 'Hotspots (HH)',
        'fr': 'Points Chauds (EE)'
    },
    'coldspots_ll': {
        'en': 'Coldspots (LL)',
        'fr': 'Points Froids (FF)'
    },
    'high_low_outliers': {
        'en': 'High-Low Outliers',
        'fr': 'Valeurs Aberrantes Élevé-Faible'
    },
    'low_high_outliers': {
        'en': 'Low-High Outliers',
        'fr': 'Valeurs Aberrantes Faible-Élevé'
    },
    'high_high': {
        'en': 'High-High',
        'fr': 'Élevé-Élevé'
    },
    'low_low': {
        'en': 'Low-Low',
        'fr': 'Faible-Faible'
    },
    'high_low': {
        'en': 'High-Low',
        'fr': 'Élevé-Faible'
    },
    'low_high': {
        'en': 'Low-High',
        'fr': 'Faible-Élevé'
    },
    'not_significant': {
        'en': 'Not Significant',
        'fr': 'Non Significatif'
    },
    'high_cases_high_neighbors': {
        'en': 'High cases surrounded by high cases',
        'fr': 'Cas élevés entourés de cas élevés'
    },
    'low_cases_low_neighbors': {
        'en': 'Low cases surrounded by low cases',
        'fr': 'Cas faibles entourés de cas faibles'
    },
    'high_cases_low_neighbors': {
        'en': 'High cases surrounded by low cases',
        'fr': 'Cas élevés entourés de cas faibles'
    },
    'low_cases_high_neighbors': {
        'en': 'Low cases surrounded by high cases',
        'fr': 'Cas faibles entourés de cas élevés'
    },
    'detailed_analysis': {
        'en': 'Detailed Analysis',
        'fr': 'Analyse Détaillée'
    },
    'all_clusters': {
        'en': 'All Clusters',
        'fr': 'Toutes les Grappes'
    },
    'hotspot_districts_identified': {
        'en': 'hotspot districts identified',
        'fr': 'districts points chauds identifiés'
    },
    'coldspot_districts_identified': {
        'en': 'coldspot districts identified',
        'fr': 'districts points froids identifiés'
    },
    'no_hotspots': {
        'en': 'No significant hotspots identified',
        'fr': 'Aucun point chaud significatif identifié'
    },
    'no_coldspots': {
        'en': 'No significant coldspots identified',
        'fr': 'Aucun point froid significatif identifié'
    },
    'temporal_evolution': {
        'en': 'Temporal Evolution of LISA Clusters',
        'fr': 'Évolution Temporelle des Grappes LISA'
    },
    'number_of_districts': {
        'en': 'Number of Districts',
        'fr': 'Nombre de Districts'
    },
    'analysis_notes': {
        'en': 'Analysis Notes',
        'fr': 'Notes d\'Analyse'
    },
    'add_custom_notes': {
        'en': 'Add Custom Notes',
        'fr': 'Ajouter des Notes Personnalisées'
    },
    'use_this_space': {
        'en': 'Use this space to document your observations, interpretations, and action items from the LISA analysis.',
        'fr': 'Utilisez cet espace pour documenter vos observations, interprétations et actions à entreprendre suite à l\'analyse LISA.'
    },
    'your_notes': {
        'en': 'Your Notes',
        'fr': 'Vos Notes'
    },
    'notes_placeholder': {
        'en': 'Example:\n- Persistent hotspot identified in [District Name] across multiple years\n- Consider enhanced surveillance in neighboring districts\n- Investigate local transmission factors...',
        'fr': 'Exemple:\n- Point chaud persistant identifié dans [Nom du District] sur plusieurs années\n- Envisager une surveillance renforcée dans les districts voisins\n- Enquêter sur les facteurs de transmission locaux...'
    },
    'notes_session_specific': {
        'en': 'These notes are session-specific and won\'t be saved permanently',
        'fr': 'Ces notes sont spécifiques à la session et ne seront pas sauvegardées de façon permanente'
    },
    'interpretation_guide': {
        'en': 'Interpretation Guide',
        'fr': 'Guide d\'Interprétation'
    },
    'cluster_types': {
        'en': 'Cluster Types:',
        'fr': 'Types de Grappes:'
    },
    'outlier_types': {
        'en': 'Outlier Types:',
        'fr': 'Types de Valeurs Aberrantes:'
    },
    'high_high_clusters': {
        'en': 'High-High (Hotspots)',
        'fr': 'Élevé-Élevé (Points Chauds)'
    },
    'low_low_clusters': {
        'en': 'Low-Low (Coldspots)',
        'fr': 'Faible-Faible (Points Froids)'
    },
    'high_cases_high_neighbor_cases': {
        'en': 'High cases + high neighbor cases',
        'fr': 'Cas élevés + cas élevés chez les voisins'
    },
    'low_cases_low_neighbor_cases': {
        'en': 'Low cases + low neighbor cases',
        'fr': 'Cas faibles + cas faibles chez les voisins'
    },
    'indicates_spatial_clustering': {
        'en': 'Indicates spatial clustering',
        'fr': 'Indique un regroupement spatial'
    },
    'indicates_low_burden': {
        'en': 'Indicates low-burden areas',
        'fr': 'Indique des zones à faible charge'
    },
    'action_priority_intervention': {
        'en': 'Action: Priority for intervention',
        'fr': 'Action: Priorité pour intervention'
    },
    'action_maintain_surveillance': {
        'en': 'Action: Maintain surveillance',
        'fr': 'Action: Maintenir la surveillance'
    },
    'high_low_outlier': {
        'en': 'High-Low',
        'fr': 'Élevé-Faible'
    },
    'low_high_outlier': {
        'en': 'Low-High',
        'fr': 'Faible-Élevé'
    },
    'high_cases_but_low_neighbors': {
        'en': 'High cases but low neighbor cases',
        'fr': 'Cas élevés mais voisins à cas faibles'
    },
    'low_cases_but_high_neighbors': {
        'en': 'Low cases but high neighbor cases',
        'fr': 'Cas faibles mais voisins à cas élevés'
    },
    'isolated_outbreak': {
        'en': 'Isolated outbreak or data issue',
        'fr': 'Épidémie isolée ou problème de données'
    },
    'potential_buffer_zone': {
        'en': 'Potential buffer zone',
        'fr': 'Zone tampon potentielle'
    },
    'action_investigate': {
        'en': 'Action: Investigate local factors',
        'fr': 'Action: Enquêter sur les facteurs locaux'
    },
    'action_enhanced_surveillance': {
        'en': 'Action: Enhanced surveillance',
        'fr': 'Action: Surveillance renforcée'
    },
    'statistical_significance_note': {
        'en': 'Statistical Significance: Clusters are identified using permutation-based significance testing. Only clusters with p-value <',
        'fr': 'Signification Statistique: Les grappes sont identifiées par des tests de signification basés sur des permutations. Seules les grappes avec valeur p <'
    },
    'are_classified_significant': {
        'en': 'are classified as significant.',
        'fr': 'sont classées comme significatives.'
    },
    'download_results': {
        'en': 'Download Results',
        'fr': 'Télécharger les Résultats'
    },
    'download_lisa_results': {
        'en': 'Download LISA Results',
        'fr': 'Télécharger les Résultats LISA'
    },
    'download_multi_year_summary': {
        'en': 'Download Multi-Year Summary',
        'fr': 'Télécharger le Résumé Multi-Années'
    },
    'lisa_configuration_footer': {
        'en': 'LISA Configuration:',
        'fr': 'Configuration LISA:'
    },
    'spatial_weights': {
        'en': 'Spatial Weights',
        'fr': 'Poids Spatiaux'
    },
    'queen_contiguity': {
        'en': 'Queen Contiguity',
        'fr': 'Contiguïté de la Reine'
    },
    'average_neighbors': {
        'en': 'Average Neighbors',
        'fr': 'Voisins Moyens'
    },
    'spatial_not_available': {
        'en': 'Spatial analysis libraries not available',
        'fr': 'Bibliothèques d\'analyse spatiale non disponibles'
    },
    'lisa_requires': {
        'en': 'This page requires:',
        'fr': 'Cette page nécessite:'
    },
    'install_with': {
        'en': 'Install with:',
        'fr': 'Installer avec:'
    },
    'failed_load_geojson': {
        'en': 'Failed to load GeoJSON. LISA analysis requires district boundaries.',
        'fr': 'Échec du chargement du GeoJSON. L\'analyse LISA nécessite les limites des districts.'
    },
    'failed_spatial_weights': {
        'en': 'Failed to create spatial weights matrix.',
        'fr': 'Échec de la création de la matrice de poids spatiaux.'
    },
    'loaded_districts': {
        'en': 'Loaded',
        'fr': 'Chargé'
    },
    'districts_with': {
        'en': 'districts with',
        'fr': 'districts avec'
    },
    'average_neighbors_value': {
        'en': 'average neighbors',
        'fr': 'voisins en moyenne'
    },
    'please_select_year': {
        'en': 'Please select at least one year',
        'fr': 'Veuillez sélectionner au moins une année'
    },
    'cases': {
        'en': 'cases',
        'fr': 'cas'
    },
    'deaths': {
        'en': 'deaths',
        'fr': 'décès'
    },
    
    # ========================================================================
    # CHARTS & VISUALIZATIONS
    # ========================================================================
    'annual_cases_deaths': {
        'en': 'Annual Cases and Deaths',
        'fr': 'Cas et Décès Annuels'
    },
    'weekly_average': {
        'en': 'Weekly Average',
        'fr': 'Moyenne Hebdomadaire'
    },
    'cumulative_cases': {
        'en': 'Cumulative Cases',
        'fr': 'Cas Cumulés'
    },
    'distribution': {
        'en': 'Distribution',
        'fr': 'Distribution'
    },
    'comparison': {
        'en': 'Comparison',
        'fr': 'Comparaison'
    },
    'heatmap': {
        'en': 'Heatmap',
        'fr': 'Carte Thermique'
    },
    'map': {
        'en': 'Map',
        'fr': 'Carte'
    },
    'chart': {
        'en': 'Chart',
        'fr': 'Graphique'
    },
    'interactive_maps': {
        'en': 'Interactive Maps',
        'fr': 'Cartes Interactives'
    },
    
    # ========================================================================
    # FILTERS & CONTROLS
    # ========================================================================
    'filters': {
        'en': 'Filters',
        'fr': 'Filtres'
    },
    'advanced_filters': {
        'en': 'Advanced Filters',
        'fr': 'Filtres Avancés'
    },
    'select': {
        'en': 'Select',
        'fr': 'Sélectionner'
    },
    'filter_by': {
        'en': 'Filter by',
        'fr': 'Filtrer par'
    },
    'show': {
        'en': 'Show',
        'fr': 'Afficher'
    },
    'hide': {
        'en': 'Hide',
        'fr': 'Masquer'
    },
    'apply': {
        'en': 'Apply',
        'fr': 'Appliquer'
    },
    'reset': {
        'en': 'Reset',
        'fr': 'Réinitialiser'
    },
    'clear': {
        'en': 'Clear',
        'fr': 'Effacer'
    },
    
    # ========================================================================
    # DATA OPERATIONS
    # ========================================================================
    'loading_data': {
        'en': 'Loading data...',
        'fr': 'Chargement des données...'
    },
    'loading': {
        'en': 'Loading',
        'fr': 'Chargement'
    },
    'download': {
        'en': 'Download',
        'fr': 'Télécharger'
    },
    'export': {
        'en': 'Export',
        'fr': 'Exporter'
    },
    'download_data': {
        'en': 'Download Data',
        'fr': 'Télécharger les Données'
    },
    'download_filtered_data': {
        'en': 'Download Filtered Data (CSV)',
        'fr': 'Télécharger les Données Filtrées (CSV)'
    },
    'download_summary_stats': {
        'en': 'Download Summary Statistics (CSV)',
        'fr': 'Télécharger les Statistiques Récapitulatives (CSV)'
    },
    
    # ========================================================================
    # MESSAGES
    # ========================================================================
    'failed_load_data': {
        'en': 'Failed to load data',
        'fr': 'Échec du chargement des données'
    },
    'error_loading_data': {
        'en': 'Error loading data',
        'fr': 'Erreur de chargement des données'
    },
    'no_data_available': {
        'en': 'No data available',
        'fr': 'Aucune donnée disponible'
    },
    'please_select': {
        'en': 'Please select',
        'fr': 'Veuillez sélectionner'
    },
    'no_records_found': {
        'en': 'No records found',
        'fr': 'Aucun enregistrement trouvé'
    },
    
    # ========================================================================
    # TABLES & LISTS
    # ========================================================================
    'table': {
        'en': 'Table',
        'fr': 'Tableau'
    },
    'data_table': {
        'en': 'Data Table',
        'fr': 'Tableau de Données'
    },
    'records': {
        'en': 'Records',
        'fr': 'Enregistrements'
    },
    'total_records': {
        'en': 'Total Records',
        'fr': 'Enregistrements Totaux'
    },
    'filtered_records': {
        'en': 'Filtered Records',
        'fr': 'Enregistrements Filtrés'
    },
    'displaying': {
        'en': 'Displaying',
        'fr': 'Affichage'
    },
    'columns': {
        'en': 'Columns',
        'fr': 'Colonnes'
    },
    'rows': {
        'en': 'Rows',
        'fr': 'Lignes'
    },
    'select_columns': {
        'en': 'Select columns to display',
        'fr': 'Sélectionner les colonnes à afficher'
    },
    'max_rows': {
        'en': 'Maximum rows to display',
        'fr': 'Nombre maximum de lignes à afficher'
    },
    
    # ========================================================================
    # STATISTICS
    # ========================================================================
    'statistics': {
        'en': 'Statistics',
        'fr': 'Statistiques'
    },
    'quick_statistics': {
        'en': 'Quick Statistics',
        'fr': 'Statistiques Rapides'
    },
    'summary_statistics': {
        'en': 'Summary Statistics',
        'fr': 'Statistiques Récapitulatives'
    },
    'mean': {
        'en': 'Mean',
        'fr': 'Moyenne'
    },
    'median': {
        'en': 'Median',
        'fr': 'Médiane'
    },
    'std_dev': {
        'en': 'Std Dev',
        'fr': 'Écart Type'
    },
    'min': {
        'en': 'Min',
        'fr': 'Min'
    },
    'max': {
        'en': 'Max',
        'fr': 'Max'
    },
    'sum': {
        'en': 'Sum',
        'fr': 'Somme'
    },
    'count': {
        'en': 'Count',
        'fr': 'Nombre'
    },
    'total': {
        'en': 'Total',
        'fr': 'Total'
    },
    
    # ========================================================================
    # PREDICTIONS
    # ========================================================================
    'forecast': {
        'en': 'Forecast',
        'fr': 'Prévision'
    },
    'prediction': {
        'en': 'Prediction',
        'fr': 'Prédiction'
    },
    'outbreak_detection': {
        'en': 'Outbreak Detection',
        'fr': 'Détection d\'Épidémie'
    },
    'risk_classification': {
        'en': 'Risk Classification',
        'fr': 'Classification des Risques'
    },
    'risk_level': {
        'en': 'Risk Level',
        'fr': 'Niveau de Risque'
    },
    'high_risk': {
        'en': 'High Risk',
        'fr': 'Risque Élevé'
    },
    'low_risk': {
        'en': 'Low Risk',
        'fr': 'Risque Faible'
    },
    'moderate_risk': {
        'en': 'Moderate Risk',
        'fr': 'Risque Modéré'
    },
    'critical_risk': {
        'en': 'Critical Risk',
        'fr': 'Risque Critique'
    },
    'statistical_mode': {
        'en': 'Statistical Prediction Mode',
        'fr': 'Mode de Prévision Statistique'
    },
    
    # ========================================================================
    # DOCUMENTATION
    # ========================================================================
    'methodology': {
        'en': 'Methodology',
        'fr': 'Méthodologie'
    },
    'data_sources': {
        'en': 'Data Sources',
        'fr': 'Sources de Données'
    },
    'technical_specs': {
        'en': 'Technical Specifications',
        'fr': 'Spécifications Techniques'
    },
    'limitations': {
        'en': 'Limitations',
        'fr': 'Limites'
    },
    'references': {
        'en': 'References',
        'fr': 'Références'
    },
    'contact': {
        'en': 'Contact',
        'fr': 'Contact'
    },
    'feedback': {
        'en': 'Feedback',
        'fr': 'Retour d\'Information'
    },
    'version_history': {
        'en': 'Version History',
        'fr': 'Historique des Versions'
    },
    'project_overview': {
        'en': 'Project Overview',
        'fr': 'Aperçu du Projet'
    },
    
    # ========================================================================
    # SPATIAL ANALYSIS - ADDITIONAL TRANSLATIONS
    # ========================================================================
    'metric': {
        'en': 'Metric',
        'fr': 'Métrique'
    },
    'ranking': {
        'en': 'Ranking',
        'fr': 'Classement'
    },
    'rank': {
        'en': 'Rank',
        'fr': 'Rang'
    },
    'highest_burden': {
        'en': 'Highest Burden District',
        'fr': 'District le Plus Affecté'
    },
    'highest': {
        'en': 'Highest',
        'fr': 'Le Plus Élevé'
    },
    'insights': {
        'en': 'Insights',
        'fr': 'Aperçus'
    },
    'display': {
        'en': 'Display',
        'fr': 'Affichage'
    },
    
    # ========================================================================
    # TEMPORAL ANALYSIS - ADDITIONAL TRANSLATIONS
    # ========================================================================
    'threshold': {
        'en': 'Threshold',
        'fr': 'Seuil'
    },
    'peak': {
        'en': 'Peak',
        'fr': 'Pic'
    },
    'lowest': {
        'en': 'Lowest',
        'fr': 'Le Plus Bas'
    },
    'increasing': {
        'en': 'Increasing',
        'fr': 'Croissant'
    },
    'stable': {
        'en': 'Stable',
        'fr': 'Stable'
    },
    'change': {
        'en': 'Change',
        'fr': 'Changement'
    },
    'status': {
        'en': 'Status',
        'fr': 'Statut'
    },
    
    # ========================================================================
    # PREDICTIONS PAGE - ADDITIONAL TRANSLATIONS
    # ========================================================================
    'predictions_forecasting': {
        'en': 'Outbreak Predictions & Forecasting',
        'fr': 'Prédictions et Prévisions d\'Épidémies'
    },
    'prediction_settings': {
        'en': 'Prediction Settings',
        'fr': 'Paramètres de Prédiction'
    },
    'current_period': {
        'en': 'Current Period',
        'fr': 'Période Actuelle'
    },
    'forecast_horizon': {
        'en': 'Forecast Horizon',
        'fr': 'Horizon de Prévision'
    },
    'weeks_ahead': {
        'en': 'weeks ahead',
        'fr': 'semaines à l\'avance'
    },
    'filter_by_regions': {
        'en': 'Filter by Regions',
        'fr': 'Filtrer par Régions'
    },
    'district_level_predictions': {
        'en': 'District-Level Predictions',
        'fr': 'Prédictions par District'
    },
    'generating_predictions': {
        'en': 'Generating predictions...',
        'fr': 'Génération des prédictions...'
    },
    'predicted_cases': {
        'en': 'Predicted Cases',
        'fr': 'Cas Prédits'
    },
    'next_weeks': {
        'en': 'Next {n} Weeks',
        'fr': 'Prochaines {n} Semaines'
    },
    'sort_by': {
        'en': 'Sort by',
        'fr': 'Trier par'
    },
    'model_performance': {
        'en': 'Model Performance',
        'fr': 'Performance du Modèle'
    },
    'feature_importance': {
        'en': 'Feature Importance',
        'fr': 'Importance des Caractéristiques'
    },
    'early_warning': {
        'en': 'Early Warning',
        'fr': 'Alerte Précoce'
    },
    'statistical_mode': {
        'en': 'Statistical Prediction Mode',
        'fr': 'Mode de Prévision Statistique'
    },
    'ml_models_loaded': {
        'en': 'ML models loaded successfully',
        'fr': 'Modèles ML chargés avec succès'
    },
    'no_predictions': {
        'en': 'No predictions available',
        'fr': 'Aucune prédiction disponible'
    },
    'top_risk_districts': {
        'en': 'Top Risk Districts',
        'fr': 'Districts à Haut Risque'
    },
    'prediction_summary': {
        'en': 'Prediction Summary',
        'fr': 'Résumé des Prédictions'
    },
    'accuracy': {
        'en': 'Accuracy',
        'fr': 'Précision'
    },
    'confidence': {
        'en': 'Confidence',
        'fr': 'Confiance'
    },
    'team': {
        'en': 'Team',
        'fr': 'Équipe'
    },
    'organization': {
        'en': 'Organization',
        'fr': 'Organisation'
    },
    'acknowledgments': {
        'en': 'Acknowledgments',
        'fr': 'Remerciements'
    },
    'report_issues': {
        'en': 'Report Issues',
        'fr': 'Signaler des Problèmes'
    },
    'future_enhancements': {
        'en': 'Future Enhancements',
        'fr': 'Améliorations Futures'
    },
    'disclaimer': {
        'en': 'Disclaimer',
        'fr': 'Avertissement'
    },
    'custom': {
        'en': 'Custom',
        'fr': 'Personnalisé'
    },
    'recent': {
        'en': 'Recent',
        'fr': 'Récent'
    },
    'analysis': {
        'en': 'Analysis',
        'fr': 'Analyse'
    },
    
    # ========================================================================
    # COMMON PHRASES
    # ========================================================================
    'developed_by': {
        'en': 'Developed by',
        'fr': 'Développé par'
    },
    'last_updated': {
        'en': 'Last Updated',
        'fr': 'Dernière Mise à Jour'
    },
    'dashboard_version': {
        'en': 'Dashboard Version',
        'fr': 'Version du Tableau de Bord'
    },
    'partner': {
        'en': 'Partner',
        'fr': 'Partenaire'
    },
}

# ============================================================================
# HELPER FUNCTION
# ============================================================================

def get_text(key, language='en'):
    """
    Get translated text for a given key.
    
    Args:
        key: Translation key
        language: 'en' or 'fr'
    
    Returns:
        Translated text, or key if not found
    """
    if key in translations:
        return translations[key].get(language, translations[key]['en'])
    return key
