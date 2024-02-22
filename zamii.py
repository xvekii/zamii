import os
import sqlite3
import customtkinter
from docxtpl import DocxTemplate

popis_ucitelja = []
popis_ucitelja_G = []
popis_ucitelja_G_dict = {}

# Get and set the file path
file_dir = os.path.dirname(os.path.abspath(__file__))
db_name = "ucitelji.db"
db_path = os.path.join(file_dir, db_name)

db_connection = sqlite3.connect(db_path)
db = db_connection.cursor()

# Get teachers' names from db
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

db.execute("SELECT prezime_G, ime_G FROM ucitelji_G ORDER BY prezime_G")
for row in db.fetchall():
  prezime_ime_G = f"{row[0]} {row[1]}"
  popis_ucitelja_G_dict[prezime_ime_G] = (row[0], row[1])


dani = list(range(1, 32))
dani_str = [str(dan) for dan in dani]

mjeseci = list(range(1, 13))
mjeseci_z_str = [str(mjesec) for mjesec in mjeseci]

trajanje_sati_z = list(range(1, 6))
trajanje_sati_z_str = [str(sat) for sat in trajanje_sati_z]

šk_sati_z = list(range(1, 9))
šk_sat_z_str = [str(sat) for sat in šk_sati_z]

obrazl_textbox = None
klasa_textbox = None


class ZamjenaFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    ime_prezime_zamjene_label = customtkinter.CTkLabel(self, text="prezime i ime zamjene", fg_color="transparent")
    ime_prezime_zamjene_label.grid(row=0, column=0, padx=(38, 0), pady=0)

    ime_prezime_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja, command=self.combobox_callback, 
                                                  state="normal", button_hover_color=("plum"), width=300)
    ime_prezime_combo.set("odaberi prezime i ime")
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
                                              state="normal", button_hover_color=("plum"), width=300)
    umjesto_combo.set("odaberi prezime i ime")
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

    ime = ime_i_prezime_zamjene.split()[-1]
    prezime = " ".join(ime_i_prezime_zamjene.split()[:-1])

    print(ime, prezime)

    get_ime_ucitelja_D(prezime, ime)


  def combobox_callback_G(self, izbor_G):
    global ime_i_prezime_zamijenjenog_G
    prezime_ime_G = izbor_G
    split_prezime_ime_G = prezime_ime_G.split()
    ime_i_prezime_zamijenjenog_G = " ".join([split_prezime_ime_G[-1]] + split_prezime_ime_G[:-1])
    print(ime_i_prezime_zamijenjenog_G)

    prezime_ime_G_tuples = find_surname_name_G(prezime_ime_G)
    prezime_G = prezime_ime_G_tuples[0]
    ime_G = prezime_ime_G_tuples[1]
    get_radno_mjesto_zamijenjenog(prezime_G, ime_G)


def get_ime_ucitelja_D(prezime, ime):
  db.execute("SELECT ime_D, prezime_D FROM ucitelji_D WHERE id_ucitelja_D = ( \
             SELECT id_ucitelja_N FROM ucitelji WHERE ime = ? AND prezime = ?)", (prezime, ime))
  rows_D = db.fetchone()
  ime_D = rows_D[0]
  prez_D = rows_D[1] 
  ime_prez_D = ime_D + " " + prez_D
  print(ime_prez_D)
  context["ime_prez_z_D"] = ime_prez_D


def get_radno_mjesto_zamijenjenog(prezime_G, ime_G):
    db.execute("SELECT na_radnom_mjestu FROM radno_mjesto WHERE id_radnog_mjesta = ( \
               SELECT radno_mjesto FROM ucitelji WHERE id_ucitelja_N = ( \
               SELECT id_ucitelja_G FROM ucitelji_G \
               WHERE prezime_G = ? AND ime_G = ?))", (prezime_G, ime_G))
    rows_G = db.fetchone()
    radno_mj = rows_G[0]
    context["r_mj_zamijenj_G"] = radno_mj
    print(radno_mj)


def find_surname_name_G(prezime_ime_G):
  return popis_ucitelja_G_dict.get(prezime_ime_G)


class VrijemeZamjeneFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    nadnevak_zamjene_label = customtkinter.CTkLabel(self, text="nadnevak zamjene", fg_color="transparent")
    nadnevak_zamjene_label.grid(row=0, column=0, padx=(62, 0), pady=0)

    dan_zamjene_combo = customtkinter.CTkComboBox(self, values=dani_str, command=self.combo_dani_z_callback, 
                                                  state="normal", button_hover_color=("plum"), width=120)
    dan_zamjene_combo.set("dan")
    dan_zamjene_combo.grid(row=0, column=1, padx=60, pady=10, columnspan=1)
    
    mjesec_zamjene_combo = customtkinter.CTkComboBox(self, values=mjeseci_z_str, command=self.combo_mjeseci_z_callback, 
                                                    state="normal", button_hover_color=("plum"), width=120)
    mjesec_zamjene_combo.set("mjesec")
    mjesec_zamjene_combo.grid(row=0, column=2, padx=0, pady=10, columnspan=1)

    trajanje_zamjene_label = customtkinter.CTkLabel(self, text="trajanje zamjene", fg_color="transparent")
    trajanje_zamjene_label.grid(row=1, column=0, padx=(76, 0), pady=0)

    trajanje_zamjene_combo = customtkinter.CTkComboBox(self, values=trajanje_sati_z_str, 
                                                       command=self.combo_trajanje_sati_z_callback, state="normal", 
                                                       button_hover_color=("plum"), width=120)
    trajanje_zamjene_combo.grid(row=1, column=1, padx=0, pady=10, columnspan=1)
    trajanje_zamjene_combo.set("koliko sati")

    šk_sat_zamjene_label = customtkinter.CTkLabel(self, text="školski sat zamjene", fg_color="transparent")
    šk_sat_zamjene_label.grid(row=2, column=0, padx=(57, 0), pady=0)

    šk_sat_zamjene_combo = customtkinter.CTkComboBox(self, values=šk_sat_z_str, 
                                                       command=self.combo_šk_sat_z_callback, state="normal", 
                                                       button_hover_color=("plum"), width=120)
    šk_sat_zamjene_combo.grid(row=2, column=1, padx=0, pady=10, columnspan=1)
    šk_sat_zamjene_combo.set("koji sat")
  

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


  def combo_trajanje_sati_z_callback(self, izbor):
    trajanje_zamjene = izbor
    context["trajanje_zamjene"] = trajanje_zamjene
    set_sat_i(trajanje_zamjene)


  def combo_šk_sat_z_callback(self, izbor):
    šk_sat_z = izbor
    context["šk_sat_z"] = šk_sat_z


def set_sat_i(sati):
  if sati == "1":
    context["sat_i"] = "sat"
  elif sati == "5":
    context["sat_i"] = "sati"
  else:
    context["sat_i"] = "sata"


class ObrazloženjeFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    obrazl_label = customtkinter.CTkLabel(self, text="obrazloženje", fg_color="transparent")
    obrazl_label.grid(row=0, column=0, padx=(98, 0), pady=0)

    global obrazl_textbox
    obrazl_textbox = customtkinter.CTkTextbox(self, width=300, height=50, corner_radius=0, border_width=1, 
                                              wrap="word", border_color=("black"))
    obrazl_textbox.grid(row=0, column=1, padx=60, pady=(10, 10), sticky="e")
    
    nadnevak_naloga_label = customtkinter.CTkLabel(self, text="nadnevak naloga", fg_color="transparent")
    nadnevak_naloga_label.grid(row=1, column=0, padx=(72, 0), pady=(0, 10))

    dan_naloga_combo = customtkinter.CTkComboBox(self, values=dani_str, command=self.combo_dani_n_callback, 
                                                  state="normal", button_hover_color=("plum"), width=120)
    dan_naloga_combo.set("dan")
    dan_naloga_combo.grid(row=1, column=1, padx=(0, 182), pady=(0, 10))

    mjesec_naloga_combo = customtkinter.CTkComboBox(self, values=mjeseci_z_str, command=self.combo_mjeseci_n_callback, 
                                                    state="normal", button_hover_color=("plum"), width=120)
    mjesec_naloga_combo.set("mjesec")
    mjesec_naloga_combo.grid(row=1, column=1, padx=(180, 0), pady=(0, 10))

    klasa_label = customtkinter.CTkLabel(self, text="KLASA", fg_color="transparent")
    klasa_label.grid(row=2, column=0, padx=(132, 0), pady=(0, 10))

    global klasa_textbox
    klasa_textbox = customtkinter.CTkTextbox(self, width=120, height=10, corner_radius=0, border_width=1, 
                                            border_color=("black"))
    klasa_textbox.grid(row=2, column=1, padx=(0, 240), pady=(0, 10), sticky="e")
  
  
  def combo_dani_n_callback(self, izbor):
    dan_naloga = izbor
    context["dan_naloga"] = dan_naloga


  def combo_mjeseci_n_callback(self, izbor):
    mj_naloga = izbor
    context["mj_naloga"] = mj_naloga
  

