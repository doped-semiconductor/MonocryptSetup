from os import chdir, system, getcwd, path, mkdir
from hashlib import sha256
from subprocess import Popen
from tkinter import filedialog, messagebox
import tkinter as tk
from cryptography.fernet import Fernet


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):  
        self.char = "*"   

        self.passtext = tk.Label(self, text="Set New Password:")
        self.passtext.grid(row = 2, column = 1, sticky='E') 

        self.tb=tk.Entry(self, width=63, show=self.char) 
        self.tb.grid(row = 2, column = 2, sticky='W') 

        self.tog = tk.Button(self,text="(>▂<)",command=self.togglePas)
        self.tog.grid(row=2,column=3, sticky='W')

        self.note = tk.Label(self, padx=20, text="Note: Forgetting your password could lead to permanent loss of your files.")
        self.note.grid(row = 3, column = 1, columnspan=3)  

        self.gap = tk.Label(self, text=" ")
        self.gap.grid(row = 4, column = 1) 

        self.dir=tk.Text(self, height=1, width=60) 
        self.dir.grid(row = 5, column = 1,columnspan=2)  
        self.dir.config(state='disabled') 

        self.lab = tk.Button(self, text="Select Folder",command=self.chooseDir)
        self.lab.grid(row = 5, column = 3)

        self.gap = tk.Label(self, text=" ")
        self.gap.grid(row = 6, column = 1)

        self.next = tk.Button(self, text="Proceed",command=self.check)
        self.next.grid(row = 7, column = 1, columnspan=3) 
    def chooseDir(self):
        self.select = filedialog.askdirectory()
        self.dir.config(state='normal')
        self.dir.insert('1.0',self.select)
        self.dir.config(state='disabled')
    def togglePas(self):
        if self.char!="*":
            self.char = "*"
            self.tog['text'] = "(>▂<)"
        else:
            self.char = ""
            self.tog['text'] = "(◉▂◉)"
        self.tb.config(show=self.char)
    def check(self): 
        setuploc = getcwd()
        # print('cwd',getcwd())
        # print(path.join(getcwd(),'Monocrypt'))  
        newpath = self.select.replace('/','\\')
        chdir(newpath)
        mkdir('Monocrypt')
        chdir('Monocrypt')
        newpath = path.join(newpath,'Monocrypt')
        cmd = 'xcopy '+path.join(setuploc,"Monocrypt")+' '+newpath
        print(cmd)        
        # system('mkdir Monocrypt')
        system(cmd)
        chdir(newpath)
        system('mkdir Notes')
        system('attrib +h Notes')
        f = open('p.p','w')
        f.write(sha256(self.tb.get().encode() + self.tb.get().encode()).hexdigest())
        f.close()
        f = open('n.p','wb')
        f.write(Fernet.generate_key())
        f.close()        
        system('attrib +r +h p.p')
        system('attrib +r +h n.p')
        self.master.quit()
        messagebox.showinfo(title="Setup Completed",message="Please find Monocrypt/app.exe in:\n"+self.select)
        loc = 'explorer '+self.select
        loc = loc.replace('/','\\')
        Popen(loc)


if __name__=="__main__":
    print('cwd:',getcwd())
    root = tk.Tk()
    root.title('MonoCrypt Setup')
    root.resizable(0,0)
    root.iconbitmap("lock.ico")
    app = Application(master=root)
    app.mainloop()