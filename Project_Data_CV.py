from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

UTILISATEUR = "SYSTEM"
MOT_DE_PASSE = "ton_mot_de_passe"
HOTE = "localhost"
PORT = "1521"
SERVICE = "XE"
pd.options.display.float_format = '{:,.2f}'.format

try:

    url_connexion = f"oracle+oracledb://{UTILISATEUR}:{MOT_DE_PASSE}@{HOTE}:{PORT}/?service_name={SERVICE}"
    moteur = create_engine(url_connexion)
    requete = "SELECT * FROM CLIENTS_CREDITS"
    df = pd.read_sql(requete, con=moteur)
    print(df.head())
    print("\nInformations sur le tableau récupéré :")
    print(df.info())

    print("\n--- Phase de Nettoyage ---")
    df  = df.replace('NA', np.nan)
    print("Valeurs manquantes par colonne :")
    print(df.isnull().sum())

    print("\n---Analyse des Risques---")
    repartition_risk = df['risk'].value_counts()
    print("Répartition globale du risque :")
    print(repartition_risk)
    montant_moyen = df.groupby('risk')['credit_amount'].mean()
    print("\nMontant moyen du credit selon le risque :")
    print(montant_moyen)
    print("\n---Génération des graphiques---")
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(1,2, figsize=(12, 5))
    sns.countplot(data=df, x='risk', hue='risk', palette={'good': '#2ecc71', 'bad': '#e74c3c'},legend=False, ax=axes[0])
    axes[0].set_title('Répartition des clients (Bons vs Mauvais)')
    axes[0].set_xlabel('Niveau de Risque')
    axes[0].set_ylabel('Nombre de clients')

    sns.barplot(data=df, x='risk', y='credit_amount',hue='risk', estimator='mean', palette={'good': '#2ecc71', 'bad': '#e74c3c'},legend=False, ax=axes[1])
    axes[1].set_title('Montant moyen emprunté selon le risque')
    axes[1].set_xlabel('Niveau de Risque')
    axes[1].set_ylabel('Montant moyen du crédit')

    plt.tight_layout()
    plt.show()
except Exception as e:
    print("\nUne erreur est survenue :")
    print(e)
