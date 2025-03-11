import requests

# Wikipedia-Seite abrufen (requests)
r = requests.get('https://en.wikipedia.org/wiki/List_of_largest_companies_by_revenue')
# response object r

from bs4 import BeautifulSoup
# make html code searchable / parse html doc
soup = BeautifulSoup(r.text, 'html.parser')


# all tables
tables = soup.find_all('table', {'class': 'wikitable'})

# first big table
company_table = tables[0]

# test if correct table
print(company_table.prettify())


# In ein Pandas DataFrame umwandeln

# Spalten umbenennen & formatieren (z. B. "Revenue (USD billion)" → "Revenue (Billion USD)")
# Umsatzwerte (float) umwandeln
# Nicht benötigte Spalten entfernen

# Erste Analysen & Statistiken

    #Top 10 Unternehmen nach Umsatz
    #Durchschnittlicher Umsatz pro Land
    #Häufigste Branchen unter den größten Unternehmen

# Daten visualisieren

    #Balkendiagramm: Die 10 umsatzstärksten Unternehmen
    #Kreisdiagramm: Umsatzverteilung nach Branche
    #Histogramm: Verteilung der Mitarbeiterzahlen