import os
import sqlite3
from tkinter import *
from tkinter import ttk
import customtkinter
from CTkMessagebox import CTkMessagebox
from PIL import ImageTk
from docxtpl import DocxTemplate

# For storing teacher names and surnames (Nominative and Genitive)
popis_ucitelja = []
popis_ucitelja_G = []
popis_ucitelja_N_dict = {}
popis_ucitelja_G_dict = {}

# Days and months lists
dani = list(range(1, 32))
dani_str = [str(dan) for dan in dani]
mjeseci = list(range(1, 13))
mjeseci_z_str = [str(mjesec) for mjesec in mjeseci]

# Number of classes 
trajanje_sati_z = list(range(1, 6))
trajanje_sati_z_str = [str(sat) for sat in trajanje_sati_z]

# Which classes
šk_sati_z = list(range(1, 9))
šk_sat_z_str = [str(sat) for sat in šk_sati_z]

obrazl_textbox = None
klasa_textbox = None

# For storing school class(es) the replacement is needed for
šk_sat_z_chckbxes = []
šk_sat_z_chckbxes_clean = []

# Name and surname of the replacement teacher
# Name and surname of the replaced teacher (Genitive)
ime_i_prezime_zamjene = ""
ime_i_prezime_zamijenjenog_G = ""

# Day of replacement
# Month of replacement
dan_zamjene = ""
mjesec_zamjene = ""

# Day of the overtime form
# Month of the overtime form
dan_naloga = ""
mj_naloga = ""

# For tracking of the state of consent for the overtime work: add/remove
izjava = False

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

# Get prezime_ime from ucitelji and store into a dictionary with prezime_ime_N key and surname, name tuples
db.execute("SELECT prezime, ime FROM ucitelji ORDER BY prezime")
for row in db.fetchall():
  prezime_ime_N = f"{row[0]} {row[1]}"
  popis_ucitelja_N_dict[prezime_ime_N] = (row[0], row[1])

# Get prezime_ime_G from ucitelji and store into a dictionary with prezime_ime_G key and surname, name tuples
db.execute("SELECT prezime_G, ime_G FROM ucitelji_G ORDER BY prezime_G")
for row in db.fetchall():
  prezime_ime_G = f"{row[0]} {row[1]}"
  popis_ucitelja_G_dict[prezime_ime_G] = (row[0], row[1])

