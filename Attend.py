from tkinter.constants import GROOVE, RAISED, RIDGE
import cv2
import pyzbar.pyzbar as pyzbar
import time
from datetime import date, datetime
import tkinter as tk 
from tkinter import Frame, ttk, messagebox
from tkinter import *

window = tk.Tk()
window.title('Attendance System V-089')
window.geometry('900x600') 
                                                   
year= tk.StringVar()      
branch= tk.StringVar()
sec= tk.StringVar() 
period= tk.StringVar()

title = tk.Label(window,text="Attendance System V-089",bd=10,relief=tk.GROOVE,font=("times new roman",40),bg="lavender",fg="black")
title.pack(side=tk.TOP,fill=tk.X)

Manage_Frame=Frame(window,bg="lavender")
Manage_Frame.place(x=0,y=80,width=480,height=530)

# def checkk():
#     # if(year.get() and branch.get() and period.get() and sec.get()):
#     #     window.destroy()
#     # else:
#     #     messagebox.showwarning("Warning", "All fields required!!")

# exit_button = tk.Button(window,width=13, text="Submit",font=("Times New Roman", 15),command=checkk,bd=2,relief=RIDGE)
# exit_button.place(x=300,y=380)



Manag_Frame=Frame(window,bg="lavender")
Manag_Frame.place(x=480,y=80,width=450,height=530)

canvas = Canvas(Manag_Frame, width = 300, height = 300,background="lavender")      
canvas.pack()      
#img = PhotoImage(file="Bg.png")      
canvas.create_image(50,50, anchor=NW) #image=img 

window.mainloop()

cap = cv2.VideoCapture(0)
names=[]
today=date.today()
d= today.strftime("%b-%d-%Y")

fob=open(d+'.xlsx','w+')
fob.write("Reg No."+'\t')
fob.write("In Time"+'\n')

def enterData(z):   
    if z in names:
        pass
    else:
        it=datetime.now()
        names.append(z)
        z=''.join(str(z))
        intime = it.strftime("%H:%M:%S")
        fob.write(z+'\t'+'\t'+intime+'\n')
    return names 
    
print('Reading...')

def checkData(data):
    # data=str(data)    
    if data in names:
        print('Already Present')
    else:
        print('\n'+str(len(names)+1)+'\n'+'present...')
        enterData(data)

while True:
    _, frame = cap.read()         
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        checkData(obj.data)
        time.sleep(1)
       
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1)&0xFF == ord('g'):
        cv2.destroyAllWindows()
        break
    
fob.close()


from tkinter.constants import GROOVE, RAISED, RIDGE
import cv2
import pyzbar.pyzbar as pyzbar
import time
from datetime import date, datetime
import tkinter as tk 
from tkinter import Frame, ttk, messagebox
from tkinter import *
from playsound import playsound                                             

# title = tk.Label(window,text="Attendance System V-089",bd=10,relief=tk.GROOVE,font=("times new roman",40),bg="lavender",fg="black")
# title.pack(side=tk.TOP,fill=tk.X)

# Manage_Frame=Frame(window,bg="lavender")
# Manage_Frame.place(x=0,y=80,width=480,height=530)

# def checkk():
#     # if(year.get() and branch.get() and period.get() and sec.get()):
#     #     window.destroy()
#     # else:
#     #     messagebox.showwarning("Warning", "All fields required!!")

# exit_button = tk.Button(window,width=13, text="Submit",font=("Times New Roman", 15),command=checkk,bd=2,relief=RIDGE)
# exit_button.place(x=300,y=380)



# Manag_Frame=Frame(bg="lavender")
# Manag_Frame.place(x=480,y=80,width=450,height=530)

# canvas = Canvas(Manag_Frame, width = 300, height = 300,background="lavender")      
# canvas.pack()      
# #img = PhotoImage(file="Bg.png")      
# canvas.create_image(50,50, anchor=NW) #image=img 

