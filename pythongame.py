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

#rzut kostką
    def cube(self):
        num = (randint(1, 6))
        return num

# kolor przypisany do numeru
    def colornumber(self, number):
        return {
            1: 'red',
            2: 'blue',
            3: 'yellow',
            4: 'green'
        }[number]

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
class Pawn(board):

    #który kolor bazy
    def whoiam(self, col):
        return {
        'red': [6,10],
        'blue': [10,4],
        'yellow': [4,0],
        'green': [0,6]
    }[col]

    #sprawdzenie ruchu u człowieka
    def check_move(self, cube, pawnlist, homelist, field, pawn_number, col, dealer, pos1, pos2, pos3, pos4): #field - stara pozycja []
        if field in homelist: #wychodzi z bazy
            if cube == 6:
                x = self.whoiam(col)
                beg = self.forwards(x, pos1, pos2, pos3, pos4, col, field, cube)
                if beg != 'Na tym polu już stoi twój pionek':
                    pawnlist[pawn_number] = x
            else:
                beg = 'Nie możesz wykonać tego ruchu!'
        elif dealer == 'forwards': #jeśli pionek którym gracz chce się ruszyć nie jest w bazie i ruch do przodu
            new = self.move_forward(field, cube) #współrzędne pola, na które chce przejść
            beg = self.forwards(new, pos1, pos2, pos3, pos4, col, field, cube)
            if type(beg) == list:
                pawnlist = beg
            elif beg == 1 or beg not in ('sinu','Nie możesz wykonać tego ruchu!', 'Ten pionek jest już w domu'):
                pawnlist[pawn_number] = new
        else: #jeśli gracz chce się ruszyć do tyłu
            fieldlist = self.makelist()
            temp = fieldlist.index(field)
            if temp > 39:
                beg = 'Nie możesz wykonać tego ruchu!'
            else:
                new = self.move_backward(field, cube)  # współrzędne pola, na które chce przejść
                beg = self.backwards(new, pos1, pos2, pos3, pos4, col, field)
                if beg == 1:
                    pawnlist[pawn_number] = new
        if type(beg) == str:
            pawnlist.append(beg)
        else:
            pawnlist.append('')
        return pawnlist

    #pole do przodu
    def move_forward(self, field, cube):
        makelist = self.makelist()
        if field in makelist:
            index = makelist.index(field)
            index = index + cube
            if index > 39:
                index = index - 40
            return makelist[index]

    #pole do tyłu
    def move_backward(self, field, cube):
        makelist = self.makelist()
        if field in makelist:
            index = makelist.index(field)
            index = index - cube
            if index < 0:
                index = 40 + index
            return makelist[index]

    #ruch do przodu i bicie
    def forwards(self, new, rpos, bpos, ypos, gpos, col, field, cube): #field - współrzędne przed ruchem
        trap = ([6,4],[4,6])
        untouch = ([4,4],[6,6])
        pos = list(self.tellmepos(col, rpos, bpos, ypos, gpos))
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
                moveresult = 1
        else:
            moveresult = amihome

        return moveresult

    #bicie do tyłu
    def backwards(self, new, rpos, bpos, ypos, gpos, col, field):
        makelist = self.makelist()
        newindex = makelist.index(new) #index po ruchu
        oldindex = makelist.index(field) #index przed ruchem
        if (col == 'red' and oldindex >9 and newindex<10) or (col == 'blue' and oldindex >19 and newindex<20) or (col == 'yellow' and oldindex >29 and newindex<30) or (col == 'green' and oldindex >=0 and newindex<40):
            moveresult = 'Nie możesz wykonać tego ruchu!'
        elif new in rpos: #bicie przez kolejne 4 elify
            if col == 'red':
                moveresult = 'Nie możesz wykonać tego ruchu!' #nie może zbić swojego pionka
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
                moveresult = 'Nie możesz wykonać tego ruchu!'
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
                moveresult = 'Nie możesz wykonać tego ruchu!'
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
                moveresult = 'Nie możesz wykonać tego ruchu!'
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

    #wyjdź z bazy
    def leavebase(self, fields, col):
        if col == 'red': homelist = self.set_red()
        elif col == 'blue': homelist = self.set_blue()
        elif col == 'yellow': homelist = self.set_yellow()
        else: homelist = self.set_green()
        for i in fields:
            if i in homelist: #wychodzi z bazy
                if cube == 6:
                    return 1
                else:
                    return 0
            else:
                return 0
    #ruch w domu
    def move_inhouse(self, homelist, cube, field): #pole przed ruchem jest w domu | field to index
        if field + cube < (homelist[1]+1): #ruch jak nie wychodzi poza dom
            field = field + cube #index po ruchu
            return field
        else:
            return 'Nie możesz wykonać tego ruchu!'

    #wybierz pozycje przypisane do koloru
    def tellmepos(self, col, rpos, bpos, ypos, gpos):
        if col == 'red':
            return rpos
        elif col == 'blue':
            return bpos
        elif col == 'yellow':
            return ypos
        else:
            return gpos