# Replacement and replaced teachers frame
class ZamjenaFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    prezime_ime_zamjene_label = customtkinter.CTkLabel(self, text="Prezime i ime zamjene", fg_color="transparent")
    prezime_ime_zamjene_label.grid(row=0, column=0, padx=(42, 0), pady=(0, 0)
)
    global prezime_ime_combo
    prezime_ime_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja, command=self.combo_prezime_ime_callback, 
                                                  state="normal", button_hover_color=("plum"), width=300)
    prezime_ime_combo.set("odaberi prezime i ime")
    prezime_ime_combo.grid(row=0, column=1, padx=60, pady=(10, 5), columnspan=2)
    prezime_ime_combo.grid_columnconfigure(0, weight=1)

    radnog_vremena_label = customtkinter.CTkLabel(self, text="Radnog vremena", fg_color="transparent")
    radnog_vremena_label.grid(row=1, column=0, padx=(75, 0), pady=(10, 5), sticky="w")

    global radnog_vremena_radio1
    global radnog_vremena_radio2
    self.radio_rad_vrem_var = customtkinter.StringVar(value=0)
    radnog_vremena_radio1 = customtkinter.CTkRadioButton(self, text="punog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="punog")
    radnog_vremena_radio1.grid(row=1, column=1, padx=(85, 0), pady=(10, 5), sticky="w")
    
    radnog_vremena_radio2 = customtkinter.CTkRadioButton(self, text="nepunog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="nepunog")
    radnog_vremena_radio2.grid(row=1, column=2, padx=(0, 60), pady=(10, 5))

    umjesto_label = customtkinter.CTkLabel(self, text="Umjesto", fg_color="transparent")
    umjesto_label.grid(row=3, column=0, padx=(128, 0), pady=(10, 5))
    
    global umjesto_combo
    umjesto_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja_G, command=self.combo_umjesto_callback_G, 
                                              state="normal", button_hover_color=("plum"), width=300)
    umjesto_combo.set("odaberi prezime i ime")
    umjesto_combo.grid(row=3, column=1, padx=60, pady=(10, 10), columnspan=2)


  def radiobtn_event(self):
    konačnog_radnog_vremena = self.radio_rad_vrem_var.get() 
    print(konačnog_radnog_vremena)
    context["rad_vrem"] = konačnog_radnog_vremena
    

  # Get prezime_ime from db and store into tuples for easier ime i prezime identification and reversal
  # Use prezime_ime tuples for check and reverse to ime i prezime instead of splitting 
  def combo_prezime_ime_callback(self, izbor_N):
    global ime_i_prezime_zamjene
    global ime_N
    global prezime_N
    
    print(f"izbor 1: {izbor_N}")

    if izbor_N == "":
      unesi_prezime_ime_alert()
      return

    prezime_ime_N = izbor_N
    prezime_ime_N_tuples = find_surname_name_N(prezime_ime_N)
    prezime_N = prezime_ime_N_tuples[0]
    ime_N = prezime_ime_N_tuples[1]
    ime_i_prezime_zamjene = " ".join([ime_N, prezime_N])
    
    print(ime_N, prezime_N)

    get_ime_ucitelja_D(prezime_N, ime_N)
    # prezime_ime_N = ""
    # prezime_N = ""
    # ime_N = ""
    

  # Use prezime_ime tuples for check and reverse to ime i prezime instead of splitting 
  def combo_umjesto_callback_G(self, izbor_G):
    global ime_i_prezime_zamijenjenog_G
    prezime_ime_G = izbor_G
    
    prezime_ime_G_tuples = find_surname_name_G(prezime_ime_G)
    prezime_G = prezime_ime_G_tuples[0]
    ime_G = prezime_ime_G_tuples[1]
    ime_i_prezime_zamijenjenog_G = " ".join([ime_G, prezime_G])
    print(ime_i_prezime_zamijenjenog_G)

    get_radno_mjesto_zamijenjenog(prezime_G, ime_G)


def find_surname_name_N(prezime_ime_N):
  return popis_ucitelja_N_dict.get(prezime_ime_N)


def find_surname_name_G(prezime_ime_G):
  return popis_ucitelja_G_dict.get(prezime_ime_G)


# Get the name of the teacher in Dative (surname, name)
def get_ime_ucitelja_D(prezime, ime):
  db.execute("SELECT ime_D, prezime_D FROM ucitelji_D WHERE id_ucitelja_D = ( \
             SELECT id_ucitelja_N FROM ucitelji WHERE prezime = ? AND ime = ?)", (prezime, ime))
  rows_D = db.fetchone()
  ime_D = rows_D[0]
  prez_D = rows_D[1] 
  ime_prez_D = " ".join([ime_D, prez_D])
  print(ime_prez_D)
  context["ime_prez_z_D"] = ime_prez_D

# Get the working position of the teacher in Genitive
def get_radno_mjesto_zamijenjenog(prezime_G, ime_G):
    db.execute("SELECT na_radnom_mjestu FROM radno_mjesto WHERE id_radnog_mjesta = ( \
               SELECT radno_mjesto FROM ucitelji WHERE id_ucitelja_N = ( \
               SELECT id_ucitelja_G FROM ucitelji_G \
               WHERE prezime_G = ? AND ime_G = ?))", (prezime_G, ime_G))
    rows_G = db.fetchone()
    radno_mj = rows_G[0]
    context["r_mj_zamijenj_G"] = radno_mj
    print(radno_mj)

# Time of replacement frame
class VrijemeZamjeneFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)

    nadnevak_zamjene_label = customtkinter.CTkLabel(self, text="Nadnevak zamjene", fg_color="transparent")
    nadnevak_zamjene_label.grid(row=0, column=0, padx=(62, 0), pady=0)

    dan_zamjene_combo = customtkinter.CTkComboBox(self, values=dani_str, command=self.combo_dani_z_callback, 
                                                  state="normal", button_hover_color=("plum"), width=120)
    dan_zamjene_combo.set("dan")
    dan_zamjene_combo.grid(row=0, column=1, padx=60, pady=10, columnspan=1)
    
    mjesec_zamjene_combo = customtkinter.CTkComboBox(self, values=mjeseci_z_str, command=self.combo_mjeseci_z_callback, 
                                                    state="normal", button_hover_color=("plum"), width=120)
    mjesec_zamjene_combo.set("mjesec")
    mjesec_zamjene_combo.grid(row=0, column=2, padx=0, pady=10, columnspan=1)

    trajanje_zamjene_label = customtkinter.CTkLabel(self, text="Trajanje zamjene", fg_color="transparent")
    trajanje_zamjene_label.grid(row=1, column=0, padx=(76, 0), pady=0)

    global trajanje_zamjene_combo
    trajanje_zamjene_combo = customtkinter.CTkComboBox(self, values=trajanje_sati_z_str, 
                                                       command=self.combo_trajanje_sati_z_callback, state="normal", 
                                                       button_hover_color=("plum"), width=120)
    trajanje_zamjene_combo.grid(row=1, column=1, padx=0, pady=10, columnspan=1)
    trajanje_zamjene_combo.set("koliko sati")

    šk_sat_zamjene_label = customtkinter.CTkLabel(self, text="Školski sat zamjene", fg_color="transparent")
    šk_sat_zamjene_label.grid(row=2, column=0, padx=(60, 0), pady=(10, 0))

    # šk_sat_zamjene checkboxes - first 4, first column
    global šk_sat_zamjene_checkbox1
    global šk_sat_chk_var1
    šk_sat_chk_var1 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox1 = customtkinter.CTkCheckBox(self, text="1. sat", command=self.get_chkbox1_callback,
                                                        variable=šk_sat_chk_var1, onvalue="1.")
    šk_sat_zamjene_checkbox1.grid(row=2, column=1, padx=(0, 20), pady=(10, 0))

    global šk_sat_zamjene_checkbox2
    global šk_sat_chk_var2
    šk_sat_chk_var2 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox2 = customtkinter.CTkCheckBox(self, text="2. sat", command=self.get_chkbox2_callback,
                                                        variable=šk_sat_chk_var2, onvalue="2.")
    šk_sat_zamjene_checkbox2.grid(row=3, column=1, padx=(0, 20), pady=(10, 0))

    global šk_sat_zamjene_checkbox3
    global šk_sat_chk_var3
    šk_sat_chk_var3 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox3 = customtkinter.CTkCheckBox(self, text="3. sat", command=self.get_chkbox3_callback,
                                                        variable=šk_sat_chk_var3, onvalue="3.")
    šk_sat_zamjene_checkbox3.grid(row=4, column=1, padx=(0, 20), pady=(10, 0))
    
    global šk_sat_zamjene_checkbox4
    global šk_sat_chk_var4
    šk_sat_chk_var4 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox4 = customtkinter.CTkCheckBox(self, text="4. sat", command=self.get_chkbox4_callback,
                                                        variable=šk_sat_chk_var4, onvalue="4.")
    šk_sat_zamjene_checkbox4.grid(row=5, column=1, padx=(0, 20), pady=(10, 10))
    
    # šk_sat_zamjene checkboxes - second 4, second column
    global šk_sat_zamjene_checkbox5
    global šk_sat_chk_var5
    šk_sat_chk_var5 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox5 = customtkinter.CTkCheckBox(self, text="5. sat", command=self.get_chkbox5_callback,
                                                        variable=šk_sat_chk_var5, onvalue="5.")
    šk_sat_zamjene_checkbox5.grid(row=2, column=2, padx=(0, 20), pady=(10, 0))
    
    global šk_sat_zamjene_checkbox6
    global šk_sat_chk_var6
    šk_sat_chk_var6 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox6 = customtkinter.CTkCheckBox(self, text="6. sat", command=self.get_chkbox6_callback,
                                                        variable=šk_sat_chk_var6, onvalue="6.")
    šk_sat_zamjene_checkbox6.grid(row=3, column=2, padx=(0, 20), pady=(10, 0))
    
    global šk_sat_zamjene_checkbox7
    global šk_sat_chk_var7
    šk_sat_chk_var7 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox7 = customtkinter.CTkCheckBox(self, text="7. sat", command=self.get_chkbox7_callback,
                                                        variable=šk_sat_chk_var7, onvalue="7.")
    šk_sat_zamjene_checkbox7.grid(row=4, column=2, padx=(0, 20), pady=(10, 0))
    
    global šk_sat_zamjene_checkbox8
    global šk_sat_chk_var8
    šk_sat_chk_var8 = customtkinter.StringVar(value="0")
    šk_sat_zamjene_checkbox8 = customtkinter.CTkCheckBox(self, text="8. sat", command=self.get_chkbox8_callback,
                                                        variable=šk_sat_chk_var8, onvalue="8.")
    šk_sat_zamjene_checkbox8.grid(row=5, column=2, padx=(0, 20), pady=(10, 10))


  def get_chkbox1_callback(self):
    izbor = šk_sat_chk_var1.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check1: {šk_sat_z_chckbxes}")


  def get_chkbox2_callback(self):
    izbor = šk_sat_chk_var2.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check2: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox3_callback(self):
    izbor = šk_sat_chk_var3.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check3: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox4_callback(self):
    izbor = šk_sat_chk_var4.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check4: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox5_callback(self):
    izbor = šk_sat_chk_var5.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check5: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox6_callback(self):
    izbor = šk_sat_chk_var6.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check6: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox7_callback(self):
    izbor = šk_sat_chk_var7.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check7: {šk_sat_z_chckbxes}")
  
  
  def get_chkbox8_callback(self):
    izbor = šk_sat_chk_var8.get()
    šk_sat_z_chckbxes.append(izbor)
    print(f"check8: {šk_sat_z_chckbxes}")

  
  def combo_dani_z_callback(self, izbor):
    global dan_zamjene
    dan_zamjene = izbor
    

  def combo_mjeseci_z_callback(self, izbor):
    global mjesec_zamjene
    mjesec_zamjene = izbor


  def combo_trajanje_sati_z_callback(self, izbor):
    trajanje_zamjene = izbor
    context["trajanje_zamjene"] = trajanje_zamjene
    print(f"trajanje zamjene: {context["trajanje_zamjene"]}")
    set_sat_i(trajanje_zamjene)


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

    obrazl_label = customtkinter.CTkLabel(self, text="Obrazloženje", fg_color="transparent")
    obrazl_label.grid(row=0, column=0, padx=(98, 0), pady=0)

    global obrazl_textbox
    obrazl_textbox = customtkinter.CTkTextbox(self, width=300, height=40, corner_radius=0, border_width=1, 
                                              wrap="word", border_color=("black"))
    obrazl_textbox.grid(row=0, column=1, padx=60, pady=(10, 5), sticky="e")
    
    očisti_btn = customtkinter.CTkButton(self, text="Očisti", width=56, fg_color="#6C757D", command=clear_obrazl_textbox_callback)
    očisti_btn.grid(row=1, column=1, padx=60, pady=(0, 20), sticky="e")

    nadnevak_naloga_label = customtkinter.CTkLabel(self, text="Nadnevak naloga", fg_color="transparent")
    nadnevak_naloga_label.grid(row=2, column=0, padx=(72, 0), pady=(0, 10))

    dan_naloga_combo = customtkinter.CTkComboBox(self, values=dani_str, command=self.combo_dani_n_callback, 
                                                  state="normal", button_hover_color=("plum"), width=120)
    dan_naloga_combo.set("dan")
    dan_naloga_combo.grid(row=2, column=1, padx=(0, 182), pady=(0, 10))

    mjesec_naloga_combo = customtkinter.CTkComboBox(self, values=mjeseci_z_str, command=self.combo_mjeseci_n_callback, 
                                                    state="normal", button_hover_color=("plum"), width=120)
    mjesec_naloga_combo.set("mjesec")
    mjesec_naloga_combo.grid(row=2, column=1, padx=(180, 0), pady=(0, 10))

    klasa_label = customtkinter.CTkLabel(self, text="KLASA", fg_color="transparent")
    klasa_label.grid(row=3, column=0, padx=(132, 0), pady=(10, 10))

    global klasa_textbox
    klasa_textbox = customtkinter.CTkTextbox(self, width=120, height=10, corner_radius=0, border_width=1, 
                                            border_color=("black"))
    klasa_textbox.grid(row=3, column=1, padx=(0, 240), pady=(10, 10), sticky="e")
  
  
  def combo_dani_n_callback(self, izbor):
    global dan_naloga
    dan_naloga = izbor


  def combo_mjeseci_n_callback(self, izbor):
    global mj_naloga
    mj_naloga = izbor
  

