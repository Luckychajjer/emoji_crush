import tkinter as tk
from tkinter import messagebox
import pyautogui,random,sys

def printboard(boardlist):
    foregnd={'👺':'red','🤑':"yellow",'🤢':'green','🥶':"blue",'👿':"purple"}
    pos =0
    for i in range(5):
        for j in range(5):
            pnt_but = tk.Button(fra_1,text=boardlist[pos],
                                relief=tk.SUNKEN,font=('times',30),
                                command=check_but,background='black',border=2,
                                foreground=foregnd[boardlist[pos]])
            pnt_but.grid(row=i,column=j)
            pos+=1

def check_pattern(new):
    #horizontal row
    c1=[new-2,new-1,new]
    c2=[new,new+1,new+2]
    c3=[new-1,new,new+1]
    horizontal_row=[[0,1,2,3,4],[5,6,7,8,9],[10,11,12,13,14],[15,16,17,18,19],[20,21,22,23,24]]
    horizontal_pattern = [c1,c2,c3]
    valid_horizontal=[]
    for hp in horizontal_pattern:
        for hr in horizontal_row:
            if all(item in hr for item in hp):
                valid_horizontal.append(hp)

    #vertical row
    c4=[new-10,new-5,new]
    c5=[new,new+5,new+10]
    c6=[new-5,new,new+5]
    vertical_row=[[0,5,10,15,20],[1,6,11,16,21],[2,7,12,17,22],[3,8,13,18,23],[4,9,14,19,24]]
    vertical_pattern = [c4,c5,c6]
    valid_vertical=[]
    for vp in vertical_pattern:
        for vr in vertical_row:
            if all(item in vr for item in vp):
                valid_vertical.append(vp)

    valid_horizontal.extend(valid_vertical)
    return valid_horizontal

def checkmatch(new,boardlist):
    valid_pattern = check_pattern(new)
    match = 0
    correct_pattern = []
    for combo in valid_pattern:
       if (boardlist[combo[0]]==boardlist[combo[1]]) and (boardlist[combo[1]]==boardlist[combo[2]]) and (boardlist[combo[0]]==boardlist[combo[2]]):
        match = 1
        correct_pattern.append(combo)

    if match == 1:
        return correct_pattern[0]
    else:
       pass

def remove_match(correct_pattern,boardlist):
    for pos in correct_pattern:
        elements=['👺','🤑','🤢','🥶','👿']
        elements.remove(boardlist[pos-1])
        boardlist[pos]=random.choice(elements)
    return boardlist

def check_but():
    x,y = pyautogui.position()
    base_x = 628 # x and y cord of button1
    but_colomn = int((x-base_x)/98.8)#sub leftmost with button pos and divide with button width(98.8) 
    base_y = 256
    but_row = int((y-base_y)/98.8)
    pos = but_row*5 + but_colomn #row *5 (5 nos of elements in column) + the column it is in 

    global but_his,but_nos
    but_his.append(pos) 
    if but_nos == 0:
        but_nos+=1
    else:
        but_nos =0
        valid_but(but_his)
        but_his=[]
        
def valid_but(but_his):
    exh_but=[but_his[0]+1,but_his[0]-1,but_his[0]-5,but_his[0]+5]
    global boardlist,chance,point
    if but_his[1] in exh_but:
        prevboard = boardlist
        boardlist=change_position(but_his[1],but_his[0],boardlist)
        correct_pattern = checkmatch(but_his[0],boardlist)
        correct_pattern1 =checkmatch(but_his[1],boardlist)

        if correct_pattern == None and correct_pattern1 == None:
            boardlist = prevboard
            messagebox.showerror("Warning","wrong pattern")
        else:
            if correct_pattern == None:
                correct_pattern = correct_pattern1

            boardlist = remove_match(correct_pattern,boardlist)
            for i in range(25):
                correct_pattern = checkmatch(i,boardlist)
                if correct_pattern == None:
                    continue
                else:
                    boardlist = remove_match(correct_pattern,boardlist)
                    point+=100  #increment points if there is a double match while playing 

            printboard(boardlist)
            point+=100
            points['text'] = point
            chance-=1
            moves_left['text'] = chance if chance>0 else no_moves()

    else:
        messagebox.showerror("Warning","wrong move")
        
def change_position(old,new,boardlist):
    boardlist[old],boardlist[new] = boardlist[new],boardlist[old]
    return boardlist
    
def no_moves():
    global boardlist
    moves_left['text']=0 
    mess_state = messagebox.askyesno(title='Restart',message='Restart game?')
    if mess_state == True:
        boardlist=new_board()
    else:
        sys.exit()

def new_board():
    elements=['👺','🤑','🤢','🥶','👿']
    boardlist=[]
    global chance,point
    chance = 5
    point = 0
    points['text'] = point
    moves_left['text']=chance

    for i in range(25):
        boardlist.append(random.choice(elements))

    for i in range(25):
        correct_pattern = checkmatch(i,boardlist)
        if correct_pattern == None:
            continue
        else:
            boardlist = remove_match(correct_pattern,boardlist)    
    printboard(boardlist)
    return boardlist

window = tk.Tk()
window.title("EMOJI SAGA")
window.geometry("657x545+617+215")
window.resizable(False,False)
fra = tk.Frame(window,padx=10,pady=10,background='#273746')
fra_1 = tk.Frame(fra,padx=10,pady=13,background='#48C9B0')
fra_2 = tk.Frame(fra,padx=10,pady=5,background='#DAF7A6',border=2)

for i in range(8):   #to get blank frame and then we can use rowspan
    tk.Label(fra_2,
            padx=20,
            pady=20,background="#DAF7A6"
            ).grid(column=0,row=i,ipadx=25) 
    
moves_left  = tk.Label(fra_2,background="#DAF7A6",text=5,font=('times',25))
prt_move    = tk.Label(fra_2,background="#DAF7A6",text='Moves left',font=('times',13))
prt_point   = tk.Label(fra_2,background="#DAF7A6",text='Points',font=('times',15))
points      = tk.Label(fra_2,background="#DAF7A6",text=0,font=('times',25))
restart_but = tk.Button(fra_2,background="white",foreground="red",text='RESTART',relief=tk.RAISED,font=('times',10),border=5,command=no_moves)

prt_move.grid(row=0,sticky=tk.S)
moves_left.grid(row=1)
prt_point.grid(row=2,sticky=tk.S)
points.grid(row= 3,sticky=tk.N)
restart_but.grid(row= 4,rowspan= 2)

fra_1.grid(row=0,column=0)
fra_2.grid(row=0,column=1)
fra.grid()

but_nos = 0
but_his = []
point = 0       #print inital board
x = True
while x:
    boardlist =new_board()
    x= False

window.mainloop()