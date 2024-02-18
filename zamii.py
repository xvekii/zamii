import sqlite3
import customtkinter
from docxtpl import DocxTemplate

popis_ucitelja = []
popis_ucitelja_G = []

dani = list(range(1, 32))
dani_str = [str(dan) for dan in dani]

mjeseci = list(range(1, 13))
mjeseci_z_str = [str(mjesec) for mjesec in mjeseci]

db_connection = sqlite3.connect("ucitelji.db")
db = db_connection.cursor()

db.execute("SELECT prezime, ime FROM ucitelji ORDER BY prezime")
rows = db.fetchall()

for row in rows:
  puno_ime = " ".join(row)
  popis_ucitelja.append(puno_ime)

db.execute("SELECT prezime_G, ime_G FROM ucitelji_G ORDER BY prezime_G")
rows_G = db.fetchall()

for row_G in rows_G:
  puno_ime_G = " ".join(row_G)
  popis_ucitelja_G.append(puno_ime_G)

class ZamjenaFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    ime_prezime_zamjene_label = customtkinter.CTkLabel(self, text="ime i prezime zamjene", fg_color="transparent")
    ime_prezime_zamjene_label.grid(row=0, column=0, padx=(38, 0), pady=0)

    ime_prezime_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja, command=self.combobox_callback, 
                                                  state="readonly", width=300)
    ime_prezime_combo.set("odaberi ime i prezime")
    ime_prezime_combo.grid(row=0, column=1, padx=60, pady=10, columnspan=2)
    ime_prezime_combo.grid_columnconfigure(0, weight=1)

    radnog_vremena_label = customtkinter.CTkLabel(self, text="radnog vremena", fg_color="transparent")
    radnog_vremena_label.grid(row=1, column=0, padx=(75, 0), pady=10, sticky="w")

    self.radio_rad_vrem_var = customtkinter.StringVar(value=0)
    self.radnog_vremena_radio1 = customtkinter.CTkRadioButton(self, text="punog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="punog")
    self.radnog_vremena_radio1.grid(row=1, column=1, padx=(85, 0), pady=10, sticky="w")
    
    self.radnog_vremena_radio2 = customtkinter.CTkRadioButton(self, text="nepunog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="nepunog")
    self.radnog_vremena_radio2.grid(row=1, column=2, padx=(0, 60), pady=10)

    umjesto_label = customtkinter.CTkLabel(self, text="umjesto", fg_color="transparent")
    umjesto_label.grid(row=3, column=0, padx=(126, 0), pady=10)
    
    umjesto_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja_G, command=self.combobox_callback_G, 
                                              state="readonly", width=300)
    umjesto_combo.set("odaberi ime i prezime")
    umjesto_combo.grid(row=3, column=1, padx=60, pady=10, columnspan=2)

  def radiobtn_event(self):
    konačnog_radnog_vremena = self.radio_rad_vrem_var.get() 
    print(konačnog_radnog_vremena)
    context["radnog_vremena"] = konačnog_radnog_vremena

  
  def combobox_callback(self, izbor):
    global ime_i_prezime_zamjene
    prezime_ime = izbor
    split_prezime_ime = prezime_ime.split()
    ime_i_prezime_zamjene = " ".join([split_prezime_ime[-1]] + split_prezime_ime[:-1])
    print(ime_i_prezime_zamjene)


  def combobox_callback_G(self, izbor_G):
    global ime_i_prezime_zamijenjenog_G
    prezime_ime_G = izbor_G
    split_prezime_ime_G = prezime_ime_G.split()
    ime_i_prezime_zamijenjenog_G = " ".join([split_prezime_ime_G[-1]] + split_prezime_ime_G[:-1])
    print(ime_i_prezime_zamijenjenog_G)


class VrijemeZamjeneFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    nadnevak_zamjene_label = customtkinter.CTkLabel(self, text="nadnevak zamjene", fg_color="transparent")
    nadnevak_zamjene_label.grid(row=0, column=0, padx=(62, 0), pady=0)

    dan_zamjene_combo = customtkinter.CTkComboBox(self, values=dani_str, command=self.combo_dani_z_callback, 
                                                       state="readonly", width=120)
    dan_zamjene_combo.set("dan")
    dan_zamjene_combo.grid(row=0, column=1, padx=60, pady=10, columnspan=1)
    
    mjesec_zamjene_combo = customtkinter.CTkComboBox(self, values=mjeseci_z_str, command=self.combo_mjeseci_z_callback, 
                                                       state="readonly", width=120)
    mjesec_zamjene_combo.set("mjesec")
    mjesec_zamjene_combo.grid(row=0, column=2, padx=0, pady=10, columnspan=1)


  def combo_dani_z_callback(self, izbor):
    global dan_zamjene
    dan_zamjene = izbor
    context["dan_z"] = dan_zamjene
    print(dan_zamjene)

  def combo_mjeseci_z_callback(self, izbor):
    global mjesec_zamjene
    mjesec_zamjene = izbor
    context["mjesec_z"] = mjesec_zamjene
    print(mjesec_zamjene)


def primijeni_btn_callback():
  update_context()
  render_document()


def update_context():
  global ime_i_prezime_zamjene
  global ime_i_prezime_zamijenjenog_G
  global context
  context["ime_i_prezime_zamjene"] = ime_i_prezime_zamjene
  context["ime_i_prezime_zamijenjenog"] = ime_i_prezime_zamijenjenog_G
  
  spol_zaposlen_a = get_gender_zaposlen_a(ime_i_prezime_zamjene)
  print(spol_zaposlen_a)
  context["spol_zaposlen_a"] = spol_zaposlen_a


def get_gender_zaposlen_a(ime_i_prezime_zamjene):
  split_ime = ime_i_prezime_zamjene.split()
  ime = split_ime[0]
  prezime = " ".join(split_ime[1:])
  print(ime, prezime)
  
  db.execute("SELECT spol FROM ucitelji WHERE ime = ? AND prezime = ?", (ime, prezime))
  res = db.fetchone()
  
  if res is not None:
    spol = res[0]
    if spol == "m":
      return "zaposlen"
    elif spol == "ž":
      return "zaposlena"


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
    self.grid_rowconfigure(0, weight=0)
    self.resizable(width=0, height=0)
    customtkinter.set_appearance_mode("system")

    self.zamjena_frame = ZamjenaFrame(self)
    self.zamjena_frame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="new")

    self.vrijeme_zamjene_frame = VrijemeZamjeneFrame(self)
    self.vrijeme_zamjene_frame.grid(row=1, column=0, padx=10, pady=(15, 5), sticky="ew")
    
    primijeni_btn = customtkinter.CTkButton(self, text="primijeni", fg_color="#110329", command=primijeni_btn_callback)
    primijeni_btn.grid(row=2, column=0, padx=120, pady=5, sticky="e")

context = {}

zamii = App()
zamii.mainloop()