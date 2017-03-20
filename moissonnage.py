# coding: utf-8

import unicodecsv as csv
import requests
from bs4 import BeautifulSoup

nomFichier = "contrats-tresor.csv"
fichier = open(nomFichier,"a")
fichieWriter = csv.writer(fichier)

# Préparation pour récupération contrat de la chambre du trésor
urlTresor = "http://www.tbs-sct.gc.ca/scripts/contracts-contrats/reports-rapports-fra.asp?r=l&yr=2015&q=3&d="

entetes = {
	"User-Agent":"Myriam Gendron - Requête envoyée dans le cadre d'un cours de journalisme informatique à l'UQAM (EDM5240)",
	"From":"myriamgendron94@gmail.com" # TODO Mettre email ici
}

# Récupération du contenu de la page
contenu = requests.get(urlTresor, headers=entetes)

# Parse de la page 
page = BeautifulSoup(contenu.text,"html.parser")
lignes = page.find_all("tr")
nbLigne = 0

print("=====================================================")
print("Création du fichier csv...")
for ligneCourante in lignes:

    #La ligne d'en-tête contient des classes, on l'ignore donc pour se concentrer sur les données
    if ligneCourante.get('class') is None:
        # Récupération de la page de détails d'un contat
        lien = ligneCourante.a.get("href")

        contentPageContrat = requests.get("http://www.tbs-sct.gc.ca/scripts/contracts-contrats/" + lien, headers=entetes)
        pageContrat = BeautifulSoup(contentPageContrat.text, "html.parser")

        infoContrat = []

        lignesDetailsContrat = pageContrat.find_all("tr")
        # === Ajout des différentes informations ===

        # Ajout du vendeur
        infoContrat.append(lignesDetailsContrat[0].td.text)

        # Ajout du Numéro de Ref
        infoContrat.append(lignesDetailsContrat[1].td.text)

        # Ajout du descriptif
        infoContrat.append(lignesDetailsContrat[3].td.text)

        # Ajout des dates
        dates = lignesDetailsContrat[4].td.text.split()
        infoContrat.append(dates[0]) # Date de début
        infoContrat.append(dates[2] if len(dates) >= 3 else "N/A") # Date de fin

        valeurOriginale = lignesDetailsContrat[6].td.text.replace('$', '')

        valeurOriginale = valeurOriginale.replace(" ", '')
        valeurOriginale = "".join(valeurOriginale.split())

        valeuFinale = lignesDetailsContrat[5].td.text.replace('$', '')
        valeuFinale = "".join(valeuFinale.split())
        # Ajout valeur originale
        infoContrat.append(valeurOriginale)

        # Ajout valeur finale
        infoContrat.append(valeuFinale)

        # Ajout différence de coût
        infoContrat.append(float(valeuFinale.replace(",", ".")) - float(valeurOriginale.replace(",", ".")))

        # Ajout du lien dans les informations
        infoContrat.append(lien)

        # Ajout description
        infoContrat.append(lignesDetailsContrat[7].td.text)

        # Ajout commentaire
        infoContrat.append(lignesDetailsContrat[8].td.text)

        nbLigne += 1
        fichieWriter.writerow(infoContrat)

print("Nombre de lignes au total: {}".format(nbLigne))
print("Création du fichier [{}]".format(nomFichier))