#wejście do domu

    #wejście do domu
    def gohome(self, field_before, cube, col, pos):
        fields = self.makelist() #lista wszystkich pól
        if field_before in fields:
            print(field_before,pos)
            index = fields.index(field_before) #indeks pola na którym stoi pionek przed ruchem
            posplace = pos.index(field_before) #index tegoż pola w liście pos
            new_index = index + cube
            if col == 'red':
                if index < 10 and new_index > 9: #ma wejść do domu
                    moveh = new_index - 9 #o ile się ruszyć w domu
                    if moveh < 5:
                        moveh = moveh -1
                        next_index = self.move_inhouse([44, 47], moveh, 44)  # index po ruchu
                        return self.check_ingohome(next_index, fields, pos, posplace)
                    else:
                        return 'Nie możesz wykonać tego ruchu!'
                elif index in range(44,47): #jest już w domu
                    next_index = self.move_inhouse([44,47], cube, index) #index po ruchu
                    return self.check_ingohome(next_index, fields, pos, posplace)
                elif index == 47:
                    return 'Ten pionek jest już w domu'
                else:
                    return 0
            elif col == 'blue':
                if index < 20 and new_index > 19: #ma wejść do domu
                    moveh = new_index - 19 #o ile się ruszyć w domu
                    if moveh < 5:
                        moveh = moveh -1
                        next_index = self.move_inhouse([48, 51], moveh, 48)  # index po ruchu
                        return self.check_ingohome(next_index, fields, pos, posplace)
                    else:
                        return 'Nie możesz wykonać tego ruchu!'
                elif index in range(48,51): #jest już w domu
                    next_index = self.move_inhouse([48,51], cube, index) #index po ruchu
                    return self.check_ingohome(next_index, fields, pos, posplace)
                elif index == 51:
                    return 'Ten pionek jest już w domu'
                else:
                    return 0
            elif col == 'yellow':
                if index < 30 and new_index > 29: #ma wejść do domu
                    moveh = new_index - 29 #o ile się ruszyć w domu
                    if moveh < 5:
                        moveh = moveh -1
                        next_index = self.move_inhouse([52, 55], moveh, 52)  # index po ruchu
                        return self.check_ingohome(next_index, fields, pos, posplace)
                    else:
                        return 'Nie możesz wykonać tego ruchu!'
                elif index in range(52,55): #jest już w domu
                    next_index = self.move_inhouse([52,55], cube, index) #index po ruchu
                    return self.check_ingohome(next_index, fields, pos, posplace)
                elif index == 55:
                    return 'Ten pionek jest już w domu'
                else:
                    return 0
            elif col == 'green':
                if index < 40 and new_index > 39: #ma wejść do domu
                    moveh = new_index - 39 #o ile się ruszyć w domu
                    if moveh < 5:
                        moveh = moveh -1
                        next_index = self.move_inhouse([40,43], moveh, 40)  # index po ruchu
                        return self.check_ingohome(next_index, fields, pos, posplace)
                    else:
                        return 'Nie możesz wykonać tego ruchu!'
                elif index in range(40,43): #jest już w domu
                    next_index = self.move_inhouse([40,43], cube, index) #index po ruchu
                    return self.check_ingohome(next_index, fields, pos, posplace)
                elif index == 43:
                    return 'Ten pionek jest już w domu'
                else:
                    return 0
        else:
            return 0

#elif w gohome

#sprawdzenie w funkcji gohome

#kod z gohome który się powtarza

    #funkcja z gohome
    def check_ingohome(self, next_index, fields, pos, posplace):
        if type(next_index) != str:
            new = fields[next_index] #współrzędne po ruchu
            if new in pos:
                return 'Nie możesz wykonać tego ruchu!'
            else:
                pos[posplace] = new
                return pos
        else:
            return next_index

#zbicie na polu trap

    #trap
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

    def checkgoinghome(self, pawns, cube, col, rpos, bpos, ypos, gpos):
        movelist = self.makelist()
        run = 'nic'
        count = 0 #nie może się ruszyć
        for i in pawns:
            if i in movelist:
                # możliwy rych do tyłu
                index = pawns.index(i)
                new = movelist[movelist.index(i)-cube]
                if new in (rpos, bpos, ypos, gpos) and new not in pawns:
                    count+=count

                run = self.gohome(i,cube,col,pawns)
                print(run)
                print(type(run))
                pawns[index] = i
                if type(run) == list:
                    count += count
        print('count', count)
        if count == 0:
            return 0
        else:
            return 1

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

