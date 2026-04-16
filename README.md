# Projet d'analyse de l'absentéisme au lycée

Ce projet génère un jeu de données simulé autour de l'absentéisme scolaire dans des lycées marocains. L'objectif est d'avoir une base exploitable pour l'analyse de données, la préparation BI et la mise en place de tableaux de bord Power BI centrés sur les causes possibles de l'absentéisme des élèves.

## Objectif

L'idée principale est de comprendre pourquoi les élèves ne viennent pas en classe, en croisant plusieurs dimensions:

- la région
- le type d'établissement
- le niveau et la filière
- les absences justifiées et non justifiées
- les notes et le risque de décrochage

Le projet est pensé comme un cas d'usage data analyst / data engineer, avec une logique de production de données, de modélisation, puis de restitution dans Power BI.

## Contenu du projet

- `generate_education_lycee_dataset.py`: script Python qui génère les données
- `data_raw/`: dossier de sortie des fichiers CSV produits par le script
- fichiers `.pbix`: rapports Power BI liés à l'analyse du projet

## Données générées

Le script produit plusieurs tables pour simuler un petit entrepôt de données:

- régions
- établissements
- classes
- élèves
- enseignants
- matières
- temps
- notes
- présences
- métriques élèves

Ces données permettent d'étudier les absences, les résultats scolaires et les disparités entre régions.

## Chaîne data et BI

Le projet suit une logique proche d'une chaîne data complète:

- préparation et génération des données avec Python et pandas
- organisation des fichiers pour exploitation analytique
- modélisation pour Power BI
- utilisation de SSIS pour l'alimentation et les flux ETL
- utilisation de SSAS pour la couche de modèle analytique

## Pourquoi ce jeu de données est utile

Le dataset a été construit pour permettre des analyses comme:

- comparaison des taux d'absentéisme par région
- lien entre absence et performance scolaire
- détection de profils à risque
- observation des variations saisonnières
- identification d'axes d'action pour réduire l'absentéisme

## Utilisation

1. Exécuter `generate_education_lycee_dataset.py`
2. Récupérer les CSV générés dans `data_raw/`
3. Charger les données dans Power BI ou un entrepôt analytique
4. Construire les mesures et visuels de suivi de l'absentéisme

## Stack

- Python
- pandas
- numpy
- Power BI
- SSIS
- SSAS

## Lecture du projet

Si vous voulez comprendre le projet rapidement, commencez par:

1. ce README
2. le script de génération des données
3. les rapports Power BI
