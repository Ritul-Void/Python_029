import customtkinter as ctk
import tkinter as tk
import math
import matplotlib.pyplot as plt 
import numpy as np
from tkinter import messagebox

ctk.set_appearance_mode("bright")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        def dispPie(self,M,N):
            names = ['Invested Amount\n('+str(format(N,',d'))+')','Maturity Value\n('+str(format(M,',d'))+')'] 
            pi = np.array([N,M])
            fig = plt.figure(figsize=(5,5))

            plt.pie(pi,labels= names)
            plt.show()

        def Display(self,M,N):
            self.MatDisp.configure(text=str(format(M,',d')))
            self.AmtDisp.configure(text=str(format(N,',d')))
            self.Details = ctk.CTkButton(self,text='Details',fg_color = '#E74C3C',border_color='#E74C3C',command = lambda: dispPie(self,M,N))
            self.Details.grid(row = 6, column = 0, padx = 20, pady = 20, sticky= 'ew')
            # dispPie(self,M,N)

        
            

        def getSip(self,amt,te,pe) :
            P = amt
            i = float(pe/12)
            n = te*12

            M = int(P * ((pow((1+i),n)-1)/i) * (1+i))
            N = int(amt*n)
            print(M,N)
            Display(self,M,N)

        def getLump(self,lsamt,te,pe):
            P=lsamt
            M = math.ceil(P*(pow(1+pe,te)))
            print(M,P)
            Display(self,M,P)


        def mixedletters(quant):
            for i in range(len(quant)):
                if quant[i].isalpha():
                    return True
            return False

        def pressedCalculate():

            global tenure
            if self.ten.get() == '':
                messagebox.showerror('Error','Please enter the tenure of your investment')
                return
            elif '.' in self.ten.get():
                messagebox.showerror('Error','Entered a fractional value')
                return
            elif self.ten.get().isalpha() or mixedletters(self.ten.get()):
                messagebox.showerror('Error','Only numerical values allowed')
                return
            else :
                tenure = int(self.ten.get())
                if tenure == 0:
                    messagebox.showerror('Error','Tenure is zero')

            
            global per
            if self.roi.get() == '':
                messagebox.showerror('Error','Please enter the Rate of Return on your investment')
                return
            elif self.roi.get().isalpha() or mixedletters(self.roi.get()):
                messagebox.showerror('Error','Only numerical values allowed')
                return
            else:
                per = float(self.roi.get())
                if per > 0.0:
                    per /= 100
                    if per > 1.00:
                        messagebox.showerror('Error','ROI cannot be greater than 100')
                        return
                else :
                    messagebox.showerror('Error','ROI cannot be zero')
                    return

            
            global amount
            if self.Amt.get() == '' and self.ls.get() =='':
                messagebox.showerror('Error','Please enter Investment Value')
            elif self.ls.get() =='' and self.Amt.get() != '':
                if '.' in self.Amt.get():
                    messagebox.showerror('Error','Entered a fractional value')
                    return
                elif self.Amt.get().isalpha() or mixedletters(self.Amt.get()):
                    messagebox.showerror('Error','Only numerical values allowed')
                    return
                else:
                    amount = int(self.Amt.get())
                    getSip(self,amount,tenure,per)
            elif self.Amt.get() =='' and self.ls.get() != '' :
                if '.' in self.ls.get():
                    messagebox.showerror('Error','Entered a fractional value')
                    return
                elif self.ls.get().isalpha() or mixedletters(self.ls.get()):
                    messagebox.showerror('Error','Only numerical values allowed')
                    return
                else:
                    amount = int(self.ls.get())
                    getLump(self, amount, tenure, per)
            else:
                messagebox.showerror('Error','Please calculate either LumpSum or Sip not both at the same time')              

        def pressedReset():
            self.Amt.delete(0,'end')
            # self.ten.delete(0,'end')
            self.ls.delete(0,'end')
            self.roi.delete(0,'end')
            self.MatDisp.configure(text="")
            self.AmtDisp.configure(text="")
            self.Details.destroy()
            


        self.title("SIP Calculator")
        self.geometry('330x600')

        self.InputFrame = ctk.CTkFrame(master = self,fg_color='#F5B7B1')
        self.InputFrame.grid(row =0,column=0,sticky='ew')

        self.SIPamt = ctk.CTkLabel(master=self.InputFrame,text = 'SIP Amount  ')
        self.SIPamt.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = 'ew')

        self.Amt = ctk.CTkEntry(master=self.InputFrame,placeholder_text = '2000',border_color="#E74C3C")
        self.Amt.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = 'ew')
        

        self.Tenure = ctk.CTkLabel(master=self.InputFrame, text = "Tenure (in years) ")
        self.Tenure.grid(row = 1, column = 0, padx = 20, pady = 20,sticky = 'ew')

        self.ten = ctk.CTkComboBox(master=self.InputFrame,values = ['5','10','15','20','25','30','35'],border_color="#E74C3C",button_color="#E74C3C",dropdown_hover_color="#02b165")
        self.ten.grid(row = 1, column = 1, padx = 20, pady = 20, sticky = 'ew')

        self.ror = ctk.CTkLabel(master=self.InputFrame, text = 'Rate of Return (%) ')
        self.ror.grid(row = 2, column = 0, padx = 20, pady = 20,sticky = 'ew')

        self.roi = ctk.CTkEntry(master=self.InputFrame, placeholder_text= '12%',border_color="#E74C3C")
        self.roi.grid(row = 2, column = 1, padx = 20, pady = 20, sticky = 'ew')


        self.lumpSum = ctk.CTkLabel(master=self.InputFrame,text='Lump-sum Amount  ')
        self.lumpSum.grid(row = 3, column = 0, padx = 20, pady = 20, sticky = 'ew')

        self.ls = ctk.CTkEntry(master=self.InputFrame, placeholder_text = '1,00,000',border_color="#E74C3C")
        self.ls.grid(row = 3, column = 1, padx = 20, pady = 20, sticky = 'ew')

        self.Output = ctk.CTkFrame(master=self,fg_color='#E74C3C')
        self.Output.grid(row=1,column=0,sticky='ew')

        self.InvAmt = ctk.CTkLabel(master=self.Output,text ="Invested Amount")
        self.InvAmt.grid(row = 5, column = 0, padx = 20, pady = 20, sticky = 'ew')

        self.AmtDisp = ctk.CTkLabel(master=self.Output,text='')
        self.AmtDisp.grid(row = 5, column = 1, padx=20, pady = 20, sticky = 'ew')

        self.MatVal = ctk.CTkLabel(master=self.Output,text='Maturity Value   ')
        self.MatVal.grid(row = 6, column = 0,padx = 10,pady = 20, sticky = 'ew')

        self.MatDisp = ctk.CTkLabel(master=self.Output,text='')
        self.MatDisp.grid(row = 6, column = 1, padx = 20,pady =20, sticky = 'ew')
        
        self.Calculate = ctk.CTkButton(self,text="Calculate",fg_color="#E74C3C",border_color="black", command = pressedCalculate)
        self.Calculate.grid(row = 4, column = 0, padx = 20, pady = 20 ,sticky = 'ew')

        self.Reset = ctk.CTkButton(self,text="Reset",fg_color="#E74C3C",border_color="black",command = pressedReset)
        self.Reset.grid(row = 5,column = 0, padx =20, pady = 20, sticky = 'ew')
        

if __name__=="__main__":
    app = App()
    app.mainloop()