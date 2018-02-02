from flask import Flask
from flask import render_template, json, request
from random import randint
import os
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
        for i in range(3,-1,-1):
            fieldlist.append([6,i])
        for i in range(6,3,-1):
            fieldlist.append([i, 0])
        for i in range(1,5):
            fieldlist.append([4,i])
        for i in range(3,0,-1):
            fieldlist.append([i,4])
        for i in range(4, 6):
            fieldlist.append([0, i])
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


class pawn(board):

#który kolor bazy
    def whoiam(self, col):
        return {
        'red': [6,10],
        'blue': [10,4],
        'yellow': [4,0],
        'green': [0,6]
    }[col]

#wybór ruchu
    def check_move(self, cube, pawnlist, homelist, field, pawn_number, col):
        moveresult = ''
        if field in homelist: #wychodzi z bazy
            if cube == 6:
                x = self.whoiam(col)
                pawnlist[pawn_number] = x
                moveresult = 'Dobry ruch :)'
            else:
                moveresult = 'Nie możesz wykonać tego ruchu!'
        else: #jeśli pionek którym gracz chce się ruszyć nie jest w bazie
            new = self.move_forward(field, cube)
            pawnlist[pawn_number] = new
        pawnlist.append(moveresult)
        return pawnlist

#ruch do przodu
    def move_forward(self, field, cube):
        makelist = self.makelist()
        index = makelist.index(field)
        index = index + cube
        return makelist[index]

#wystaw pionek z bazy


#sprawdź ruch do przodu

#zbij pionek przeciwnika

#sprawdź bicie do tyłu

#poprawić wyświetlanie jaki pionek się rusza

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

yellow = b.set_yellow()
green = b.set_green()
red = b.set_red()
blue = b.set_blue()
blueh = b.blue_house()
redh = b.red_house()
yellowh = b.yellow_house()
greenh = b.green_house()
cube = b.cube()

rpawn = pawn()
rpos = red

gpawn = pawn()
gpos = green

ypawn = pawn()
ypos = yellow

bpawn = pawn()
bpos = blue


positions = []
positions.append(rpos)
positions.append(bpos)
positions.append(ypos)
positions.append(gpos)
positions.append('red')
positions.append(0)
positions.append(0)

marshal.dump(positions, open("data.marshal", "wb"))

@app.route('/',)
def start():
    return render_template('start.html')

@app.route('/game', methods=['GET', 'POST'])
def draw_board():
    whatisay = ''
    form_len = request.form

    red = b.set_red()
    blue = b.set_blue()
    yellow = b.set_yellow()
    green = b.set_green()
    blueh = b.blue_house()
    redh = b.red_house()
    yellowh = b.yellow_house()
    greenh = b.green_house()

    p = marshal.load(open("data.marshal", "rb"))
    rpos = p[0]
    bpos = p[1]
    ypos = p[2]
    gpos = p[3]
    col = p[4]
    cube = p[5]
    changeclass=p[6]

    turn = col

    if len(form_len) == 2:
        pawn_number = int(request.form['pawnnum'])

        if col == 'red':
            rpos = rpawn.check_move(cube, rpos, red, rpos[pawn_number], pawn_number, col)
            whatisay = rpos[4]
            rpos.pop()
            red = b.set_red()
            col = 'blue'

        elif col == 'blue':
            bpos = bpawn.check_move(cube, bpos, blue, bpos[pawn_number], pawn_number, col)
            whatisay = bpos[4]
            bpos.pop()
            blue = b.set_blue()
            col = 'yellow'

        elif col == 'yellow':
            ypos = ypawn.check_move(cube, ypos, yellow, ypos[pawn_number], pawn_number, col)
            whatisay = ypos[4]
            ypos.pop()
            yellow = b.set_yellow()
            col = 'green'

        else:
            gpos = bpawn.check_move(cube, gpos, green, gpos[pawn_number], pawn_number, col)
            whatisay = gpos[4]
            gpos.pop()
            green = b.set_green()
            col = 'red'

    else:
        cube = b.cube()

#zamiana - możliwy rzut albo ruch
    if changeclass == 1: changeclass = 0
    else: changeclass = 1

    print(bpos)
    positions = []
    positions.append(rpos)
    positions.append(bpos)
    positions.append(ypos)
    positions.append(gpos)
    positions.append(col)
    positions.append(cube)
    positions.append(changeclass)

    marshal.dump(positions, open("data.marshal", "wb"))

    return render_template('board.html', field=fields, blueh=blueh, redh=redh, yellowh=yellowh, greenh=greenh, cube=cube,
                           rpos=rpos, gpos=gpos, ypos=ypos, bpos=bpos, turn = turn, changeclass=changeclass, whatisay = whatisay) #na sztywno id?

if __name__ == '__main__':
    app.run(debug=True)




    #zaczyna gracz który pierwszy wyrzuci 6
#ese est percipi - istnieć to być potrzeganym !!!!!!!