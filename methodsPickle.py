import os
import pickle

authToken = ''

class PikleToken():
    '''
    Class for grouping pickle method
    '''
        
    def __init__(self, kat, plik):
        self.kat = kat
        self.plik = plik

    def pickleZapis(self, slownik):
        '''
        Save authToken to file as a pickle data
        '''
        pikelZap = open((os.path.join(self.kat, 'data', self.plik)), 'wb')
        pickle.dump(slownik, pikelZap)
        pikelZap.close()
    
    def pickleOdczyt(self):
        """
        Read authToken from file (pickle data)
        """
        pikel = open((os.path.join(self.kat, 'data', self.plik)), 'rb')
        dane=pickle.load(pikel)
        pikel.close()
        return dane


tokenObject = PikleToken(kat = os.getcwd(), plik = 'pikle')

if __name__ == '__main__':
    tokenObject = PikleToken(kat = os.getcwd(), plik = 'pikle')
    tokenObject.pickleZapis(authToken)
    test = tokenObject.pickleOdczyt() 
    print (test)
