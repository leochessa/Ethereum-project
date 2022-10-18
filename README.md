# README #

Attraverso questo readme illustriamo i procedimenti di pulizia dei testi dei contratti estratti nel branch
Web-Scraping-e-Parsing , la creazione del dizionario riassuntivo contenente i contratti e la successiva topic modelling
che applicheremo.

### Obbiettivi ###

* Pulizia contratti
* Creazione dizionario
* Topic modelling

### Pulizia dei contratti ###

* Installazione di tutte le librerie presenti su requirements.txt
* Attraverso la programmazione ad oggetti creiamo diverse funzioni richiamabili
* Apriamo il file contracts.csv, creato nel branch Web-Scraping-e-Parsing
* Creiamo un set vuoto, per evitare doppioni, dove inseriremo i contratti puliti
* Attraverso le Regex effettuiamo una prima pulizia del testo, quantomeno per la punteggiatura
* Completiamo la pulizia attraverso un doppio ciclo for, grazie anche all'utilizzo di una lista

### Creazione ?dizionario? ###

* Il testo dei contratti puliti viene dapprima inserito nel set precedentemente creato
* Attraverso un semplice ciclo for copiamo gli elementi del set in un dizionario per poi effettuare la topic modelling
* E' stato creato anche un dataset a partire dal dizionario in modo da poterlo visualizzare meglio

### Topic modelling ###

* Repo owner or admin
* Other community or team contact

#########################################################

## PROGETTO LOBINA-CHESSA ##

### SMART CONTRACT WITH ETHERIUM ###
*  SCRAPING DEI CONTRATTI
*  STOPWORDS E PULIZIA DEI TESTI
*  CREAZIONE DATASET
*  TOPIC MODELLING
*  DEDUZIONI E CONCLUSIONI
*  PRESENTAZIONE

# 

Per ottenere il file csv (aggiornato) generato nel Branch Web-Scraping-e-Parsing
è sufficiente scrivere nel terminale:

"git checkout origin/Web-Scraping-e-Parsing Deposito_contratti"


