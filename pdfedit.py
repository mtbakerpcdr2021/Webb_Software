import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, scrolledtext
import fitz  # PyMuPDF
import os

def merge_pdfs():
    files = filedialog.askopenfilenames(title="Select PDFs to merge", filetypes=[("PDF Files", "*.pdf")])
    if not files:
        return
    output = filedialog.asksaveasfilename(title="Save Merged PDF", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not output:
        return

    pdf_writer = fitz.open()
    for path in files:
        pdf_reader = fitz.open(path)
        pdf_writer.insert_pdf(pdf_reader)
    pdf_writer.save(output)
    pdf_writer.close()
    messagebox.showinfo("Success", f"PDFs merged into {output}")

def split_pdf():
    input_file = filedialog.askopenfilename(title="Select PDF to split", filetypes=[("PDF Files", "*.pdf")])
    if not input_file:
        return
    output_folder = filedialog.askdirectory(title="Select Output Folder")
    if not output_folder:
        return

    pdf = fitz.open(input_file)
    for page_number in range(len(pdf)):
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(pdf, from_page=page_number, to_page=page_number)
        output_filename = os.path.join(output_folder, f"page_{page_number + 1}.pdf")
        pdf_writer.save(output_filename)
        pdf_writer.close()
    messagebox.showinfo("Success", f"PDF split into individual pages in {output_folder}")


def add_text_to_pdf():
    input_file = filedialog.askopenfilename(title="Select PDF to add text", filetypes=[("PDF Files", "*.pdf")])
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(title="Save PDF with Text", defaultextension=".pdf",
                                               filetypes=[("PDF Files", "*.pdf")])
    if not output_file:
        return

    text = simpledialog.askstring("Input", "Enter the text to add:")
    if text is None:
        return

    doc = fitz.open(input_file)
    max_pages = doc.page_count
    page_number = simpledialog.askinteger("Input", "Enter page number:", minvalue=1, maxvalue=max_pages)
    if not page_number:
        return

    # Positioning options
    horizontal = simpledialog.askstring("Input", "Choose position (Left or Right):")
    vertical = simpledialog.askstring("Input", "Choose position (Top, Middle, Bottom):")

    if horizontal and vertical:
        page = doc[page_number - 1]
        rect = page.rect

        if horizontal.lower() == 'left':
            x_position = rect.x0 + 10  # Slightly offset from the left edge
        else:
            x_position = rect.x1 - 10  # Slightly offset from the right edge

        y_position = {
            'top': rect.y0 + 10,  # Slightly offset from the top
            'middle': rect.height / 2,
            'bottom': rect.y1 - 10  # Slightly offset from the bottom
        }.get(vertical.lower(), rect.height / 2)

        if horizontal.lower() == 'right':
            text = "<right>" + text  # Right-align text by prepending with <right>

        page.insert_text((x_position, y_position), text, fontsize=11, color=(0, 0, 0))
        doc.save(output_file)
        doc.close()
        messagebox.showinfo("Success", f"Text added to {output_file}")


def extract_and_edit_text():
    input_file = filedialog.askopenfilename(title="Select PDF to edit text", filetypes=[("PDF Files", "*.pdf")])
    if not input_file:
        return
    output_file = filedialog.asksaveasfilename(title="Save Edited PDF", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
    if not output_file:
        return

    doc = fitz.open(input_file)
    text_instances = []

    for page_num, page in enumerate(doc):
        text_page = page.get_text("dict")
        blocks = text_page.get("blocks", [])
        for block in blocks:
            if block['type'] == 0:
                text_content = block.get("lines", [])
                combined_text = ""
                for line in text_content:
                    for span in line["spans"]:
                        combined_text += span["text"] + " "
                if combined_text.strip():
                    text_instances.append((page_num, combined_text, block["bbox"]))

    if not text_instances:
        messagebox.showinfo("Info", "No editable text found in PDF.")
        return

    edit_window = tk.Toplevel(app)
    edit_window.title("Edit Text Blocks")
    canvas = tk.Canvas(edit_window, borderwidth=0)
    frame = tk.Frame(canvas)
    vsb = tk.Scrollbar(edit_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

    text_widgets = []
    for page_num, text, bbox in text_instances:
        label = tk.Label(frame, text=f"Page {page_num + 1} Text Block:", anchor="w")
        label.pack(fill="x", padx=10, pady=2)
        txt = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=5)
        txt.insert(tk.END, text)
        txt.pack(expand=True, fill="both", padx=10, pady=2)
        text_widgets.append((page_num, txt, bbox))

    def save_changes():
        for page_num, txt_widget, bbox in text_widgets:
            new_text = txt_widget.get("1.0", "end-1c").strip()
            if new_text:
                page = doc.load_page(page_num)
                page.clean_contents()
                page.insert_text(bbox[:2], new_text, fontsize=11, color=(0, 0, 0))
        doc.save(output_file)
        doc.close()
        messagebox.showinfo("Success", f"Edited PDF saved as {output_file}")
        edit_window.destroy()

    save_btn = tk.Button(frame, text="Save Changes", command=save_changes)
    save_btn.pack(pady=10)

app = tk.Tk()
app.title("PDF Editor Tool")
app.geometry("300x200")

tk.Button(app, text="Merge PDFs", command=merge_pdfs).pack(expand=True)
tk.Button(app, text="Split PDF", command=split_pdf).pack(expand=True)
tk.Button(app, text="Add Text to PDF", command=add_text_to_pdf).pack(expand=True)
tk.Button(app, text="Edit Text in PDF", command=extract_and_edit_text).pack(expand=True)

app.mainloop()
