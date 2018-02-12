from flask import Flask
from flask import render_template, request
from random import randint
import marshal

app = Flask(__name__)

class board:

    def __init__(self):
        k = 1

#Pola, po których można się poruszać
    def makelist(self):
        fieldlist = []
        for i in range(0, 5):
            fieldlist.append([i, 6])
        for i in range(7, 11):
            fieldlist.append([4, i])
        for i in range(5, 7):
            fieldlist.append([i, 10])
        for i in range(9, 5, -1):
            fieldlist.append([6,i])
        for i in range(7,11):
            fieldlist.append([i,6])
        for i in range(5,3,-1):
            fieldlist.append([10,i])
        for i in range(9,5,-1):
            fieldlist.append([i, 4])
        for i in range(3,0,-1):
            fieldlist.append([6,i])
        for i in range(6,3,-1):
            fieldlist.append([i, 0])
        for i in range(1,5):
            fieldlist.append([4,i])
        for i in range(3,0,-1):
            fieldlist.append([i,4])
        for i in range(4, 6):
            fieldlist.append([0, i])
        for i in range(1,5):
            fieldlist.append([i,5]) #40-43 zielone
        for i in range(9,5,-1):
            fieldlist.append([5,i])#44-47 czerwone
        for i in range(9,5,-1):
            fieldlist.append([i,5])#48-51 niebieskie
        for i in range(1,5):
            fieldlist.append([5,i])#52-55 żółte
        return fieldlist

    def blue_house(self):
        blue_home = []
        for i in range(9, 5,-1):
            blue_home.append([i,5])
        return blue_home

    def red_house(self):
        red_home = []
        for i in range(9, 5, -1):
            red_home.append([5, i])
        return red_home

    def green_house(self):
        green_home = []
        for i in range(1, 5):
            green_home.append([i, 5])
        return green_home

    def yellow_house(self):
        yellow_home = []
        for i in range(1, 5):
            yellow_home.append([5, i])
        return yellow_home

    def cube(self):
        num = (randint(1, 6))
        return num

#Żółte pola bazowe
    def set_yellow(self):
        yellow_list = []
        for i in (0,1):
            for j in (0,1):
                yellow_list.append([i,j])
        return yellow_list

#Niebieskie pola bazowe
    def set_blue(self):
        blue_list = []
        for i in (9,10):
            for j in (0,1):
                blue_list.append([i,j])
        return blue_list

#Czerwone pola bazowe
    def set_red(self):
        red_list = []
        for i in (9,10):
            for j in (9,10):
                red_list.append([i,j])
        return red_list

#Zielone pola bazowe
    def set_green(self):
        green_list = []
        for i in (0,1):
            for j in (9,10):
                green_list.append([i,j])
        return green_list


#klasa gracza
class pawn(board):

#który kolor bazy
    def whoiam(self, col):
        return {
        'red': [6,10],
        'blue': [10,4],
        'yellow': [4,0],
        'green': [0,6]
    }[col]

#sprawdzenie ruchu u człowieka
#funkcja wywołująca funkcje; wchodzą jakieś dane, sprawdza się jakiś warunek, w zależności zwraca liczę, potem w zalezności od liczby wybiera co dalej

    def check_move(self, cube, pawnlist, homelist, field, pawn_number, col, dealer, pos1, pos2, pos3, pos4): #field - stara pozycja
        beg = ''
        if field in homelist: #wychodzi z bazy
            if cube == 6:
                x = self.whoiam(col)
                beg = self.forwards(x, pos1, pos2, pos3, pos4, col, field, cube)
                if beg != 'Na tym polu już stoi twój pionek':
                    pawnlist[pawn_number] = x
        elif dealer == 'forwards': #jeśli pionek którym gracz chce się ruszyć nie jest w bazie i ruch do przodu
            new = self.move_forward(field, cube) #współrzędne pola, na które chce przejść
            beg = self.forwards(new, pos1, pos2, pos3, pos4, col, field, cube)
            if type(beg) == list:
                pawnlist = beg
            elif beg == 1 or beg != 'sinu':
                pawnlist[pawn_number] = new
        else: #jeśli gracz chce się ruszyć do tyłu
            new = self.move_backward(field, cube)  # współrzędne pola, na które chce przejść
            beg = self.backwards(new, pos1, pos2, pos3, pos4, col, field)
            if beg == 1:
                pawnlist[pawn_number] = new
        if type(beg) == str:
            pawnlist.append(beg)
        else:
            pawnlist.append('')
        print(pawnlist)
        return pawnlist

#pole do przodu
    def move_forward(self, field, cube):
        makelist = self.makelist()
        index = makelist.index(field)
        index = index + cube
        if index > 39:
            index = index - 40
        return makelist[index]

#pole do tyłu
    def move_backward(self, field, cube):
        makelist = self.makelist()
        index = makelist.index(field)
        index = index - cube
        if index < 0:
            index = 40 + index
        return makelist[index]

