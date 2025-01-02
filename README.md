# Zamii

## Overview

Zamii is a desktop application built for elementary school administration. It includes features for managing overtime requests, yearly leave forms, and employee management. The most used feature of the app is applying the input information to the .docx template file so that it can be printed as soon as possible.
For this particular school where it's used in (over 70 teachers and over 600 pupils), this significantly reduces time for filling in the information into the template. The app is also used in a similar way for printing out yearly leave forms for the whole school staff (113 employees at the time of writing this documentation).


## Technologies Used

- Python
- Tkinter
- Customtkinter
- CTkMessagebox
- PIL (Pillow)
- Docxtpl
- SQLite
- Figma

## Features

1. **Teacher Replacement Management**: Allows administrators to manage teacher replacements, including selecting replacement teachers and specifying the duration and details of the replacement.
2. **Overtime Request Management**: Facilitates the creation and management of overtime requests for teachers.
3. **Yearly Leave Management**: Provides functionality to manage yearly leave requests and approvals.
4. **Employee Database Management**: Includes a database of teachers and their details, allowing for easy addition, modification, and deletion of records.

## Application Structure

### Main Window

![A screenshot showing the main Zamii window](https://drive.google.com/uc?export=view&id=19pwCtIlKCkn96KneNNmCj_2A3apXdIcq)

The main window of the application is divided into several sections:

1. **Replacement Frame**: Manages the selection of replacement teachers and the details of the replacement.
2. **Time of Replacement Frame**: Specifies the date and duration of the replacement.
3. **Explanation Frame**: Provides a textbox for entering explanations or additional details about the reasons of teacher's absence.
4. **Commands Frame**: Contains buttons for various actions such as managing yearly leave (Odluka godišnji), opening the database (Baza podataka), add statement of consent (Dodaj izjavu) and applying changes (Primijeni).

### Database Management Window

The database management window allows administrators to view, add, modify, and delete teacher records. It includes a tree view for displaying records and input forms for managing data.

### Yearly Leave Management Window

The yearly leave management window provides functionality for managing yearly leave requests. It includes dropdowns for selecting employees, specifying the duration of leave, and entering relevant dates.

## Key Functions

- **`primijeni_btn_callback`**: Applies the changes made in the main window.
- **`dodaj_unos`**: Adds a new teacher record to the database.
- **`izbriši_unos_baza`**: Deletes a selected teacher record from the database.
- **`render_document`**: Generates a document based on the provided context and saves it.
- **`render_godisnji`**: Generates a yearly leave document based on the provided context and saves it.

## Usage

1. **Managing Replacements**:
   - Select a replacement teacher and the teacher being replaced.
   - Specify the date and duration of the replacement.
   - Enter any additional details in the explanation textbox.
   - Click "Apply" to save the changes.

2. **Managing Yearly Leave**:
   - Open the yearly leave management window.
   - Select an employee and specify the duration and dates of the leave.
   - Click "Apply" to generate the yearly leave document.

3. **Managing the Database**:
   - Open the database management window.
   - Use the input forms to add, modify, or delete teacher records.
   - View the records in the tree view.

A desktop app built for elementary school administration. Overtime request, yearly leave .docx forms editor and employee management system. 



