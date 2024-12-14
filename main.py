import flet as ft
from fpdf import FPDF
import os

class PhotoManager:
    def __init__(self):
        self.photos = []

    def add_photo(self, photo_path):
        self.photos.append(photo_path)

    def get_photos(self):
        return self.photos

    def clear_photos(self):
        self.photos = []

def main(page: ft.Page):
    page.title = "Vehicle Damage Report"
    page.scroll = "adaptive"

    photo_manager = PhotoManager()

    # Checklist items
    checklist_items = [
        "Capout is broken",
        "Front light is working",
        "Back light is working",
        "Front bumper is broken",
        "Front left door has an accident",
        "Back left door has an accident",
        "Front right door has an accident",
        "Back right door has an accident",
        "Back bumper has an accident",
    ]

    # Checkboxes
    checkboxes = [ft.Checkbox(label=item, value=True) for item in checklist_items]

    # Placeholder for photos
    photo_list_view = ft.ListView(expand=True)

    def add_photo(e):
        # Simulate adding a photo (use a placeholder image or a selected file path)
        photo_path = f"https://via.placeholder.com/300x200.png?text=Photo+{len(photo_manager.get_photos()) + 1}"
        photo_manager.add_photo(photo_path)
        photo_list_view.controls.append(ft.Image(src=photo_path, width=300, height=200))
        page.update()

    def save_as_pdf():
        def save_file(e):
            file_name = file_name_input.value.strip()
            if not file_name.endswith(".pdf"):
                file_name += ".pdf"

            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Add checklist items to PDF
                pdf.cell(200, 10, txt="Vehicle Damage Report", ln=True, align="C")
                pdf.ln(10)

                for cb in checkboxes:
                    pdf.cell(0, 10, txt=f"{cb.label}: {'Yes' if cb.value else 'No'}", ln=True)

                pdf.ln(10)
                pdf.cell(0, 10, txt="Photos:", ln=True)

                # Add photos to PDF
                for photo_path in photo_manager.get_photos():
                    pdf.image(photo_path, x=10, y=pdf.get_y(), w=100)
                    pdf.ln(50)

                pdf.output(file_name)
                page.snack_bar = ft.SnackBar(ft.Text(f"PDF saved as {file_name}"))
                page.snack_bar.open = True
            except Exception as ex:
                page.snack_bar = ft.SnackBar(ft.Text(f"Error saving PDF: {ex}"), bgcolor="red")
                page.snack_bar.open = True

            page.update()

        # Ask for file name
        file_name_input = ft.TextField(label="Enter file name", required=True)
        save_button = ft.ElevatedButton("Save", on_click=save_file)

        page.dialog = ft.AlertDialog(
            title=ft.Text("Save PDF"),
            content=ft.Column([file_name_input, save_button]),
            on_dismiss=lambda e: None,
        )
        page.dialog.open = True
        page.update()

    # Buttons for actions
    submit_button = ft.ElevatedButton("Submit", on_click=lambda e: save_as_pdf())
    add_photo_button = ft.ElevatedButton("Add Photo", on_click=add_photo)
    convert_pdf_button = ft.ElevatedButton("Convert to PDF", on_click=lambda e: save_as_pdf())

    # Add components to page
    page.add(ft.Text("Vehicle Damage Checklist", size=20, weight="bold"))
    page.add(ft.Column(checkboxes))
    page.add(ft.Text("Photos:", size=16, weight="bold"))
    page.add(photo_list_view)
    page.add(ft.Row([add_photo_button, convert_pdf_button, submit_button], alignment="center"))

ft.app(target=main)
