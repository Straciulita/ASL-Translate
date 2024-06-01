from tkinter import *
from PIL import Image, ImageTk
import subprocess
import sys
import threading
import os
import time


# Funcția pentru a citi output-ul din fișier într-un thread separat
def read_output(output_text):   # functie pt a citii output ul din  fisier ... ce imi afiseaza in consola trec in fisier si de acolo iau datele
    while True:
        if os.path.exists('output.txt'):
            with open('output.txt', 'r') as f:
                output_text.delete('1.0', END)
                output_text.insert(END, f.read())
        time.sleep(1)


# Funcțiile pentru evenimentele butoanelor
def OnClickASL():   # functie pt butonul asl to text
    frame_Start.pack_forget()   # fac frame ul de start invizibil
    frame_ASL.pack(fill='both', expand=True)   # fac frame ul de asl in text vizibil

# functie pt butonul text to asl
def OnClickTEXT():
    frame_Start.pack_forget()
    frame_Text.pack(fill='both', expand=True)

# functia pt butonul back
def OnClickBack():
    frame_ASL.pack_forget()
    frame_Text.pack_forget()
    frame_Start.pack(fill='both', expand=True)


def OnClickStart():   #functia pt butonul start
    # Șterge conținutul vechi din fișierul output.txt
    if os.path.exists('output.txt'):
        os.remove('output.txt')

    # Deschide procesul recunoasterea.py
    process = subprocess.Popen([sys.executable, "recunoasterea.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)

    # Creare thread pentru citirea output-ului
    thread = threading.Thread(target=read_output, args=(output_text,))
    thread.daemon = True
    thread.start()

def OnClickTranslate():   #functie pt butonul translate
    img_window = Toplevel(window)   # creez fereastra in care se vor afisa elemente
    text = output_text1.get("1.0", "end-1c")  # iau textul din spatiul destinat
    letters = [char.upper() for char in text if char.isalpha()]
    display_images_sequentially(letters, img_window)  #afisez imaginiile

def display_images_sequentially(letters, img_window):   # functie pt afisa imaginile corespunzator
    if letters:
        letter = letters.pop(0)
        display_image(letter, img_window)
        window.after(3000, lambda: display_images_sequentially(letters, img_window))
    else:

        img_window.destroy() # dupa ce se afiseaza imaginile sterg fereastra

def display_image(letter, img_window):  # functie pt afisa o imagine
    try:

        image = Image.open(f"Litere/{letter}.png")  # cauta poza corespunzatoare literei respective
        image = ImageTk.PhotoImage(image)


        for widget in img_window.winfo_children():
            widget.destroy()


        img_label = Label(img_window, image=image)
        img_label.image = image
        img_label.pack()

    except FileNotFoundError:
        print(f"No image found for letter: {letter}")


# Fereastra principala
window = Tk()
window.geometry('620x490')
window.title('ASL translate')
window.configure(bg='#bbf2fc')

#Poza din bara
icon = PhotoImage(file='Poze/istockphoto-1345842412-612x612.png')
window.iconphoto(True, icon)

# Elementele din fereastră
frame_Start = Frame(window, bg='#bbf2fc')#frame ulm pt pagina de start
frame_Start.pack() # afisez frame ul

frame_ASL = Frame(window, bg='#bbf2fc')#frame ul pt pagina ce traduce asl in text

frame_Text = Frame(window, bg='#bbf2fc')# frameul pt pagina ce traduce text in asl

poza = ImageTk.PhotoImage(file='Poze/ASL-cover-image.png') # poza pt frame ul de start

#textu wellcome
wlc = Label(frame_Start, text='*WELCOME*', font=('Comic Sans MS', 35, 'bold'), bg='#bbf2fc', fg='#0d1559', image=poza,
            compound='bottom')
wlc.pack(pady=20) # afisez textul cu o distanta de sus si jos de 20 de pixeli

#intrebarea
q = Label(frame_Start, text='What do you want to do?', font=('Comic Sans MS', 15), bg='#bbf2fc', fg='#0d1559')
q.pack(pady=10)# afisez textul cu o distanta de sus si jos de 10 de pixeli

# un frame pt butoane pt a le afisa frumix una langa alta
button_frame = Frame(frame_Start, bg='#bbf2fc')
button_frame.pack(pady=20)

#poze pt butoane
original_image_asl = Image.open('Poze/ASL TO TEXT.png')
pic_asl = ImageTk.PhotoImage(original_image_asl)

#buton
asl_to_text = Button(button_frame, image=pic_asl, command=OnClickASL, bg='#92e8f7', highlightthickness=0)
asl_to_text.pack(side=LEFT, padx=25)

#poze pt butoane
original_image_text = Image.open('Poze/TEXT TO ASL.png')
pic_text = ImageTk.PhotoImage(original_image_text)

#buton
text_to_asl = Button(button_frame, image=pic_text, command=OnClickTEXT, bg='#92e8f7', highlightthickness=0)
text_to_asl.pack(side=LEFT)

#frame ul ce face traducerea din asl in text

#text
instr = Label(frame_ASL, text='How to use?', font=('Comic Sans MS', 35, 'bold'), bg='#bbf2fc', fg='#0d1559')
instr.pack(pady=20)

#butonul back
back = Button(frame_ASL, text='Back', font=('Comic Sans MS', 12, 'bold'), bg='#92e8f7', fg='#0d1559',
              command=OnClickBack)
back.place(x=10, y=10)

#text
text = Label(frame_ASL, text=(' Show the gesture you want to translate to the camera. '
                              'The camera will recognize the gesture, and the corresponding letter or word will appear in the designated space. '
                              'The dislike is for deleting the letter or word if the gesture was not recognized correctly the first time, '
                              'and the like is for adding a space. Enjoy!'), font=('Comic Sans MS', 12), bg='#bbf2fc',
             fg='#0d1559', wraplength=450)
text.pack(pady=20, padx=20)

#butonul start
Start = Button(frame_ASL, text='Start', font=('Comic Sans MS', 15, 'bold'), bg='#92e8f7', fg='#0d1559',
               command=OnClickStart)
Start.pack(pady=(10, 20))

#spatiul iin care se genereaza textul pe care il recunoaste la camera
output_text = Text(frame_ASL, font=('Comic Sans MS', 12), bg='#ffffff', fg='#0d1559')
output_text.pack(pady=20, padx=20, fill='both', expand=True)

# farme ul ce traduce text in asl

#text
instr = Label(frame_Text, text='How to use?', font=('Comic Sans MS', 35, 'bold'), bg='#bbf2fc', fg='#0d1559')
instr.pack()

#butonul back
back = Button(frame_Text, text='Back', font=('Comic Sans MS', 12, 'bold'), bg='#92e8f7', fg='#0d1559',
              command=OnClickBack)
back.place(x=10, y=10)

#text
text = Label(frame_Text, text=(' Write the text you want to translate, click "Translate," and wait for the images to be generated. Have fun! '), font=('Comic Sans MS', 12), bg='#bbf2fc',
             fg='#0d1559', wraplength=450)
text.pack(pady=20, padx=20)

#butonul transalte
Translate = Button(frame_Text, text='Translate', font=('Comic Sans MS', 15, 'bold'), bg='#92e8f7', fg='#0d1559',
               command=OnClickTranslate)
Translate.pack(pady=(10, 20))

#spatiul in care utilizatorul scrie textul pe care il are de tradus
output_text1 = Text(frame_Text, font=('Comic Sans MS', 12), bg='#ffffff', fg='#0d1559')
output_text1.pack(pady=20, padx=20, fill='both', expand=True)

# Începe bucla principală a interfeței grafice
window.mainloop()