def primijeni_btn_callback():
  check_names_comboboxes()
  update_obrazl_textboxes()
  
  update_context()
  render_document()
  clear_widgets()

  ukloni_izjavu()
  clear_context()
  
  clear_names_variables()
  
  # Print for debugging
  print_var_values()
  

def check_names_comboboxes():
  check_prezime_ime_combo_selection()
  check_umjesto_prezime_ime_combo_selection()


def update_obrazl_textboxes():
  get_obrazl_textbox()
  get_klasa_textbox()


def clear_widgets():
  deselect_chkboxes()
  clear_prezime_ime_combobox()
  clear_radnog_vremena_radio_btns()
  clear_combo_umjesto_callback_G()
  clear_trajanje_zamjene_combo()


def clear_names_variables():
  clear_ime_i_prezime_zamjene()
  clear_ime_i_prezime_zamijenjenog_G()


def print_var_values(): 
  print(f"ime i prezime fin: {ime_i_prezime_zamjene}")
  print(f"context fin: {context}")
  print(f"ime_N fin: {ime_N}")
  print(f"dan zamjene: {dan_zamjene}")
  print(f"mjesec zamjene: {mjesec_zamjene}")


def clear_prezime_ime_combobox():
  prezime_ime_combo.set("odaberi prezime i ime")


