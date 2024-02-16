import sqlite3
import customtkinter
from docxtpl import DocxTemplate

popis_ucitelja = []

db_connection = sqlite3.connect("ucitelji.db")
db = db_connection.cursor()

db.execute("SELECT prezime, ime FROM ucitelji ORDER BY prezime")
rows = db.fetchall()

for row in rows:
  puno_ime = " ".join(row)
  popis_ucitelja.append(puno_ime)


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("Zamii")

    self.geometry("600x500+300+100")
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.resizable(width=0, height=0)
    customtkinter.set_appearance_mode("system")


zamii = App()
zamii.mainloop()