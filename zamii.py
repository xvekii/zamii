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


class ZamjenaFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    mylabel = customtkinter.CTkLabel(self, text="ime i prezime zamjene", fg_color="transparent")
    mylabel.grid(row=0, column=0, padx=(40, 0), pady=20)

    mycombo = customtkinter.CTkComboBox(self, values=popis_ucitelja, command = self.combobox_callback, width=300)
    mycombo.set("Odaberi ime")
    mycombo.grid(row=0, column=1, padx=60, pady=20)
    mycombo.grid_columnconfigure(0, weight=1)

    primijeni_btn = customtkinter.CTkButton(self, text="primijeni", fg_color="#110329", command=self.primijeni_btn_callback)
    primijeni_btn.grid(row=1, column=1, padx=5, pady=5)

  def combobox_callback(self, izbor):
    global ime_i_prezime_zamjene
    prezime_ime = izbor
    ime_i_prezime_zamjene = " ".join(prezime_ime.split()[::-1])

  def primijeni_btn_callback(self):
    update_context()
    render_document()


def update_context():
  global ime_i_prezime_zamjene
  global context
  context["ime_i_prezime_zamjene"] = ime_i_prezime_zamjene


def render_document():
  doc = DocxTemplate("word.docx")
  doc.render(context)
  doc.save(f"{ime_i_prezime_zamjene}.docx")


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("Zamii")

    self.geometry("600x500+300+100")
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=1)
    self.resizable(width=0, height=0)
    customtkinter.set_appearance_mode("system")

    self.zamjena_frame = ZamjenaFrame(self)
    self.zamjena_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new")


context = {}

zamii = App()
zamii.mainloop()