#ile wspólnych pól w listach

    #czy są wspólne pola obu list
    def commonfields(self, list1, list2):
        l = 0
        fieldlist = []
        for x in list1:
            if x in list2:
                l+=1
                fieldlist.append(x)
        return l, fieldlist

    #zmiana wyświetlanego formularza
    def changeclass(self, result):
        if result in ('Na tym polu już stoi twój pionek', 'Nie możesz wykonać tego ruchu!'):
            return 0
        else:
            return 1

    #czy się może ruszyćw  domu
    def canmoveinhome(self, countinhome, makefields, home, cube):
        count = 0
        for i in countinhome[1]:
            move = self.move_inhouse([makefields.index(home[0]), makefields.index(home[3])], cube,
                                     makefields.index(i))
            if type(move) == list:
                count += count
        if count > 0:
            return 1
        else:
            return 0

    def canyoumove(self, pos, cube, col, rpos, bpos, ypos, gpos):
        pos1 = pos
        r1 = rpos
        b1 = bpos
        y1 = ypos
        g1 = gpos
        counter = 0
        for i in pos:
            newf = self.move_forward(i, cube)
            newb = self.move_backward(i, cube)

            if newf != None and newb != None:
                print('tutaj', type(self.forwards(newf, rpos, bpos, ypos, gpos, col, i, cube)))
                if self.forwards(newf, rpos, bpos, ypos, gpos, col, i, cube) == 1:
                    counter = 1
                    print(counter)

                if type(self.forwards(newf, rpos, bpos, ypos, gpos, col, i, cube)) == list:
                    counter = 1
                    print(counter)

                elif self.backwards(newb, rpos, bpos, ypos, gpos, col, i) == 1:
                    counter += counter

                elif self.leavebase(pos,cube) == 1:
                    counter += counter

                elif type(self.gohome(i, cube, col, pos))==list:
                    counter += counter

            if counter > 0:
                pos = pos1
                rpos = r1
                bpos = b1
                ypos = y1
                gpos = g1
                print('co2', counter)
                return 1

        pos = pos1
        rpos = r1
        bpos = b1
        ypos = y1
        gpos = g1
        print('co',counter)
        if counter>0:
            return 1
        else:
            return 0



    #czy może się ruszyć
    def canyoumoves(self, pos, base, home, cube, color, rpos, bpos, ypos, gpos):
        makefields = self.makelist()
        countinbase = self.commonfields(pos, base)#ile pionków jest w bazie
        countinhome = self.commonfields(pos, home)#ile pionków jest w domu
        if countinbase[0] != 4: #jeśli nie wszystkie pionki są w bazie
            if countinbase[0]+countinhome[0] == 4 and countinbase>0: #ale jeśli wszystkie pionki są w bazie lub domu
                print('jestem w superfunkcji')
                if cube == 6:
                    return 1
                elif cube == 4 or cube == 5:
                    return 0
                elif countinhome[0] ==1:
                    if countinhome[1][0] == home[3]:
                        return 0
                    else:
                        move = self.move_inhouse([makefields.index(home[0]),makefields.index(home[3])], cube, makefields.index(countinhome[1][0]))
                        if type(move) == str:
                            return 0
                        else:
                            return 1
                else:
                    for i in countinhome[1]:
                        move = self.move_inhouse([makefields.index(home[0]),makefields.index(home[3])], cube, makefields.index(i))
                        if type(move) == list:
                            break
                    if type(move) == list:
                        return 1
                    else:
                        return 0
            elif self.checkgoinghome(pos, cube, color, rpos, bpos, ypos, gpos) == 1:#czy może wejść do domu albo iść w tył
                return 1
            elif self.canmoveinhome(countinhome, makefields, home, cube) == 1: #czy może po prostu się ruszyć w przód po prostej
                return 1
            else:
                return 0

        else: #wszystkie pionki są w bazie
            return 1 #1-idzie normalna funkcja napisana wcześniej, 0- stata kolejki


b = board()
fields = b.makelist()

#tutaj zaczynają
yellow = b.set_yellow()
green = b.set_green()
red = b.set_red()
blue = b.set_blue()

cube = b.cube()

rpawn = Pawn()
rpos = red
gpawn = Pawn()
gpos = green
ypawn = Pawn()
ypos = yellow
bpawn = Pawn()
bpos = blue


@app.route('/',)
def start():
    return render_template('start.html')

