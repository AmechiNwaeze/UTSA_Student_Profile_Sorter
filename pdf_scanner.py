import os
import sys
import PyPDF2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

def search_pdf(pdf_file, search_phrase, match_type):
    pdf = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num].extract_text()
        lines = page.split("\n")
        for line in lines:
            if match_type == "Full Match":
                if all(word.lower() in line.lower() for word in search_phrase.split()):
                    return line
            else:
                if any(word.lower() in line.lower() for word in search_phrase.split()):
                    return line
    return False

def search_folder(folder_path, search_phrase, match_type):
    results = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_file = open(os.path.join(folder_path, filename), 'rb')
            result = search_pdf(pdf_file, search_phrase, match_type)
            
            if result:
                results.append({
                    "search_phrase": search_phrase,
                    "context": f"Found in file: {filename}: '{result}'"
                })
    return results

def write_to_text(results, text_file):
    with open(text_file, 'w') as file:
        for result in results:
            file.write("Search phrase: " + result["search_phrase"] + "\n")
            file.write("Context in PDF: " + result["context"] + "\n")

# Example usage
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title = "Select the folder containing the PDFs")

match_type = simpledialog.askstring("Match Type", "Enter Full Match or Partial Match:")
search_phrase = simpledialog.askstring("Search Phrase", "Enter the search phrase:")
results = search_folder(folder_path, search_phrase, match_type)

if results:
    text_file = "results.txt"
    write_to_text(results, text_file)
    
    save = messagebox.askyesno("Save", "Do you want to save the text file?")
    if save:
        text_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Save the Text File")
        write_to_text(results, text_file)
else:
    messagebox.showinfo("No Results", "No results found")

