"""
Emergency Card UI Component - Shared by both Dialog and Tab
Location: gui/components/emergency_card_content.py

This is the SINGLE SOURCE OF TRUTH for emergency card display.
Used by both EmergencyDialog (popup) and EmergencyCardTab (tab).
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.styles import *
from utils.pdf_generator import generate_emergency_card
from utils.qr_generator import generate_patient_qr
from PIL import ImageTk
import os


class EmergencyCardContent(ctk.CTkFrame):
    """
    Emergency card UI component - can be used in dialog or tab.
    
    This is the ONLY place where emergency card UI is defined.
    Both EmergencyDialog and EmergencyCardTab use this component.
    """
    
    def __init__(self, parent, patient_data, show_close_button=False):
        """
        Create emergency card UI
        
        Args:
            parent: Parent widget (dialog or tab)
            patient_data: Patient information dictionary
            show_close_button: If True, shows Close button (for dialog)
                              If False, only shows PDF button (for tab)
        """
        super().__init__(parent, fg_color=COLORS['bg_dark'])
        
        self.patient_data = patient_data
        self.show_close_button = show_close_button
        self.parent = parent
        
        self.create_ui()
    
    def create_ui(self):
        """Create emergency card UI"""
        # Emergency header - Red
        emergency_header = ctk.CTkFrame(
            self,
            fg_color=COLORS['danger'],
            height=120
        )
        emergency_header.pack(fill='x')
        emergency_header.pack_propagate(False)

        header_content = ctk.CTkFrame(emergency_header, fg_color='transparent')
        header_content.pack(expand=True)

        emergency_icon = ctk.CTkLabel(
            header_content,
            text="🆘",
            font=('Segoe UI', 48)
        )
        emergency_icon.pack()

        emergency_title = ctk.CTkLabel(
            header_content,
            text="EMERGENCY CARD",
            font=('Segoe UI', 28, 'bold'),
            text_color='white'
        )
        emergency_title.pack()

        # Scrollable content
        content_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color='transparent'
        )
        content_scroll.pack(fill='both', expand=True, padx=30, pady=30)

        # Patient Name - Large
        name_label = ctk.CTkLabel(
            content_scroll,
            text=self.patient_data.get('full_name', 'N/A'),
            font=('Segoe UI', 32, 'bold'),
            text_color=COLORS['text_primary']
        )
        name_label.pack(pady=(0, 5))

        # National ID
        id_label = ctk.CTkLabel(
            content_scroll,
            text=f"ID: {self.patient_data.get('national_id', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_muted']
        )
        id_label.pack(pady=(0, 20))

        # Divider
        ctk.CTkFrame(
            content_scroll,
            height=2,
            fg_color=COLORS['bg_hover']
        ).pack(fill='x', pady=20)

        # Blood Type - Highlighted
        blood_frame = ctk.CTkFrame(
            content_scroll,
            fg_color=COLORS['danger'],
            corner_radius=RADIUS['lg'],
            height=80
        )
        blood_frame.pack(fill='x', pady=(0, 20))
        blood_frame.pack_propagate(False)

        blood_content = ctk.CTkFrame(blood_frame, fg_color='transparent')
        blood_content.place(relx=0.5, rely=0.5, anchor='center')

        blood_label = ctk.CTkLabel(
            blood_content,
            text=f"🩸 Blood Type: {self.patient_data.get('blood_type', 'Unknown')}",
            font=('Segoe UI', 24, 'bold'),
            text_color='white'
        )
        blood_label.pack()

        # Basic Info
        info_frame = ctk.CTkFrame(
            content_scroll,
            fg_color=COLORS['bg_medium'],
            corner_radius=RADIUS['md']
        )
        info_frame.pack(fill='x', pady=(0, 20))

        info_content = ctk.CTkFrame(info_frame, fg_color='transparent')
        info_content.pack(fill='x', padx=20, pady=20)

        info_row = ctk.CTkFrame(info_content, fg_color='transparent')
        info_row.pack(fill='x')

        age_label = ctk.CTkLabel(
            info_row,
            text=f"Age: {self.patient_data.get('age', 'N/A')} years",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        age_label.pack(side='left', padx=(0, 40))

        gender_label = ctk.CTkLabel(
            info_row,
            text=f"Gender: {self.patient_data.get('gender', 'N/A')}",
            font=FONTS['body'],
            text_color=COLORS['text_primary']
        )
        gender_label.pack(side='left')

        # Allergies - Red warning if present
        allergies = self.patient_data.get('allergies', [])
        if allergies:
            allergy_frame = ctk.CTkFrame(
                content_scroll,
                fg_color='#fef2f2',
                corner_radius=RADIUS['md'],
                border_width=2,
                border_color=COLORS['danger']
            )
            allergy_frame.pack(fill='x', pady=(0, 20))

            allergy_content = ctk.CTkFrame(
                allergy_frame, fg_color='transparent')
            allergy_content.pack(fill='x', padx=20, pady=20)

            allergy_title = ctk.CTkLabel(
                allergy_content,
                text="⚠️ ALLERGIES",
                font=FONTS['subheading'],
                text_color=COLORS['danger']
            )
            allergy_title.pack(anchor='w', pady=(0, 10))

            allergy_text = ctk.CTkLabel(
                allergy_content,
                text=", ".join(allergies),
                font=FONTS['body_bold'],
                text_color='#7f1d1d',
                anchor='w'
            )
            allergy_text.pack(anchor='w')
        else:
            no_allergy_label = ctk.CTkLabel(
                content_scroll,
                text="✓ No known allergies",
                font=FONTS['body'],
                text_color=COLORS['secondary']
            )
            no_allergy_label.pack(anchor='w', pady=(0, 20))

        # Chronic Diseases
        chronic = self.patient_data.get('chronic_diseases', [])
        if chronic:
            chronic_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            chronic_frame.pack(fill='x', pady=(0, 20))

            chronic_content = ctk.CTkFrame(
                chronic_frame, fg_color='transparent')
            chronic_content.pack(fill='x', padx=20, pady=20)

            chronic_title = ctk.CTkLabel(
                chronic_content,
                text="🏥 Chronic Conditions",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            chronic_title.pack(anchor='w', pady=(0, 8))

            chronic_text = ctk.CTkLabel(
                chronic_content,
                text=", ".join(chronic),
                font=FONTS['body'],
                text_color=COLORS['text_secondary'],
                anchor='w'
            )
            chronic_text.pack(anchor='w')

        # Current Medications
        medications = self.patient_data.get('current_medications', [])
        if medications:
            meds_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            meds_frame.pack(fill='x', pady=(0, 20))

            meds_content = ctk.CTkFrame(meds_frame, fg_color='transparent')
            meds_content.pack(fill='x', padx=20, pady=20)

            meds_title = ctk.CTkLabel(
                meds_content,
                text="💊 Current Medications",
                font=FONTS['body_bold'],
                text_color=COLORS['text_primary']
            )
            meds_title.pack(anchor='w', pady=(0, 10))

            for i, med in enumerate(medications[:3], 1):
                # Handle both dict and string formats
                if isinstance(med, dict):
                    med_text = f"{i}. {med.get('name', 'N/A')} - {med.get('dosage', '')} {med.get('frequency', '')}"
                else:
                    med_text = f"{i}. {med}"
                
                med_label = ctk.CTkLabel(
                    meds_content,
                    text=med_text,
                    font=FONTS['body'],
                    text_color=COLORS['text_secondary'],
                    anchor='w'
                )
                med_label.pack(anchor='w', pady=2)

        # Emergency Contact
        emergency = self.patient_data.get('emergency_contact', {})
        if emergency:
            contact_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['info'],
                corner_radius=RADIUS['md']
            )
            contact_frame.pack(fill='x', pady=(0, 20))

            contact_content = ctk.CTkFrame(
                contact_frame, fg_color='transparent')
            contact_content.pack(fill='x', padx=20, pady=20)

            contact_title = ctk.CTkLabel(
                contact_content,
                text="📞 Emergency Contact",
                font=FONTS['body_bold'],
                text_color='white'
            )
            contact_title.pack(anchor='w', pady=(0, 8))

            contact_name = ctk.CTkLabel(
                contact_content,
                text=f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})",
                font=FONTS['body'],
                text_color='white',
                anchor='w'
            )
            contact_name.pack(anchor='w')

            contact_phone = ctk.CTkLabel(
                contact_content,
                text=f"Phone: {emergency.get('phone', 'N/A')}",
                font=FONTS['body_bold'],
                text_color='white',
                anchor='w'
            )
            contact_phone.pack(anchor='w')

        # QR Code
        try:
            qr_frame = ctk.CTkFrame(
                content_scroll,
                fg_color=COLORS['bg_medium'],
                corner_radius=RADIUS['md']
            )
            qr_frame.pack(fill='x')

            qr_content = ctk.CTkFrame(qr_frame, fg_color='transparent')
            qr_content.pack(padx=20, pady=20)

            qr_img = generate_patient_qr(
                self.patient_data.get('national_id', ''))
            qr_photo = ImageTk.PhotoImage(qr_img)

            qr_label = ctk.CTkLabel(
                qr_content,
                image=qr_photo,
                text=""
            )
            qr_label.image = qr_photo  # Keep reference
            qr_label.pack()

            qr_text = ctk.CTkLabel(
                qr_content,
                text="Scan for quick access",
                font=FONTS['small'],
                text_color=COLORS['text_muted']
            )
            qr_text.pack(pady=(5, 0))

        except Exception as e:
            print(f"QR code display error: {e}")

        # Action buttons
        btn_frame = ctk.CTkFrame(self, fg_color='transparent')
        btn_frame.pack(fill='x', padx=30, pady=(0, 30))

        # PDF button (always shown)
        if self.show_close_button:
            # Dialog mode: Two buttons side by side
            generate_btn = ctk.CTkButton(
                btn_frame,
                text="💾 Generate PDF",
                command=self.generate_pdf,
                font=FONTS['body_bold'],
                height=50,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            generate_btn.pack(side='left', fill='x', expand=True, padx=(0, 10))

            close_btn = ctk.CTkButton(
                btn_frame,
                text="Close",
                command=self.close_parent,
                font=FONTS['body_bold'],
                height=50,
                fg_color='transparent',
                hover_color=COLORS['bg_light'],
                border_width=2,
                border_color=COLORS['primary'],
                text_color=COLORS['primary']
            )
            close_btn.pack(side='right', fill='x', expand=True, padx=(10, 0))
        else:
            # Tab mode: Only PDF button
            generate_btn = ctk.CTkButton(
                btn_frame,
                text="💾 Generate PDF Emergency Card",
                command=self.generate_pdf,
                font=FONTS['body_bold'],
                height=50,
                fg_color=COLORS['secondary'],
                hover_color='#059669'
            )
            generate_btn.pack(fill='x')

    def generate_pdf(self):
        """Generate emergency card PDF"""
        try:
            # Ask where to save
            default_filename = f"Emergency_Card_{self.patient_data.get('full_name', 'Patient').replace(' ', '_')}.pdf"

            file_path = filedialog.asksaveasfilename(
                title="Save Emergency Card",
                defaultextension=".pdf",
                filetypes=[("PDF Files", "*.pdf")],
                initialfile=default_filename
            )

            if not file_path:
                return

            # Generate PDF
            success = generate_emergency_card(self.patient_data, file_path)

            if success:
                messagebox.showinfo(
                    "Success",
                    f"Emergency card saved successfully!\n\n{file_path}\n\n"
                    "Print this card and keep it in your wallet."
                )

                # Ask if user wants to open the file
                if messagebox.askyesno("Open File", "Would you like to open the PDF now?"):
                    import platform
                    import subprocess

                    if platform.system() == 'Windows':
                        os.startfile(file_path)
                    elif platform.system() == 'Darwin':  # macOS
                        subprocess.call(['open', file_path])
                    else:  # Linux
                        subprocess.call(['xdg-open', file_path])
            else:
                messagebox.showerror(
                    "Error", "Failed to generate emergency card PDF")

        except Exception as e:
            messagebox.showerror(
                "Error", f"Failed to save emergency card: {str(e)}")
    
    def close_parent(self):
        """Close the parent dialog"""
        if hasattr(self.parent, 'destroy'):
            self.parent.destroy()