#ruch w domu
    def move_inhouse(self, homelist, cube, field): #pole przed ruchem jest w domu | field to index
        if field + cube < (homelist[1]+1): #ruch jak nie wychodzi poza dom
            field = field + cube #index po ruchu
            return field

    def tellmepos(self, col, rpos, bpos, ypos, gpos):
        if col == 'red':
            return rpos
        elif col == 'blue':
            return bpos
        elif col == 'yellow':
            return ypos
        else:
            return gpos


#bicie do tyłu
    def backwards(self, new, rpos, bpos, ypos, gpos, col, field):
        if new in rpos: #bicie przez kolejne 4 elify
            if col == 'red':
                moveresult = 'Nie możesz wykonać tego ruchu!' #nie może zbić swojego pionka | tu do zrobienia
            else:
                iwilldie = rpos.index(new) #z pozycji numer pozycji
                base = self.set_red()
                for x in base:
                    if x not in rpos:
                       gotit = x #wolne pole w bazie
                rpos[iwilldie] = gotit
                moveresult = 1
        elif new in bpos:
            if col == 'blue':
                moveresult = 'Nie możesz wykonać tego ruchu!' #tu do zrobienia
            else:
                iwilldie = bpos.index(new) #z pozycji numer pozycji
                base = self.set_blue()
                for x in base:
                    if x not in bpos:
                       gotit = x #wolne pole w bazie
                bpos[iwilldie] = gotit
                moveresult = 1
        elif new in ypos:
            if col == 'yellow':
                moveresult = 'Nie możesz wykonać tego ruchu!' #tu do zrobienia
            else:
                iwilldie = ypos.index(new) #z pozycji numer pozycji
                base = self.set_yellow()
                for x in base:
                    if x not in ypos:
                       gotit = x #wolne pole w bazie
                ypos[iwilldie] = gotit
                moveresult = 1
        elif new in gpos:
            if col == 'green':
                moveresult = 'Nie możesz wykonać tego ruchu!' #tu do zrobienia
            else:
                iwilldie = gpos.index(new) #z pozycji numer pozycji
                base = self.set_green()
                for x in base:
                    if x not in gpos:
                       gotit = x #wolne pole w bazie
                gpos[iwilldie] = gotit
                moveresult = 1
        else:
            moveresult = 'Nie możesz wykonać tego ruchu!'

        return moveresult

#wejście do domu
    def gohome(self, field_before, cube, col, pos):
        fields = self.makelist() #lista wszystkich pól
        if field_before in fields:
            index = fields.index(field_before) #indeks pola na którym stoi pionek przed ruchem
            posplace = pos.index(field_before) #index tegoż pola w liście pos
            if col == 'red':
                if index < 10 and index + cube > 9: #ma wejść do domu
                    home = self.red_house()
                elif field_before in ([5,9],[5,8],[5,7]): #jest już w domu
                    print('wchodze w elif')
                    next_index = self.move_inhouse([44,47], cube, index)
                    new = fields[next_index]
                    pos[posplace] = new
                    return pos
                elif index == 47:
                    print('Ten pionek jest już w domu')
                else:
                    return 0
        else:
            return 0
#ruch do przodu + bicie
    def forwards(self, new, rpos, bpos, ypos, gpos, col, field, cube): #field - współrzędne przed ruchem
        trap = ([6,4],[4,6])
        untouch = ([4,4],[6,6])
        pos = list(self.tellmepos(col, rpos,bpos,ypos,gpos))
        amihome = self.gohome(field, cube, col, pos)
        if amihome == 0: #jeśli pionek nie ma nic wspólnego z domem
            if new in trap: #zbity jak wejdzie na trap
                moveresult = self.trap(field, col, rpos, bpos, ypos, gpos)
            elif new in rpos: #bicie przez kolejne 4 elify
                if col == 'red':
                    moveresult = 'Na tym polu już stoi twój pionek' #nie może zbić swojego pionka | tu do zrobienia
                else:
                    if new in untouch:
                        moveresult = self.trap(field, col, rpos, bpos, ypos, gpos)
                    else:
                        iwilldie = rpos.index(new) #z pozycji numer pozycji
                        base = self.set_red()
                        for x in base:
                            if x not in rpos:
                               gotit = x #wolne pole w bazie
                        rpos[iwilldie] = gotit
                        moveresult = 1
            elif new in bpos:
                if col == 'blue':
                    moveresult = 'Na tym polu już stoi twój pionek' #tu do zrobienia
                else:
                    if new in untouch:
                        moveresult = self.trap(field, col, rpos, bpos, ypos, gpos)
                    else:
                        iwilldie = bpos.index(new) #z pozycji numer pozycji
                        base = self.set_blue()
                        for x in base:
                            if x not in bpos:
                               gotit = x #wolne pole w bazie
                        bpos[iwilldie] = gotit
                        moveresult = 1
            elif new in ypos:
                if col == 'yellow':
                    moveresult = 'Na tym polu już stoi twój pionek' #tu do zrobienia
                else:
                    if new in untouch:
                        moveresult = self.trap(field, col, rpos, bpos, ypos, gpos)
                    else:
                        iwilldie = ypos.index(new) #z pozycji numer pozycji
                        base = self.set_yellow()
                        for x in base:
                            if x not in ypos:
                               gotit = x #wolne pole w bazie
                        ypos[iwilldie] = gotit
                        moveresult = 1
            elif new in gpos:
                if col == 'green':
                    moveresult = 'Na tym polu już stoi twój pionek' #tu do zrobienia
                else:
                    if new in untouch:
                        moveresult = self.trap(field, col, rpos, bpos, ypos, gpos)
                    else:
                        iwilldie = gpos.index(new) #z pozycji numer pozycji
                        base = self.set_green()
                        for x in base:
                            if x not in gpos:
                               gotit = x #wolne pole w bazie
                        gpos[iwilldie] = gotit
                        moveresult = 1
            else: #ruch do przodu/wejście do domu
                moveresult = ''
        else:
            moveresult = amihome

        return moveresult