@app.route('/losuj', methods=['GET', 'POST'])
def losuj():
    mynumber = int(request.form['humanplayers'])
    if mynumber == 0: #jak jest 0 to dostaje wartość z losowania
        p = marshal.load(open("data.marshal", "rb"))
        players = p[0]
        player = p[1]+1
        if player > players:
            player = 1

        cube = b.cube()
    else: #jak nie jest 0 to dostaje liczbe ludzkich graczy
        cube = 0
        player = mynumber
        players = int(request.form['humanplayers'])

    if cube == 6: #przekierowanie
        color = b.colornumber(player)
        positions = []
        positions.append([[5,6],[5,7], [5,9],[5,10]])
        positions.append(bpos)
        positions.append(ypos)
        positions.append(gpos)
        positions.append(color)  # kolor zaczynający tu
        positions.append(0)
        positions.append(0)  # counter
        marshal.dump(positions, open("data.marshal", "wb"))
        return render_template('whostarts.html', color=color)
    else:
        positions = []
        positions.extend([players, player])
        marshal.dump(positions, open("data.marshal", "wb"))
        return render_template('losuj.html', cube=cube)


@app.route('/game', methods=['GET', 'POST'])
def draw_board():
    whatisay = ''
    form_len = request.form
    endgame = 0

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
    counter = p[6]
    turn = col


    if len(form_len) == 2: #jeśli przesłane którym pionkiem ruch i w którą stronę
        pawn_number = int(request.form['pawnnum'])
        dealer = str(request.form['dir'])
        if col == 'red':
            #canyoumove, if 1 leci to co jest, else sama zmiana koloru
            rpos = rpawn.check_move(cube, rpos, red, rpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            end = rpawn.compare(rpos, redh)
            if end == 1:
                endgame = 1
            else:
                whatisay = rpos[4]
                rpos.pop()
                changeclass = rpawn.changeclass(whatisay)
                if changeclass == 1:
                    col = 'blue'
        elif col == 'blue':
            bpos = bpawn.check_move(cube, bpos, blue, bpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = bpos[4]
            bpos.pop()
            changeclass = rpawn.changeclass(whatisay)
            if changeclass == 1:
                col = 'yellow'
        elif col == 'yellow':
            ypos = ypawn.check_move(cube, ypos, yellow, ypos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = ypos[4]
            ypos.pop()
            changeclass = rpawn.changeclass(whatisay)
            if changeclass == 1:
                col = 'green'

        else:
            gpos = bpawn.check_move(cube, gpos, green, gpos[pawn_number], pawn_number, col, dealer, rpos, bpos, ypos, gpos)
            whatisay = gpos[4]
            gpos.pop()
            changeclass = rpawn.changeclass(whatisay)
            if changeclass == 1:
                col = 'red'

    else:
        cube = b.cube()

        if col == 'red':
            if cube <6 and rpawn.compare(rpos, red) == 1:
                changeclass = 1
                if counter<2:
                    counter=counter+1
                else:
                    counter = 0
                    col = 'blue'
            elif rpawn.canyoumove(rpos, cube, col, rpos, bpos, ypos, gpos) == 1:
                changeclass = 0
            else:
                changeclass = 1
                col = 'blue'
        elif col == 'blue':
            if cube < 6 and bpawn.compare(bpos, blue) == 1:
                changeclass = 1
                if counter<2:
                    counter=counter+1
                else:
                    counter = 0
                    col = 'yellow'
            elif cube == 6 and bpawn.compare(bpos, blue) == 1:
                changeclass = 0
            elif bpawn.canyoumove(bpos, cube, col, rpos, bpos, ypos, gpos) == 1:
                changeclass = 0
            else:
                changeclass = 1
                col = 'yellow'
        elif col == 'yellow':
            if cube < 6 and ypawn.compare(ypos, yellow) == 1:
                changeclass = 1
                if counter<2:
                    counter=counter+1
                else:
                    counter = 0
                    col = 'green'
            else:
                changeclass = 0
        elif col == 'green':
            if cube < 6 and gpawn.compare(gpos, green) == 1:
                changeclass = 1
                if counter<2:
                    counter=counter+1
                else:
                    counter = 0
                    col = 'red'
            else:
                changeclass = 0

    positions = []
    positions.extend([rpos, bpos, ypos, gpos, col, cube, counter])
    marshal.dump(positions, open("data.marshal", "wb"))
    if endgame == 0:
        return render_template('board.html', field=fields, cube=cube, rpos=rpos, gpos=gpos, ypos=ypos, bpos=bpos, turn = turn,
                               changeclass=changeclass, whatisay = whatisay)
    else:
        return render_template('endgame.html', color=col)

if __name__ == '__main__':
    app.run(debug=True)

#ese est percipi - istnieć to być potrzeganym !!!!!!!