import sqlite3
from tkinter import *
from tkinter import messagebox

con = sqlite3.connect('')
cur = con.cursor()

#functions______________

def create_table():
    cur.execute('create table if not exists info(id integer primary key,username text,password integer)')
    con.commit()


def insert(username,password):
    cur.execute('insert into info(id,username,password) VALUES(null,?,?)',(username,password))
    con.commit()        


def update(id,new_username,newpassword):
    cur.execute('update info set username = ? , password = ? where id = ?',(new_username,newpassword,id))
    con.commit()


def delete(id):
    cur.execute('delete from info where id = ?',(id,))
    con.commit()

def search_(inp):
    cur.execute('select * from info where username like ? or password like ?',(inp,inp))
    record = cur.fetchall()
    return record

def select_():
    cur.execute('select * from info')
    record = cur.fetchall()
    return record


def clear():
    ent_name.delete(0,END)
    ent_pass.delete(0,END)
    ent_name.focus_set()




def insert_2():
    global records
    records = select_()
    create_table()
    username = ent_name.get().strip()
    password = ent_pass.get().strip()
    for record in records:
        if not username or not password:
            messagebox.showerror('!','you must enter username and password!')
            return
        if record[1] == username or record[2] == password:
            messagebox.showerror('error','you\'ve submited with these info.')
            return
        ent_name.focus_set()
        insert(username,password)
    clear()




def update_user():
    username = ent_name.get()
    password = ent_pass.get()
    index = lst_show.curselection()
    data = lst_show.get(index[0])
    result = messagebox.askquestion('?','do you want to save this changes?')
    if result == 'yes':    
        update(data[0],username,password)
        clear()
        show()
    clear()



def delete_user():
    index = lst_show.curselection()
    data = lst_show.get(index)
    result = messagebox.askquestion('?','are you sure you want to delete user ?')
    if result == 'yes':
        delete(data[0])
        clear()
        show()





def fetch(event):
    clear()
    index = lst_show.curselection()
    data = lst_show.get(index[0])
    ent_name.insert(0,data[1])
    ent_pass.insert(0,data[2])


def search():
    input_ = ent_search.get().strip()
    input_search = f'%{input_}%'
    lst_show.delete(0,END)
    result = search_(input_search)
    if not result:
        lst_show.insert(END,'nothing found')
        return
    for record in result:
        lst_show.insert(END,f'{record[1]} {record[2]}')

def show():
    lst_show.delete(0,END)
    create_table()
    cur.execute('select * from info')
    fetch = cur.fetchall()
    for fetchs in fetch:
        lst_show.insert(END,fetchs)





def exit():
    result = messagebox.askquestion('?','are you sure you want to exit?')
    if result == 'yes':
        win.destroy()



#________________
win = Tk()
win.geometry('400x500')
win.resizable(0,0)
win.config(bg='light blue')


#labels_________________________

lbl_name = Label(win,text='User name:',font='arial 15 bold',bg='light blue')
lbl_name.place(x=20,y=20)

lbl_password = Label(win,text='Password:',font='arial 15 bold',bg='light blue')
lbl_password.place(x=20,y=60)




#Entry_______________________

ent_name = Entry(win,width=25)
ent_name.place(x=140,y=27)

ent_pass = Entry(win,width=25,show='')
ent_pass.place(x=140,y=67)

ent_search = Entry(win,width=40)
ent_search.place(x=110,y=400,height=42)

#list box______________

lst_show = Listbox(win,width=50)
lst_show.place(x=10,y=130)







#Buttons______________________________

btn_show = Button(win,text='Show',font='tahoam 15 bold',command=show)
btn_show.place(x=20,y=350)

btn_cancel = Button(win,text='Exit',font='tahoma 15 bold',width=6,command=exit)
btn_cancel.place(x=100,y=350)

btn_submit = Button(win,text='Submit',font='tahoma 15 bold',width=12,command=insert_2)
btn_submit.place(x=20,y=300)

btn_edit = Button(win,text='Edit',font='tahoma 15 bold',width=12,command=update_user)
btn_edit.place(x=190,y=350)

btn_delete = Button(win,text='Delete',font='tahoma 15 bold',width=12,command=delete_user)
btn_delete.place(x=190,y=300)

btn_search = Button(win,text='search',font ='tahoma 15 bold',width=6,command=search)
btn_search.place(x=20,y=400)

lst_show.bind('<<ListboxSelect>>',fetch)

#==globals
records = select_()

win.mainloop()
con.close()