def clear_radnog_vremena_radio_btns():
  global radnog_vremena_radio1
  global radnog_vremena_radio2
  radnog_vremena_radio1.deselect()
  radnog_vremena_radio2.deselect()


def clear_combo_umjesto_callback_G():
  umjesto_combo.set("odaberi prezime i ime")
  

def clear_ime_i_prezime_zamjene():
  global ime_i_prezime_zamjene 
  ime_i_prezime_zamjene = ""
  global prezime_N
  global ime_N
  prezime_N = ""
  ime_N = ""


def clear_ime_i_prezime_zamijenjenog_G():
  global ime_i_prezime_zamijenjenog_G
  ime_i_prezime_zamijenjenog_G = ""


def clear_trajanje_zamjene_combo():
  global trajanje_zamjene_combo
  trajanje_zamjene_combo.set("koliko sati")
  

def clear_context():
  context.clear()


def deselect_chkboxes():
  šk_sat_zamjene_checkbox1.deselect()
  šk_sat_zamjene_checkbox2.deselect()
  šk_sat_zamjene_checkbox3.deselect()
  šk_sat_zamjene_checkbox4.deselect()
  šk_sat_zamjene_checkbox5.deselect()
  šk_sat_zamjene_checkbox6.deselect()
  šk_sat_zamjene_checkbox7.deselect()
  šk_sat_zamjene_checkbox8.deselect()
  šk_sat_z_chckbxes_clean.clear()
  šk_sat_z_chckbxes.clear()
  print(f"chkbxes_sati: {šk_sat_z_chckbxes_clean}")


def clear_obrazl_textbox_callback():
  obrazl_textbox.delete("0.0", "end-1c")


# Remove eventual "0"s and unchecked values from the list if user unchecks checkbox
def clean_šk_sat_chckbxes():
  i = 0
  while i < len(šk_sat_z_chckbxes):
    if šk_sat_z_chckbxes[i] != "0":
      šk_sat_z_chckbxes_clean.append(šk_sat_z_chckbxes[i])
    elif i > 0:
      šk_sat_z_chckbxes_clean.pop()
    i += 1


def update_šk_sat_checkboxes():
  clean_šk_sat_chckbxes()
  concat_str = ", ".join(šk_sat_z_chckbxes_clean)
  context["šk_sat_z"] = concat_str
  concat_str = None
  
  print(f"sati: {concat_str}")
  

def check_prezime_ime_combo_selection():
  if ime_i_prezime_zamjene == "":
    unesi_prezime_ime_alert()  


def check_umjesto_prezime_ime_combo_selection():
  if ime_i_prezime_zamijenjenog_G == "":
    unesi_umjesto_prezime_ime_alert()


def update_context():
  global ime_i_prezime_zamjene
  global ime_i_prezime_zamijenjenog_G
  global context
  global izjava

  context["ime_i_prezime_zamjene"] = ime_i_prezime_zamjene
  context["zamij_G"] = ime_i_prezime_zamijenjenog_G
  context["dan_z"] = dan_zamjene
  context["mjesec_z"] = mjesec_zamjene
  context["dan_naloga"] = dan_naloga
  context["mj_naloga"] = mj_naloga
  
  spol_zaposlen_a = get_gender_zaposlen_a(ime_N, prezime_N)
 
  if izjava == True: 
    primijeni_izjavu(spol_zaposlen_a)

  set_gender(spol_zaposlen_a)
  print(spol_zaposlen_a)
  context["spol_zaposlen_a"] = spol_zaposlen_a
  update_šk_sat_checkboxes()
  

def unesi_prezime_ime_alert():
  CTkMessagebox(title="Pogreška!", message="Odaberi prezime i ime zamjene!", icon="warning", bg_color="orange",
                  button_color="black", sound=True)
  

def unesi_umjesto_prezime_ime_alert():
  CTkMessagebox(title="Pogreška!", message="Odaberi umjesto koga je zamjena!", icon="warning", bg_color="orange",
                  button_color="black", sound=True)


def set_gender(spol_zaposlen_a):
  if spol_zaposlen_a == "zaposlen":
    context["dužan_na"] = "dužan"
    context["radnik_ca"] = "Radnik"
    context["rdn"] = "Radniku"
    context["r_s"] = "sam"
  elif spol_zaposlen_a == "zaposlena":
    context["dužan_na"] = "dužna" 
    context["radnik_ca"] = "Radnica"
    context["rdn"] = "Radnici"
    context["r_s"] = "sama"
  

def dodaj_izjavu_btn_callback():
  global izjava
  izjava = True


def ukloni_izjavu():
  global izjava
  izjava = False


def primijeni_izjavu(spol_zaposlen_a):
  gender = spol_zaposlen_a
  suglasan_na = None
  if gender == "zaposlen": 
    suglasan_na = "suglasan"
  elif gender == "zaposlena":
    suglasan_na = "suglasna"
  context["izjava"] = f"Izjavljujem da sam {suglasan_na} na gore navedeni prekovremeni rad _____________________"
  context["potpis"] = "potpis"
  print(suglasan_na)



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

