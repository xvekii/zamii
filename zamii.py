import os
import sqlite3
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

    prezime_ime_zamjene_label = customtkinter.CTkLabel(self, text="prezime i ime zamjene", fg_color="transparent")
    prezime_ime_zamjene_label.grid(row=0, column=0, padx=(38, 0), pady=0)

    global prezime_ime_combo
    prezime_ime_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja, command=self.combo_prezime_ime_callback, 
                                                  state="normal", button_hover_color=("plum"), width=300)
    prezime_ime_combo.set("odaberi prezime i ime")
    prezime_ime_combo.grid(row=0, column=1, padx=60, pady=10, columnspan=2)
    prezime_ime_combo.grid_columnconfigure(0, weight=1)

    radnog_vremena_label = customtkinter.CTkLabel(self, text="radnog vremena", fg_color="transparent")
    radnog_vremena_label.grid(row=1, column=0, padx=(75, 0), pady=10, sticky="w")

    global radnog_vremena_radio1
    global radnog_vremena_radio2
    self.radio_rad_vrem_var = customtkinter.StringVar(value=0)
    radnog_vremena_radio1 = customtkinter.CTkRadioButton(self, text="punog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="punog")
    radnog_vremena_radio1.grid(row=1, column=1, padx=(85, 0), pady=10, sticky="w")
    
    radnog_vremena_radio2 = customtkinter.CTkRadioButton(self, text="nepunog", command=self.radiobtn_event, 
                                                        variable=self.radio_rad_vrem_var, value="nepunog")
    radnog_vremena_radio2.grid(row=1, column=2, padx=(0, 60), pady=10)

    umjesto_label = customtkinter.CTkLabel(self, text="umjesto", fg_color="transparent")
    umjesto_label.grid(row=3, column=0, padx=(126, 0), pady=10)
    
    global umjesto_combo
    umjesto_combo = customtkinter.CTkComboBox(self, values=popis_ucitelja_G, command=self.combo_umjesto_callback_G, 
                                              state="normal", button_hover_color=("plum"), width=300)
    umjesto_combo.set("odaberi prezime i ime")
    umjesto_combo.grid(row=3, column=1, padx=60, pady=10, columnspan=2)


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

    global trajanje_zamjene_combo
    trajanje_zamjene_combo = customtkinter.CTkComboBox(self, values=trajanje_sati_z_str, 
                                                       command=self.combo_trajanje_sati_z_callback, state="normal", 
                                                       button_hover_color=("plum"), width=120)
    trajanje_zamjene_combo.grid(row=1, column=1, padx=0, pady=10, columnspan=1)
    trajanje_zamjene_combo.set("koliko sati")

    šk_sat_zamjene_label = customtkinter.CTkLabel(self, text="školski sat zamjene", fg_color="transparent")
    šk_sat_zamjene_label.grid(row=2, column=0, padx=(57, 0), pady=0)

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

    obrazl_label = customtkinter.CTkLabel(self, text="obrazloženje", fg_color="transparent")
    obrazl_label.grid(row=0, column=0, padx=(98, 0), pady=0)

    global obrazl_textbox
    obrazl_textbox = customtkinter.CTkTextbox(self, width=300, height=50, corner_radius=0, border_width=1, 
                                              wrap="word", border_color=("black"))
    obrazl_textbox.grid(row=0, column=1, padx=60, pady=(10, 10), sticky="e")
    
    izbriši_btn = customtkinter.CTkButton(self, text="izbriši", width=56, fg_color="#6C757D", command=clear_obrazl_textbox_callback)
    izbriši_btn.grid(row=1, column=1, padx=60, pady=(0, 10), sticky="e")

    nadnevak_naloga_label = customtkinter.CTkLabel(self, text="nadnevak naloga", fg_color="transparent")
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
    klasa_label.grid(row=3, column=0, padx=(132, 0), pady=(0, 10))

    global klasa_textbox
    klasa_textbox = customtkinter.CTkTextbox(self, width=120, height=10, corner_radius=0, border_width=1, 
                                            border_color=("black"))
    klasa_textbox.grid(row=3, column=1, padx=(0, 240), pady=(0, 10), sticky="e")
  
  
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


def render_document():
  doc = DocxTemplate("word.docx")
  doc.render(context)
  doc.save(f"{ime_i_prezime_zamjene}.docx")
  
  print(f"Naslov dokumenta (ime i pr.) {ime_i_prezime_zamjene}")


class PretražiImePrezimeFrame(customtkinter.CTkFrame):
  def __init__(self, master):
    super().__init__(master)
    self.grid_columnconfigure(0, weight=1)

    unesi_label = customtkinter.CTkLabel(self, text="Unesi: ", fg_color="transparent")
    unesi_label.grid(row=0, column=0, padx=(0, 0), pady=0)
    
    ime_label = customtkinter.CTkLabel(self, text="ime", fg_color="transparent")
    ime_label.grid(row=1, column=0, padx=(38, 0), pady=0)
    prezime_label = customtkinter.CTkLabel(self, text="prezime", fg_color="transparent")
    prezime_label.grid(row=1, column=2, padx=(30, 0), pady=0)

    pretraži_ime_textbox = customtkinter.CTkTextbox(self, width=160, height=10, corner_radius=0, border_width=1, 
                                            border_color=("black"))
    pretraži_ime_textbox.grid(row=1, column=1, padx=(0, 0), pady=(10, 10), sticky="e")

    pretraži_ime_prezime_btn = customtkinter.CTkButton(self, text="pretraži", fg_color="#6D6875")
    pretraži_ime_prezime_btn.grid(row=2, column=1, padx=(0, 50), pady=5, sticky="e")

    



class BazaToplevelWindow(customtkinter.CTkToplevel):
  def __init__(self):
    super().__init__()
    self.title("Baza podataka")

    self.geometry("600x468+300+100")
    self.grid_columnconfigure(3, weight=1)

    self.pretraži_ime_prezime_frame = PretražiImePrezimeFrame(self)
    self.pretraži_ime_prezime_frame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="new")


class App(customtkinter.CTk):
  def __init__(self):
    super().__init__()
    self.title("Zamii")

    self.iconpath = ImageTk.PhotoImage(file=os.path.join("images","zamii.png"))
    self.wm_iconbitmap()
    self.iconphoto(False, self.iconpath)

    self.geometry("600x668+300+100")
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

    baza_podataka_btn = customtkinter.CTkButton(self, text="baza podataka", fg_color="#9A8C98",
                                                command=self.otvori_bazu_toplevel)
    baza_podataka_btn.grid(row=3, column=0, padx=(0, 415), pady=5, sticky="e")

    izjava_btn = customtkinter.CTkButton(self, text="dodaj izjavu", fg_color="#6d6875", 
                                            hover_color=("#118ab2"), command=dodaj_izjavu_btn_callback)
    izjava_btn.grid(row=3, column=0, padx=(0, 215), pady=5, sticky="e")
    
    primijeni_btn = customtkinter.CTkButton(self, text="primijeni", fg_color="#110329", 
                                            hover_color=("#38A282"), command=primijeni_btn_callback)
    primijeni_btn.grid(row=3, column=0, padx=(0, 35), pady=5, sticky="e")

    self.baza_toplevel_window = None


  def otvori_bazu_toplevel(self):
    if self.baza_toplevel_window is None or not self.baza_toplevel_window.winfo_exists():
      self.baza_toplevel_window = BazaToplevelWindow()
    else:
      self.baza_toplevel_window.focus()


context = {}

zamii = App()
zamii.mainloop()