# window.mainloop()

cap = cv2.VideoCapture(0)
names=[]
today=date.today()
d= today.strftime("%b-%d-%Y")

fob=open(d+'.xlsx','w+')
fob.write("Name."+'\t')
fob.write("Emp_id."+'\t')
fob.write("Email"+'\t')
fob.write("In Time"+'\n')

def enterData(z):   
    if z in names:
        pass
    else:
        it=datetime.now()
        names.append(z)
        z=''.join(str(z))
        intime = it.strftime("%H:%M:%S")
        fob.write(z+'\t'+'\t'+'\t'+intime+'\n')
    return names 
    
print('Camera Reading...')



def checkData(data):
    if data in names:
        print('Already Present')
        playsound(r'D:\Documents\Newproject\dong.wav')
        messagebox.showinfo("QR Code Already Present", "QR Code is already marked present!")
    else:
        print('\n'+str(len(names)+1)+'\n'+'Marked as present...')
        messagebox.showinfo("QR Code Marked as Present", "QR Code is marked as present!")
        enterData(data)


while True:
    _, frame = cap.read()         
    decodedObjects = pyzbar.decode(frame)
    for obj in decodedObjects:
        checkData(obj.data)
        time.sleep(1)
       
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1)&0xFF == ord('g'):
        cv2.destroyAllWindows()
        break
    
fob.close()



# from tkinter.constants import GROOVE, RAISED, RIDGE
# import cv2
# import pyzbar.pyzbar as pyzbar
# import time
# from datetime import date, datetime
# import tkinter as tk 
# from tkinter import Frame, ttk, messagebox
# from tkinter import *
# from playsound import playsound    

# cap = cv2.VideoCapture(0)
# names=[]
# today=date.today()
# d= today.strftime("%b-%d-%Y")

# fob=open(d+'.xlsx','w+')
# fob.write("Name."+'\t')
# fob.write("Emp_id."+'\t')
# fob.write("Email"+'\t')
# fob.write("In Time"+'\n')
# fob.write("out Time"+'\n')
# attendance_data = {}

# def enterData(z, is_out=False):
#     if z in names:
#         it = datetime.now()
#         z = ''.join(str(z))
#         if is_out:
#             outtime = it.strftime("%H:%M:%S")
#             attendance_data[z]['out_time'] = outtime
#             fob.write(z + '\t' + '\t' + '\t' + attendance_data[z]['in_time'] + '\t' + outtime + '\n')
#         else:
#             if z not in attendance_data:
#                 intime = it.strftime("%H:%M:%S")
#                 attendance_data[z] = {'in_time': intime}
#                 fob.write(z + '\t' + '\t' + '\t' + intime + '\n')

#     return names

# def checkData(data):
#     if data in names:
#         if 'out_time' in attendance_data[data]:
#             print('Already Marked Present and Out Time Recorded')
#             playsound(r'D:\Documents\Newproject\dong.wav')
#             messagebox.showinfo("QR Code Already Marked Present", "QR Code is already marked present and out time is recorded!")
#         else:
#             print('Already Present, Marking as Out...')
#             playsound(r'D:\Documents\Newproject\dong.wav')
#             messagebox.showinfo("QR Code Marked as Out", "QR Code is marked as out!")
#             enterData(data, is_out=True)
#     else:
#         print('\n' + str(len(names) + 1) + '\n' + 'Marked as present...')
#         messagebox.showinfo("QR Code Marked as Present", "QR Code is marked as present!")
#         enterData(data)

# while True:
#     _, frame = cap.read()
#     decodedObjects = pyzbar.decode(frame)
#     for obj in decodedObjects:
#         checkData(obj.data)
#         time.sleep(1)

#     cv2.imshow("Frame", frame)

#     if cv2.waitKey(1) & 0xFF == ord('g'):
#         cv2.destroyAllWindows()
#         break

# fob.close()




