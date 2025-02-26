import random
class Domanda:
    def __init__(self, testoDomanda, livelloDiff, rispCorr, rispErr1, rispErr2, rispErr3):
        self.testoDomanda = testoDomanda
        self.livelloDiff = livelloDiff
        self.rispCorr = rispCorr
        self.rispErr1 = rispErr1
        self.rispErr2 = rispErr2
        self.rispErr3 = rispErr3


class Gioco:
    def __init__(self):
        self.domandePerLivello = {}
        self.maxLivello = 0
        self.livelloCorrente = 0
        self.punteggio = 0

    def caricaDomande(self, fileName):
        with open(fileName, 'r', encoding= 'utf-8') as file:
            linee = [linea.strip() for linea in file.readlines()]

        blocchi = []
        bloccoCorrente = []

        for line in linee:
            if not line:                            ##se la riga è vuota, devo chiudere il blocco perche è finita la domanda
                if bloccoCorrente:                  ##controllo che il blocco non sia vuoto
                    blocchi.append(bloccoCorrente)  ##aggiungo il blocco della domanda alla lista dei blocchi
                    bloccoCorrente = []             ##azzero il contenuto del nuovo blocco che ospiterà la nuova domanda
            else:
                bloccoCorrente.append(line)         ##se la riga non è vuota, va aggiunta alla domanda attuale
        if bloccoCorrente:                          ##controllo che il blocco non sia vuoto
            blocchi.append(bloccoCorrente)          ##aggiungo

        for blocco in blocchi:                      ##dopo aver frammentato il file separando le domande in blocchi
            testoDomanda = blocco[0]                ##estraggo il testo della domanda
            livelloDiff = int(blocco[1])            ##e le altre cose contenute nelle righe successive
            rispCorr = blocco[2]
            rispErr1 = blocco[3]
            rispErr2 = blocco[4]
            rispErr3 = blocco[5]
                                                    ##poi creo un nuovo oggetto domanda corrispondente usando tali estrazioni
            domanda = Domanda(testoDomanda,livelloDiff,rispCorr,rispErr1,rispErr2,rispErr3)
            if livelloDiff not in self.domandePerLivello:           ##controllo se nella lista di liste che rappresenta i livelli con le rispettive domande è presente il livello della domanda creata
                self.domandePerLivello[livelloDiff] = []            ##se non c'è, creo una nuova lista di domande identificata dal [numero] del livello di diff della domanda
            self.domandePerLivello[livelloDiff].append(domanda)     ##aggiungo poi a questa nuova lista la domanda

            if livelloDiff > self.maxLivello:       ##infine controllo se il livDiff di questa dom sia il piu alto finora
                self.maxLivello = livelloDiff       ## in caso aggiorno il massimo

    def gestisciRisposta(self, risposte, corretta):
        risposteMiste = risposte.copy()                             ##importante per non dare problemi di liste
        random.shuffle(risposteMiste)                               ##mischio la nuova lista
        indiceRispCorretta = risposteMiste.index(corretta)          ##cerco l'indice a cui sta la mia corretta
        return risposteMiste, indiceRispCorretta

    def eseguiGioco(self):
        self.livelloCorrente = 0                                    ##inizia una nuova partita, azzero i valori del game
        self.punteggio = 0

        while True:                                                 ##ciclo infinito interrotto solo in caso di break
            if self.livelloCorrente > self.maxLivello:              ##se con le iterazioni ho superato il livello massimo devo interrompere
                print("hai superato tutti i livelli")
                break
            domande = self.domandePerLivello.get(self.livelloCorrente, [])        ##estraggo dalla lista che contiene le liste di domande associate ai rispettivi livelli la lista associata al livello corrente
            if not domande:                                                        ##se la lista è vuota, stoppo => fine lista domande ??
                break
            domanda = random.choice(domande)                        ##dalla lista estratta, prendo una domanda random
            risposte = [domanda.rispCorr + domanda.rispErr1 + domanda.rispErr2 + domanda.rispErr3]  ##da questa domanda random estraggo un array(lista) con le possibili risposte
            risposteMiste, indiceCorretto = self.gestisciRisposta(risposte, domanda.rispCorr)       ## sfrutto poi la funzione gestisci risposta usando l'array di risposte, estraendo cosi un mix delle risposte possibili e l'indice della risposta corretta

            print(f"\nLivello{self.livelloCorrente}) {domanda.testoDomanda}")       ## stampo il livello di gioco corrente con il testo della domanda

            for i, risp in enumerate(risposteMiste, 1):             ##ciclo che fa un count delle risposte mixate estratte sopra e le printa
                print(f"\nt{i}. {risp}")                            ## i è il count, risp sono le 4 risposte possibili

            scelta = input(f"inserisci risposta: ")                 ##faccio scrivere all'user la sua scelta in numero
            try:
                scelta = int(scelta)                                ##trasformo la scelta in intero, questo potrebbe generare eccezioni
                if 1 <= scelta <= 4 :
                    if scelta == indiceCorretto:                    ##se la scelta dell'user combacia con l'indice corretto estratto sopra tramite il metodo gestiscirisposta
                        print("risposta corretta!\n")               ##allora la risposta è corretta e aumento il punteggio
                        self.punteggio += 1                         ##poi mi chiedo se siamo gia all'ultimo livello
                        if self.livelloCorrente == self.maxLivello:
                            print("HAI VINTO!\n")
                            break                                   ##in tal caso l'user ha finito e ha vinto
                        self.livelloCorrente += 1                   ##altrimenti incremento il suo livello cosicche all'iterazione successiva acceda alle domande piu difficili
                    else:
                        print("risposta errata.\n")
                        break
                else:
                    print("Numero non valido. Risposta errata.\n")
                    break
            except ValueError:
                print("input non valido. Risposta errata.\n")
                break
        print(f"hai totalizzato {self.punteggio} punti!")
        return self.punteggio




def aggiorna_punteggi(nickname, punteggio):
    try:
        # Leggi i record esistenti dal file
        with open('punti.txt', 'r', encoding='utf-8') as file:
            records = [linea.strip().split() for linea in file if linea.strip()]
    except FileNotFoundError:            # Se il file non esiste, inizializza una lista vuota
        records = []

        # Aggiungi il nuovo record alla lista
    records.append([nickname, str(punteggio)])

    # Ordina i record in base al punteggio (in ordine decrescente)
    records_ordinati = sorted(records, key=lambda x: -int(x[1]))

    # Scrivi i record ordinati nel file
    with open('punti.txt', 'w', encoding='utf-8') as file:
        for record in records_ordinati:
            file.write(f"{record[0]} {record[1]}\n")




if __name__ == "__main__":

        gioco = Gioco()
        gioco.caricaDomande('domande.txt')
        punteggio = gioco.eseguiGioco()

        nickname = input("Inserisci il tuo nickname: ")
        aggiorna_punteggi(nickname, punteggio)