#zbicie na polu trap
    def trap(self, new, col, rpos, bpos, ypos, gpos):
        if col == 'red':
            iwilldie = rpos.index(new)
            base = self.set_red()
            for x in base:
                if x not in rpos:
                    gotit = x  # wolne pole w bazie
                rpos[iwilldie] = gotit
        elif col == 'blue':
            iwilldie = bpos.index(new)  # z pozycji numer pozycji
            base = self.set_blue()
            for x in base:
                if x not in bpos:
                    gotit = x  # wolne pole w bazie
            bpos[iwilldie] = gotit
        elif col == 'yellow':
            iwilldie = ypos.index(new)  # z pozycji numer pozycji
            base = self.set_yellow()
            for x in base:
                if x not in ypos:
                    gotit = x  # wolne pole w bazie
            ypos[iwilldie] = gotit
        else:
            iwilldie = gpos.index(new)  # z pozycji numer pozycji
            base = self.set_green()
            for x in base:
                if x not in gpos:
                    gotit = x  # wolne pole w bazie
            gpos[iwilldie] = gotit

        return 'sinu'

#sprawdź ruch do przodu - komputer

#niech się ogarnie jak nie wybierze pionka do ruchu

#porównuje listy
    def compare(self, list1, list2):
        l = 0
        for x in list1:
            if x in list2:
                l+=1
        if l == 4:
            return 1
        else:
            return 0

b = board()
fields = b.makelist()

#tutaj zaczynają
yellow = b.set_yellow()
green = b.set_green()
red = b.set_red()
blue = b.set_blue()

cube = b.cube()

rpawn = pawn()
rpos = red
gpawn = pawn()
gpos = green
ypawn = pawn()
ypos = yellow
bpawn = pawn()
bpos = blue

#dodać to do losowania
positions = []
positions.append([[5,9],[9,9],[9,10],[10,9]])
positions.append(bpos)
positions.append(ypos)
positions.append(gpos)
positions.append('red') #kolor zaczynający tu
positions.append(0)
positions.append(0)
positions.append(0) #counter

marshal.dump(positions, open("data.marshal", "wb"))

@app.route('/',)
def start():
    return render_template('start.html')


@app.route('/game', methods=['GET', 'POST'])
def draw_board():
    whatisay = ''
    form_len = request.form

    blueh = b.blue_house()
    redh = b.red_house()
    yellowh = b.yellow_house()
    greenh = b.green_house()

    p = marshal.load(open("data.marshal", "rb")) #plik rozbijany na to co potrzebne
    rpos = p[0]
    bpos = p[1]
    ypos = p[2]
    gpos = p[3]
    col = p[4]
    cube = p[5]
    changeclass=p[6]
    counter = p[7]
    turn = col


    if len(form_len) == 2: #jeśli przesłane którym pionkiem ruch i w którą stronę
        pawn_number = int(request.form['pawnnum'])
        dealer = str(request.form['dir'])
        if col == 'red':
            rpos = rpawn.check_move(cube, rpos, red, rpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = rpos[4]
            rpos.pop()
            col = 'blue'
        elif col == 'blue':
            bpos = bpawn.check_move(cube, bpos, blue, bpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = bpos[4]
            bpos.pop()
            col = 'yellow'
        elif col == 'yellow':
            ypos = ypawn.check_move(cube, ypos, yellow, ypos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = ypos[4]
            ypos.pop()
            col = 'green'
        else:
            gpos = bpawn.check_move(cube, gpos, green, gpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = gpos[4]
            gpos.pop()
            col = 'red'
    else:
        cube = b.cube()



#zamiana - możliwy rzut albo ruch - to coś nie działa
    if counter == 0:
        if changeclass == 1: changeclass = 0
        else: changeclass = 1
    elif counter == 3:
        counter = 0



    positions = []
    positions.extend([rpos, bpos, ypos, gpos, col, cube, changeclass, counter])

    marshal.dump(positions, open("data.marshal", "wb"))
    return render_template('board.html', field=fields, cube=cube, rpos=rpos, gpos=gpos, ypos=ypos, bpos=bpos, turn = turn,
                           changeclass=changeclass, whatisay = whatisay)

if __name__ == '__main__':
    app.run(debug=True)


    #zaczyna gracz który pierwszy wyrzuci 6
#ese est percipi - istnieć to być potrzeganym !!!!!!!