# Refactor to use dictionary of tuples with prezime_ime
def get_gender_zaposlen_a(ime_N, prezime_N):
  print(ime_N, prezime_N)
  
  get_radno_mjesto(ime_N, prezime_N)
  
  db.execute("SELECT spol FROM ucitelji WHERE ime = ? AND prezime = ?", (ime_N, prezime_N))
  res = db.fetchone()
  
  if res is not None:
    spol = res[0]
    if spol == "m":
      return "zaposlen"
    elif spol == "ž":
      return "zaposlena"


def generate_unique_file_name(file_name):
  base, ext = os.path.splitext(file_name)
  counter = 1
  new_filename = file_name
  while os.path.exists(new_filename):
    new_filename = f"{base}({counter}){ext}"
    counter += 1
  return new_filename


def render_document():
  doc = DocxTemplate("word.docx")
  doc.render(context)
  file_name = f"{ime_i_prezime_zamjene}.docx"
  new_file_name = generate_unique_file_name(file_name)
  doc.save(new_file_name)
  print(f"Naslov dokumenta (ime i pr.) {ime_i_prezime_zamjene}")


class BazaToplevelWindow(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.title("Baza podataka")

    self.geometry("935x605+300+100")
    self.grid_columnconfigure(3, weight=1)
    self.wm_transient(zamii)

    self.baza_frame = BazaFrame(self)
    self.baza_frame.grid(row=0, column=0, padx=(15, 15), pady=(10, 15), sticky="new")

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview", 
                  background="D3D3D3",
                  foreground="black",
                  rowheight=25,
                  fieldbackground="D3D3D3",
                  font=(None, 13))
    style.configure("Treeview.Heading", font=(None, 13))
    
    style.map("Treeview", background=[("selected", "#4a4e69")])

    baza_scroll = Scrollbar(self.baza_frame)
    baza_scroll.pack(side=RIGHT, fill=Y)

    self.baza_tree = ttk.Treeview(self.baza_frame, yscrollcommand=baza_scroll.set, selectmode="extended")
    self.baza_tree.pack(fill="both", expand=True)

    baza_scroll.config(command=self.baza_tree.yview)

    self.baza_tree["columns"] = ("ID", "Radno mjesto", "Na radnom mjestu", "Prezime", "Ime", "Spol")
    self.baza_tree.column("#0", stretch=NO, width=0)
    self.baza_tree.column("ID", anchor=CENTER, width=40)
    self.baza_tree.column("Radno mjesto", anchor=CENTER, width=120)
    self.baza_tree.column("Na radnom mjestu", anchor=W, width=350)
    self.baza_tree.column("Prezime", anchor=W, width=200)
    self.baza_tree.column("Ime", anchor=W, width=140)
    self.baza_tree.column("Spol", anchor=CENTER, width=40)

    self.baza_tree.heading("#0", text="", anchor=W)
    self.baza_tree.heading("ID", text="ID", anchor=CENTER)
    self.baza_tree.heading("Radno mjesto", text="Radno mjesto", anchor=CENTER)
    self.baza_tree.heading("Na radnom mjestu", text="Na radnom mjestu", anchor=W)
    self.baza_tree.heading("Prezime", text="Prezime", anchor=W)
    self.baza_tree.heading("Ime", text="Ime", anchor=W)
    self.baza_tree.heading("Spol", text="Spol", anchor=CENTER)

    self.baza_tree.tag_configure("oddrow", background="#FBFBFB")
    self.baza_tree.tag_configure("evenrow", background="#f2e9e4")
  
    # Input forms
    self.obrasci_frame = LabelFrame(self, text="Obrasci za unos")
    self.obrasci_frame.grid(row=1, column=0, padx=(15, 15), pady=(0, 10), sticky="ew")
  
    self.ID_label = customtkinter.CTkLabel(self.obrasci_frame, text="ID")
    self.ID_label.grid(row=1, column=0, padx=(10, 15), pady=10)

    self.ID_entry = customtkinter.CTkEntry(self.obrasci_frame, width=35)
    self.ID_entry.grid(row=1, column=1, padx=(5, 15), pady=10)

    self.radno_mjesto_label = customtkinter.CTkLabel(self.obrasci_frame, text="Radno mjesto")
    self.radno_mjesto_label.grid(row=1, column=2, padx=(5, 15), pady=10)

    self.radno_mjesto_entry = customtkinter.CTkEntry(self.obrasci_frame, width=35)
    self.radno_mjesto_entry.grid(row=1, column=3, padx=(5, 15), pady=10)

    self.na_radnom_mjestu_label = customtkinter.CTkLabel(self.obrasci_frame, text="Na radnom mjestu")
    self.na_radnom_mjestu_label.grid(row=1, column=4, padx=(5, 15), pady=10)

    self.na_radnom_mjestu_entry = customtkinter.CTkEntry(self.obrasci_frame, width=320)
    self.na_radnom_mjestu_entry.grid(row=1, column=5, padx=(5, 15), pady=10)

    # Input forms1
    self.obrasci_frame1 = LabelFrame(self, text="")
    self.obrasci_frame1.grid(row=2, column=0, padx=(15, 15), pady=(0, 10), sticky="ew")
    
    self.prezime_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Prezime")
    self.prezime_label.grid(row=2, column=4, padx=(5, 15), pady=10)
    
    self.prezime_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=220)
    self.prezime_entry.grid(row=2, column=5, padx=(5, 15), pady=10)
    
    self.ime_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Ime")
    self.ime_label.grid(row=2, column=6, padx=(5, 15), pady=10)
    
    self.ime_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=200)
    self.ime_entry.grid(row=2, column=7, padx=(5, 15), pady=10)
    
    self.spol_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Spol")
    self.spol_label.grid(row=2, column=8, padx=(5, 15), pady=10)

    self.spol_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=26)
    self.spol_entry.grid(row=2, column=9, padx=(5, 15), pady=10)

    self.prezime_ime_G_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Prezime G")
    self.prezime_ime_G_label.grid(row=3, column=4, padx=(5, 15), pady=10)

    self.prezime_ime_G_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=220)
    self.prezime_ime_G_entry.grid(row=3, column=5, padx=(5, 15), pady=10)

    self.ime_G_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Ime G")
    self.ime_G_label.grid(row=3, column=6, padx=(5, 15), pady=10)

    self.ime_G_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=200)
    self.ime_G_entry.grid(row=3, column=7, padx=(5, 15), pady=10)

    self.prezime_ime_D_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Prezime D")
    self.prezime_ime_D_label.grid(row=4, column=4, padx=(5, 15), pady=(10, 10))

    self.prezime_ime_D_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=220)
    self.prezime_ime_D_entry.grid(row=4, column=5, padx=(5, 15), pady=(10, 10))

    self.ime_D_label = customtkinter.CTkLabel(self.obrasci_frame1, text="Ime D")
    self.ime_D_label.grid(row=4, column=6, padx=(5, 15), pady=(10, 10))

    self.ime_D_entry = customtkinter.CTkEntry(self.obrasci_frame1, width=200)
    self.ime_D_entry.grid(row=4, column=7, padx=(5, 15), pady=(10, 10))

    # Buttons
    self.naredbe_frame = LabelFrame(self, text="Naredbe", width=900)
    self.naredbe_frame.grid(row=3, column=0, padx=(15, 15), pady=(0, 0), sticky="ew")

    self.izmijeni_unos_btn = customtkinter.CTkButton(self.naredbe_frame, text="Izmijeni unos", fg_color="#4a4e69",
                                                     command=self.izmijeni_unos)
    self.izmijeni_unos_btn.grid(row=1, column=0, padx=(10, 15), pady=10)
    
    self.dodaj_unos_btn = customtkinter.CTkButton(self.naredbe_frame, text="Dodaj unos", fg_color="#4a4e69")
    self.dodaj_unos_btn.grid(row=1, column=1, padx=(5, 15), pady=10)

    self.izbriši_unos_btn = customtkinter.CTkButton(self.naredbe_frame, text="Izbriši unos", fg_color="#4a4e69")
    self.izbriši_unos_btn.grid(row=1, column=2, padx=(5, 15), pady=10)
    
    self.popis_radnih_mj_btn = customtkinter.CTkButton(self.naredbe_frame, text="Popis radnih mjesta", fg_color="#4a4e69",
                                                       command=self.otvori_popis_radnih_mj_toplevel_window)
    self.popis_radnih_mj_btn.grid(row=1, column=3, padx=(5, 15), pady=10)

    self.prikaži_G_i_D_btn = customtkinter.CTkButton(self.naredbe_frame, text="Prikaži G i D", fg_color="#4a4e69",
                                                       width=110, command=self.otvori_G_i_D_toplevel_window)
    self.prikaži_G_i_D_btn.grid(row=1, column=4, padx=(5, 15), pady=10)
    
    self.očisti_obrasce_btn = customtkinter.CTkButton(self.naredbe_frame, text="Očisti obrasce", fg_color="#4a4e69",
                                                      width=110, command=self.očisti_obrasce)
    self.očisti_obrasce_btn.grid(row=1, column=5, padx=(5, 5), pady=10)

    self.baza_tree.bind("<ButtonRelease-1>", self.select_db_data)
    
    self.popis_imena_N_i_G_toplevel_window = None
    self.popis_radnih_mj_toplevel_window = None

    get_db_data(self.baza_tree)
  

  def otvori_popis_radnih_mj_toplevel_window(self):
    if self.popis_radnih_mj_toplevel_window is None or not self.popis_radnih_mj_toplevel_window.winfo_exists():
      self.popis_radnih_mj_toplevel_window = PopisRadnihMjToplevelWindow()
    else: 
      self.popis_radnih_mj_toplevel_window.focus()


  def otvori_G_i_D_toplevel_window(self):
    if self.popis_imena_N_i_G_toplevel_window is None or not self.popis_imena_N_i_G_toplevel_window.winfo_exists():
      self.popis_imena_N_i_G_toplevel_window = PopisImenaGiDToplevelWindow()
    else:
      self.popis_imena_N_i_G_toplevel_window.focus()


  def očisti_obrasce(self):
    self.ID_entry.delete(0, END)
    self.radno_mjesto_entry.delete(0, END)
    self.na_radnom_mjestu_entry.delete(0, END)
    self.prezime_entry.delete(0, END)
    self.prezime_ime_G_entry.delete(0, END)
    self.ime_G_entry.delete(0, END)
    self.prezime_ime_D_entry.delete(0, END)
    self.ime_D_entry.delete(0, END)
    self.ime_entry.delete(0, END)
    self.spol_entry.delete(0, END)


  def select_db_data(self, event):
    self.ID_entry.delete(0, END)
    self.radno_mjesto_entry.delete(0, END)
    self.na_radnom_mjestu_entry.delete(0, END)
    self.prezime_entry.delete(0, END)
    self.ime_entry.delete(0, END)
    self.spol_entry.delete(0, END)
    self.prezime_ime_G_entry.delete(0, END)
    self.ime_G_entry.delete(0, END)
    self.prezime_ime_D_entry.delete(0, END)
    self.ime_D_entry.delete(0, END)

    selected = self.baza_tree.focus()
    values = self.baza_tree.item(selected, "values")

    self.ID_entry.insert(0, values[0])
    self.radno_mjesto_entry.insert(0, values[1])
    self.na_radnom_mjestu_entry.insert(0, values[2])
    self.prezime_entry.insert(0, values[3])
    self.ime_entry.insert(0, values[4])
    self.spol_entry.insert(0, values[5])

    db_connection = sqlite3.connect(db_path)
    db = db_connection.cursor()

    db.execute("SELECT prezime_G, ime_G FROM ucitelji_G WHERE id_ucitelja_G = ?", (values[0],))
    rows = db.fetchall()
    self.prezime_ime_G_entry.insert(0, rows[0][0])
    self.ime_G_entry.insert(0, rows[0][1])

    db.execute("SELECT prezime_D, ime_D FROM ucitelji_D WHERE id_ucitelja_D = ?", (values[0],))
    rows_D = db.fetchall()
    self.prezime_ime_D_entry.insert(0, rows_D[0][0])
    self.ime_D_entry.insert(0, rows_D[0][1])


  def izmijeni_unos(self):
    selected = self.baza_tree.focus()
    if not selected:
      return
    
    self.baza_tree.item(selected, text="", values=(self.ID_entry.get(), self.radno_mjesto_entry.get(), self.na_radnom_mjestu_entry.get(),
                                                   self.prezime_entry.get(), self.ime_entry.get(), self.spol_entry.get()))
    ID = self.ID_entry.get()
    radno_mjesto = self.radno_mjesto_entry.get()
    ime = self.ime_entry.get()
    prezime = self.prezime_entry.get()
    ime_G = self.ime_G_entry.get()
    prezime_G = self.prezime_ime_G_entry.get()
    ime_D = self.ime_D_entry.get()
    prezime_D = self.prezime_ime_D_entry.get()

    if not ime or not prezime or not ime_G or not ID:
      return

    try:
      db_connection = sqlite3.connect(db_path)
      db = db_connection.cursor()

      db.execute("UPDATE ucitelji SET ime = ?, prezime = ?, radno_mjesto = ? WHERE id_ucitelja_N = ?", (ime, prezime, radno_mjesto, ID))
      db.execute("UPDATE ucitelji_G SET ime_G = ?, prezime_G = ? WHERE id_ucitelja_G = ?", (ime_G, prezime_G, ID))
      db.execute("UPDATE ucitelji_D SET ime_D = ?, prezime_D = ? WHERE id_ucitelja_D = ?", (ime_D, prezime_D, ID))

      db_connection.commit()
      db_connection.close()
    except Exception as e:
      print("Error updating db ", e)

    self.ID_entry.delete(0, END)
    self.radno_mjesto_entry.delete(0, END)
    self.na_radnom_mjestu_entry.delete(0, END)
    self.prezime_entry.delete(0, END)
    self.ime_entry.delete(0, END)
    self.prezime_ime_G_entry.delete(0, END)
    self.ime_G_entry.delete(0, END)
    self.prezime_ime_D_entry.delete(0, END)
    self.ime_D_entry.delete(0, END)
    self.spol_entry.delete(0, END)
    