def primijeni_btn_callback():
  get_obrazl_textbox()
  get_klasa_textbox()
  update_context()
  render_document()


def update_context():
  global ime_i_prezime_zamjene
  global ime_i_prezime_zamijenjenog_G
  global context
  context["ime_i_prezime_zamjene"] = ime_i_prezime_zamjene
  context["ime_i_prezime_zamijenjenog"] = ime_i_prezime_zamijenjenog_G
  
  spol_zaposlen_a = get_gender_zaposlen_a(ime_i_prezime_zamjene)
  set_gender(spol_zaposlen_a)
  print(spol_zaposlen_a)
  context["spol_zaposlen_a"] = spol_zaposlen_a
  

def set_gender(spol_zaposlen_a):
  if spol_zaposlen_a == "zaposlen":
    context["dužan_na"] = "dužan"
    context["radnik_ca"] = "Radnik"
    context["radniku_ci"] = "Radniku"
    context["sam_a"] = "sam"
  elif spol_zaposlen_a == "zaposlena":
    context["dužan_na"] = "dužna" 
    context["radnik_ca"] = "Radnica"
    context["radniku_ci"] = "Radnici"
    context["sam_a"] = "sama"
  

def get_obrazl_textbox():
  global obrazl_textbox
  obrazl_txt = obrazl_textbox.get("0.0", "end-1c")
  context["obrazl"] = obrazl_txt
  print(obrazl_txt)


def get_klasa_textbox():
  global klasa_textbox
  klasa_txt = klasa_textbox.get("0.0", "end-1c")
  context["klasa"] = klasa_txt
  print(klasa_txt)


def get_radno_mjesto(ime, prezime):
  db.execute("SELECT na_radnom_mjestu FROM radno_mjesto WHERE id_radnog_mjesta = \
             (SELECT radno_mjesto FROM ucitelji WHERE ime = ? AND prezime = ?)", (ime, prezime))
  res = db.fetchone()

  if res is not None:
    context["radno_mj"] = res[0]
    print(res[0])


def get_gender_zaposlen_a(ime_i_prezime_zamjene):
  split_ime = ime_i_prezime_zamjene.split()
  ime = split_ime[0]
  prezime = " ".join(split_ime[1:])
  print(ime, prezime)
  
  get_radno_mjesto(ime, prezime)
  
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

    self.geometry("600x550+300+100")
    self.grid_columnconfigure(0, weight=1)
    self.grid_rowconfigure(0, weight=0)
    self.resizable(width=0, height=0)
    customtkinter.set_appearance_mode("system")

    self.zamjena_frame = ZamjenaFrame(self)
    self.zamjena_frame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="new")

    self.vrijeme_zamjene_frame = VrijemeZamjeneFrame(self)
    self.vrijeme_zamjene_frame.grid(row=1, column=0, padx=10, pady=(15, 5), sticky="ew")
    
    self.obrazloženje_frame = ObrazloženjeFrame(self)
    self.obrazloženje_frame.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="ew")
    
    primijeni_btn = customtkinter.CTkButton(self, text="primijeni", fg_color="#110329", 
                                            hover_color=("#38A282"), command=primijeni_btn_callback)
    primijeni_btn.grid(row=3, column=0, padx=55, pady=5, sticky="e")

context = {}

zamii = App()
zamii.mainloop()