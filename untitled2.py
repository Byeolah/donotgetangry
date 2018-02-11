class Zwierze():
    def __init__(self, imie, gatunek):
        self.imie=imie
        self.gatunek = gatunek

    def __repr__(self):
        print(self.imie, self.gatunek)

class Ssak(Zwierze):
    def ssak(self):
        return ''

class Ptak(Zwierze):
    def lataj(self):
        return ''

class Zoo():
    def dodaj_zwierze(self, lista, zwierze):
        lista.append(zwierze)


s1=Ssak('Bartek', 'pies')
s2=Ssak('Leon', 'lew')

zoo=Zoo()
lista = []
zoo.dodaj_zwierze(lista, s1)
zoo.dodaj_zwierze(lista,s2)

print(lista)