class PopisRadnihMjToplevelWindow(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.title("Popis radnih mjesta")

    self.geometry("613x468+300+100")
    self.grid_columnconfigure(3, weight=1)
    self.wm_transient(zamii.baza_toplevel_window)
    
    self.radna_mj_frame = RadnaMjFrame(self)
    self.radna_mj_frame.grid(row=0, column=0, padx=(15, 15), pady=(10, 15), sticky="new")

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview", 
                  background="D3D3D3",
                  foreground="black",
                  rowheight=25,
                  fieldbackground="D3D3D3",
                  font=(None, 13))
    style.configure("Treeview.Heading", font=(None, 13))

    style.map("Treeview", background=[("selected", "#4a4e69")])

    radna_mj_scroll = Scrollbar(self.radna_mj_frame)
    radna_mj_scroll.pack(side=RIGHT, fill=Y)

    self.radna_mj_tree = ttk.Treeview(self.radna_mj_frame, yscrollcommand=radna_mj_scroll.set, selectmode="extended")
    self.radna_mj_tree.pack(fill="both", expand=True)

    radna_mj_scroll.config(command=self.radna_mj_tree.yview)

    self.radna_mj_tree["columns"] = ("ID radnog mjesta", "Na radnom mjestu (G)")
    self.radna_mj_tree.column("#0", stretch=NO, width=0)
    self.radna_mj_tree.column("ID radnog mjesta", anchor=CENTER, width=160)
    self.radna_mj_tree.column("Na radnom mjestu (G)", anchor=W, width=400)

    self.radna_mj_tree.heading("#0", text="", anchor=W)
    self.radna_mj_tree.heading("ID radnog mjesta", text="ID radnog mjesta", anchor=CENTER)
    self.radna_mj_tree.heading("Na radnom mjestu (G)", text="Na radnom mjestu (G)", anchor=W)

    self.radna_mj_tree.tag_configure("oddrow", background="#FBFBFB")
    self.radna_mj_tree.tag_configure("evenrow", background="#f2e9e4")

    # Radna mjesta input forms
    self.radna_mj_obrasci_frame = LabelFrame(self, text="Obrasci za unos", width=485)
    self.radna_mj_obrasci_frame.grid(row=1, column=0, padx=(15, 10), pady=(0, 10), sticky=EW)

    self.radna_mj_ID_label = Label(self.radna_mj_obrasci_frame, text="ID")
    self.radna_mj_ID_label.grid(row=1, column=0, padx=(5, 15), pady=10)

    self.radna_mj_ID_entry = Entry(self.radna_mj_obrasci_frame, width=3)
    self.radna_mj_ID_entry.grid(row=1, column=1, padx=(5, 15), pady=10)

    self.na_radnom_mjestu_label = Label(self.radna_mj_obrasci_frame, text="Radno mjesto (G)")
    self.na_radnom_mjestu_label.grid(row=1, column=2, padx=(5, 15), pady=10)

    self.na_radnom_mjestu_entry = Entry(self.radna_mj_obrasci_frame, width=35)
    self.na_radnom_mjestu_entry.grid(row=1, column=3, padx=(5, 15), pady=10)

    # Radna mjesta buttons
    self.radna_mj_naredbe_frame = LabelFrame(self, text="Naredbe", width=485)
    self.radna_mj_naredbe_frame.grid(row=2, column=0, padx=(15, 10), pady=(0, 0), sticky=EW)

    self.radna_mj_izmijeni_unos_btn = customtkinter.CTkButton(self.radna_mj_naredbe_frame, text="Izmijeni unos", fg_color="#4a4e69",
                                                              width=100)
    self.radna_mj_izmijeni_unos_btn.grid(row=1, column=0, padx=(10, 15), pady=10)
    
    self.radna_mj_dodaj_unos_btn = customtkinter.CTkButton(self.radna_mj_naredbe_frame, text="Dodaj unos", fg_color="#4a4e69")
    self.radna_mj_dodaj_unos_btn.grid(row=1, column=1, padx=(5, 15), pady=10)

    self.radna_mj_izbriši_unos_btn = customtkinter.CTkButton(self.radna_mj_naredbe_frame, text="Izbriši unos", fg_color="#4a4e69")
    self.radna_mj_izbriši_unos_btn.grid(row=1, column=2, padx=(5, 15), pady=10)

    self.radna_mj_očisti_obrasce_btn = customtkinter.CTkButton(self.radna_mj_naredbe_frame, text="Očisti obrasce", fg_color="#4a4e69",
                                                      width=119, command=self.očisti_radna_mj_obrasce)
    self.radna_mj_očisti_obrasce_btn.grid(row=1, column=4, padx=(5, 10), pady=10)

    self.radna_mj_tree.bind("<ButtonRelease-1>", self.select_radna_mjesta_data)

    get_radna_mjesta(self.radna_mj_tree)


  def očisti_radna_mj_obrasce(self):
      self.radna_mj_ID_entry.delete(0, END)
      self.na_radnom_mjestu_entry.delete(0, END)


  def select_radna_mjesta_data(self, event):
    self.radna_mj_ID_entry.delete(0, END)
    self.na_radnom_mjestu_entry.delete(0, END)

    selected = self.radna_mj_tree.focus()
    values = self.radna_mj_tree.item(selected, "values")

    self.radna_mj_ID_entry.insert(0, values[0])
    self.na_radnom_mjestu_entry.insert(0, values[1])


