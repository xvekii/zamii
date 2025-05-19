# Zamii

## Overview

Zamii (Croatian "zamjena" = "replacement") is a desktop application built for elementary school administration. It includes features for managing overtime requests, yearly leave forms, and employee management. 

The most used feature of the app is applying the input information in the Main Window to the .docx template file so that it can be printed as soon as possible.
For this particular school where it's in active use (over 70 teachers and over 600 pupils), this significantly reduces time for filling in the information into the template. 

The app is also used for printing out yearly leave forms for the whole school staff (113 employees at the time of writing this Readme).

## Features

1. **Teacher Replacement Management** (**Overtime Request Management**): 
- Facilitates the creation and management of overtime requests for teachers.

- Allows administrators to manage teacher replacements, including selecting replacement teachers and specifying the duration and details of the replacement. The input information is applied to the .docx template file so that it can be printed and handed out.

2. **Yearly Leave Management**: Provides functionality to manage yearly leave requests and approvals so that the form can be printed and handed out.

3. **Employee Database Management**: Includes a database of teachers (and all employees) and their details, allowing for easy addition, modification, and deletion of records.

## Technologies Used

- Python
- Tkinter
- Customtkinter
- CTkMessagebox
- PIL (Pillow)
- Docxtpl
- SQLite
- Figma



## Application Structure

The main window of the application is divided into several sections:

1. **Replacement Frame**: Manages the selection of replacement teachers and the details of the replacement.
2. **Time of Replacement Frame**: Specifies the date and duration of the replacement.
3. **Explanation Frame**: Provides a textbox for entering explanations or additional details about the reasons of teacher's absence.
4. **Commands Frame**: Contains buttons for various actions such as managing yearly leave ("**Odluka godišnji**"), opening the database ("**Baza podataka**"), add statement of consent ("**Dodaj izjavu**") and applying changes ("**Primijeni**").
   

## Main Window

![A screenshot showing the main Zamii window](https://drive.google.com/uc?export=view&id=19pwCtIlKCkn96KneNNmCj_2A3apXdIcq)


## Yearly Leave Management Window

![Yearly-leave-window](https://github.com/user-attachments/assets/d7123376-56e4-4405-b942-a4ac253d44ac)

The yearly leave management window provides functionality for managing yearly leave requests. It includes dropdowns for selecting employees, specifying the duration of leave, opening all employees management window and entering relevant dates.

## All Employees Management Window (for yearly leave document printing)

![All-employees-window](https://github.com/user-attachments/assets/f3f8c173-a4b4-4f03-9296-515144d00ccd)


## Database Management Window

![Database-window](https://github.com/user-attachments/assets/88acf3b3-0487-437f-ab34-1dd4766f811b)


The database management window allows administrators to view, add, modify, and delete teacher records. It includes a tree view for displaying records and input forms for managing data.


## Teacher Position Window

![Teacher-position-window](https://github.com/user-attachments/assets/4ad361ff-bee0-4d61-9e37-1125746b80b4)


## Relational Database Diagram

![Relational-database-diagram](https://github.com/user-attachments/assets/28baec48-cd4b-488e-bf60-0d6e439372a0)

## Overtime Template Document 

![Overtime-template](https://github.com/user-attachments/assets/475f3806-a8a8-4d6e-be12-635d9a6c9c4c)

## Yearly Leave Template Document

![Yearly-leave-template](https://github.com/user-attachments/assets/2fef2cf5-4635-40c4-95ac-188f6c995346)


## Zamii Desktop Icon (Designed in Figma)

![zamii-taskbar](https://github.com/user-attachments/assets/a112f07f-72c3-434c-b55d-d2e979c79cac)



## Usage

1. **Managing Replacements**:
   - Select a replacement teacher "**Prezime i ime zamjene**" (Surname and name of the replacement) and the teacher being replaced "**Umjesto**" (Instead of). All of the data related to that teacher's position (Nominative, Genitive and Dative forms of the name and surname, gender (for grammatical reasons) related word forms) are automatically filled in.
   - Specify the date "**Nadnevak zamjene**" and duration "**Trajanje zamjene**" of the replacement.
   - Specify which classes in the schedule the replacement applies to "**Školski sat zamjene**".
   - Enter any additional details in the explanation textbox "**Obrazloženje**".
   - Click "**Dodaj izjavu**" (Add statement) to apply the statement of consent for the teacher whose status requires additional consent.
   - Click "**Primijeni**" (Apply) to save the changes and generate the overtime request document that will be printed.

2. **Managing Yearly Leave**:
   - Open the yearly leave management window.
   - Select an employee and specify the duration and dates of the leave.
   - Manage all employees
   - Click  "**Primijeni**" (Apply) to generate the yearly leave document that will be printed.

3. **Managing the Database**:
   - Open the database management window.
   - Use the input forms to add "**Dodaj unos**", modify "**Izmijeni unos**", or delete "**Izbriši unos**" teacher records.
   - View the list of teacher positions "**Popis radnih mjesta**" - all of the positions are under a certain ID in order to facilitate database operations and avoid repetition.
   - View the records in the tree view.
   - Clear the forms "**Očisti obrasce**"
