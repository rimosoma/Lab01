import random


class Domanda:
    def __init__(self, testo, livello, risposta_corretta, risposte_errate):
        self.testo = testo
        self.livello = livello
        self.risposta_corretta = risposta_corretta
        self.risposte_errate = risposte_errate


class Gioco:
    def __init__(self):
        self.domande_per_livello = {}
        self.max_livello = 0
        self.livello_corrente = 0
        self.punteggio = 0

    def carica_domande(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            linee = [linea.strip() for linea in file]

        blocchi = []
        blocco_corrente = []
        for linea in linee:
            if not linea:
                if blocco_corrente:
                    blocchi.append(blocco_corrente)
                    blocco_corrente = []
            else:
                blocco_corrente.append(linea)
        if blocco_corrente:
            blocchi.append(blocco_corrente)

        for blocco in blocchi:
            testo = blocco[0]
            livello = int(blocco[1])
            corretta = blocco[2]
            errate = blocco[3:6]

            domanda = Domanda(testo, livello, corretta, errate)
            if livello not in self.domande_per_livello:
                self.domande_per_livello[livello] = []
            self.domande_per_livello[livello].append(domanda)

            if livello > self.max_livello:
                self.max_livello = livello

    def gestisci_risposta(self, risposte, corretta):
        risposte_miste = risposte.copy()
        random.shuffle(risposte_miste)
        indice_corretto = risposte_miste.index(corretta) + 1
        return risposte_miste, indice_corretto

    def esegui_gioco(self):
        self.livello_corrente = 0
        self.punteggio = 0

        while True:
            if self.livello_corrente > self.max_livello:
                print("Hai superato tutti i livelli!")
                break

            domande = self.domande_per_livello.get(self.livello_corrente, [])
            if not domande:
                break

            domanda = random.choice(domande)
            risposte = [domanda.risposta_corretta] + domanda.risposte_errate
            risposte_miste, indice_corretto = self.gestisci_risposta(risposte, domanda.risposta_corretta)

            print(f"\nLivello {self.livello_corrente}) {domanda.testo}")
            for i, risp in enumerate(risposte_miste, 1):
                print(f"\t{i}. {risp}")

            scelta = input("Inserisci la risposta: ")
            try:
                scelta = int(scelta)
                if 1 <= scelta <= 4:
                    if scelta == indice_corretto:
                        print("Risposta corretta!\n")
                        self.punteggio += 1
                        if self.livello_corrente == self.max_livello:
                            break
                        self.livello_corrente += 1
                    else:
                        print("Risposta errata.\n")
                        break
                else:
                    print("Numero non valido. Risposta errata.\n")
                    break
            except ValueError:
                print("Input non valido. Risposta errata.\n")
                break

        print(f"Hai totalizzato {self.punteggio} punti!")
        return self.punteggio


def aggiorna_punteggi(nickname, punteggio):
    try:
        with open('punti.txt', 'r', encoding='utf-8') as file:
            records = [linea.strip().split() for linea in file if linea.strip()]
    except FileNotFoundError:
        records = []

    records.append([nickname, str(punteggio)])

    records_ordinati = sorted(
        records,
        key=lambda x: (-int(x[1]), x[0]),
        reverse=False
    )

    with open('punti.txt', 'w', encoding='utf-8') as file:
        for record in sorted(records, key=lambda x: (-int(x[1]), x[0])):
            file.write(f"{record[0]} {record[1]}\n")


if __name__ == "__main__":
    gioco = Gioco()
    gioco.carica_domande('domande.txt')
    punteggio = gioco.esegui_gioco()

    nickname = input("Inserisci il tuo nickname: ")
    aggiorna_punteggi(nickname, punteggio)