class PopisImenaGiDToplevelWindow(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.title("Popis imena u genitivu i dativu")

    self.geometry("613x468+300+100")
    self.grid_columnconfigure(3, weight=1)


def get_radna_mjesta(radna_mj_tree):
  db_connection = sqlite3.connect(db_path)
  db = db_connection.cursor()

  db.execute("SELECT id_radnog_mjesta, na_radnom_mjestu FROM radno_mjesto")
  rows = db.fetchall()

  global count_rm
  count_rm = 0

  for row in rows:
    if count_rm % 2 == 0:
      radna_mj_tree.insert(parent="", index="end", iid=count_rm, text="", values=(row[0], row[1]), tags=("evenrow",))
    else: 
      radna_mj_tree.insert(parent="", index="end", iid=count_rm, text="", values=(row[0], row[1]), tags=("oddrow",))
    count_rm += 1

  db_connection.commit()
  db_connection.close()


class RadnaMjFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)


class BazaFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)


def get_db_data(baza_tree):
  db_connection = sqlite3.connect(db_path)
  db = db_connection.cursor()

  # Get teachers' names from db
  db.execute("SELECT ucitelji.id_ucitelja_N, ucitelji.radno_mjesto, radno_mjesto.na_radnom_mjestu, ucitelji.prezime, \
             ucitelji.ime, ucitelji.spol FROM ucitelji \
             JOIN radno_mjesto radno_mjesto ON ucitelji.radno_mjesto = radno_mjesto.id_radnog_mjesta \
             ORDER BY prezime")
  rows = db.fetchall()

  global count
  count = 0

  for row in rows:
    if count % 2 == 0:
      baza_tree.insert(parent="", index="end", iid=count, text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=("evenrow",))
    else: 
      baza_tree.insert(parent="", index="end", iid=count, text="", values=(row[0], row[1], row[2], row[3], row[4], row[5]), tags=("oddrow",))
    count += 1

  db_connection.commit()
  db_connection.close()


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("Zamii")

    self.iconpath = ImageTk.PhotoImage(file=os.path.join("images","zamii.png"))
    self.wm_iconbitmap()
    self.iconphoto(False, self.iconpath)

    self.geometry("600x652+400+10")
    self.grid_columnconfigure(0, weight=1)

    self.grid_rowconfigure(0, weight=0)
    self.resizable(width=0, height=0)
    customtkinter.set_appearance_mode("system")

    self.zamjena_frame = ZamjenaFrame(self)
    self.zamjena_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="new")

    self.vrijeme_zamjene_frame = VrijemeZamjeneFrame(self)
    self.vrijeme_zamjene_frame.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="ew")
    
    self.obrazloženje_frame = ObrazloženjeFrame(self)
    self.obrazloženje_frame.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="ew")

    baza_podataka_btn = customtkinter.CTkButton(self, text="Baza podataka", fg_color="#9A8C98",
                                                command=self.otvori_bazu_toplevel)
    baza_podataka_btn.grid(row=3, column=0, padx=(0, 415), pady=(5, 5), sticky="e")

    izjava_btn = customtkinter.CTkButton(self, text="Dodaj izjavu", fg_color="#6d6875", 
                                            hover_color=("#118ab2"), command=dodaj_izjavu_btn_callback)
    izjava_btn.grid(row=3, column=0, padx=(0, 213), pady=(5, 5), sticky="e")
    
    primijeni_btn = customtkinter.CTkButton(self, text="Primijeni", fg_color="#110329", 
                                            hover_color=("#38A282"), command=primijeni_btn_callback)
    primijeni_btn.grid(row=3, column=0, padx=(0, 32), pady=(5, 5), sticky="e")

    self.baza_toplevel_window = None
  

  def otvori_bazu_toplevel(self):
    if self.baza_toplevel_window is None or not self.baza_toplevel_window.winfo_exists():
      self.baza_toplevel_window = BazaToplevelWindow()
    else:
      self.baza_toplevel_window.focus()


context = {}

zamii = App()
zamii.mainloop()