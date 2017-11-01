import os
import pickle

authToken = ''

class PikleToken():
    "Klasa grupujaca funkcje peklowania danych"
    
    def __init__(self, kat, plik, slownik=None):
        "konstruktor danych wejsciowych"
        
        self.kat = kat
        self.plik = plik
        self.slownik = slownik      

    def pickleZapis(self, slownik):
        """
        Funkcja zapisujaca plik z danymi w formacie pkl.
        Podajemy jako parametry katalog z danymi, nazwe pliku oraz
        krotke danych wejsciowych
        """
        pikelZap = open((os.path.join(self.kat, 'data', self.plik)), 'wb')
        pickle.dump(slownik, pikelZap)
        pikelZap.close()
    
    def pickleOdczyt(self):
        """
        Funkcja zwaracajaca odczytana liste enumeracji z pliku w formacie pkl.
        Podajemy jako parametry katalog z danymi, nazwe pliku
        """
        pikel = open((os.path.join(self.kat, 'data', self.plik)), 'rb')
        dane=pickle.load(pikel)
        pikel.close()
        return dane


# tworzenie instancji klasy Peklowanie
tokenObject = PikleToken(kat = os.getcwd(), plik = 'pikle')

# wywolanie funkcji zapisu do pliku z parametrem wejsciowym INPUTSTRING
if __name__ == '__main__':
    tokenObject = PikleToken(kat = os.getcwd(), plik = 'pikle')
    tokenObject.pickleZapis(authToken)
    test = tokenObject.pickleOdczyt() 
    print (test)
