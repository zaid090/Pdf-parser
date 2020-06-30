from tkinter import *
from tkinter import filedialog
import os
from Analyser import Analyser as An
import temp
import tabula as tb

global s1,s2,s3,s4,s5

class gui:
    def __init__(self):
        self.root = Tk()
        self.analyse = An()
        self.root.title('HTJZ')
        #self.root.iconbitmap("d:/projects/images.ico")
        self.root.minsize(400,800)
        self.Frame1 = LabelFrame(self.root,bg='#2980B9')
        self.Frame1.grid(row=0,column=3)
        self.button1 = Button(self.Frame1,text="Choose a file",command=self.openfile)
        self.button1.grid(row=0,column=0)

        self.Process_button = Button(self.root,text="CLick Here To Process Data",width=50,height=5,bg='red',command = self.process)
        self.Process_button.grid(row=2,column=3)
        

        self.frame2 = LabelFrame(self.root,bg='yellow')
        self.frame2.grid(row=4,column=3)
        m = 5
        self.subject_box = list()
        
        

        


    def openfile(self):
        
        self.filename = filedialog.askopenfilename(initialdir="/",title="Select a Pdf",filetypes=(("pdf files","*.pdf"),("all files","*.*")) )
        self.my_label = Label(self.Frame1,text=self.filename)
        self.my_label.grid(row=1,column=0,padx=20,pady=20)
    
        
    def process(self):        
        m = 5
        self.subject_codes = self.analyse.PDF_parser(self.filename)
        for i in self.analyse.subject_codes :
            self.subject_label = Label(self.frame2,text= i)
            self.subject_label.grid(row = m,column = 2)
            self.subject = Entry(self.frame2,width=50)
            self.subject.grid(row = m,column=3,padx=20,pady=20)
            self.subject_box.append(self.subject)
            m += 1
        self.sub_button = Button(self.frame2,text="Confirm",command=self.get_data)
        self.sub_button.grid(row=m,column=3)

        
        

    
    def get_data(self):
        subs = list()
        self.m = 0
        self.Sub_codes_to_names = dict()
        for i in self.analyse.subject_codes:
            
            subs.append(str(self.subject_box[self.m].get()))
            self.subject_box[self.m].insert(INSERT,subs[self.m])
            self.subject_box[self.m].delete(0,END)
            self.Sub_codes_to_names[i] = subs[self.m]
            self.m += 1
        #print(s1,s2,s3,s4,s5)
        File = self.analyse.Analysis(self.Sub_codes_to_names)
        temp.plot_pie([self.analyse.Total_rank["Pass"], self.analyse.Total_rank["Fail"]],["Pass","Fail"])
        os.startfile(File)
       
        



app = gui()
app.root.mainloop()






