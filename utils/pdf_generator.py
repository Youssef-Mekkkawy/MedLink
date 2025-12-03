"""
PROFESSIONAL MEDICAL EMERGENCY CARD - Brand New Design
Optimized for quick scanning by emergency doctors
Clean, professional, medical-grade quality

Location: utils/pdf_generator.py (REPLACE ENTIRE FILE)
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
from utils.qr_generator import generate_patient_qr
import io


def generate_emergency_card(patient_data: dict, output_path: str) -> bool:
    """
    Generate professional medical-grade emergency card
    Optimized for emergency situations - quick scanning
    
    Design Features:
    - Large critical info (blood type, allergies)
    - Color-coded sections
    - Clear visual hierarchy
    - Professional medical aesthetic
    - Easy to read in 10 seconds
    """
    try:
        pdf = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter
        
        # Professional medical colors
        EMERGENCY_RED = (0.85, 0.11, 0.14)      # Deep red
        CRITICAL_ORANGE = (1.0, 0.6, 0.0)       # Orange
        INFO_BLUE = (0.0, 0.45, 0.70)           # Medical blue
        SUCCESS_GREEN = (0.13, 0.55, 0.13)      # Green
        DARK_GRAY = (0.2, 0.2, 0.2)             # Almost black
        LIGHT_GRAY = (0.95, 0.95, 0.95)         # Very light gray
        
        # ============================================
        # TOP STRIPE - Emergency Header
        # ============================================
        pdf.setFillColorRGB(*EMERGENCY_RED)
        pdf.rect(0, height - 0.6*inch, width, 0.6*inch, fill=True, stroke=False)
        
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 20)
        pdf.drawString(0.5*inch, height - 0.4*inch, "🚨 EMERGENCY MEDICAL CARD")
        
        pdf.setFont("Helvetica", 10)
        pdf.drawRightString(width - 0.5*inch, height - 0.4*inch, 
                           f"Generated: {datetime.now().strftime('%d %b %Y')}")
        
        y = height - 1.0*inch
        
        # ============================================
        # PATIENT IDENTIFICATION - Large & Clear
        # ============================================
        # Name - Very large
        pdf.setFillColorRGB(*DARK_GRAY)
        pdf.setFont("Helvetica-Bold", 26)
        patient_name = patient_data.get('full_name', 'N/A').upper()
        pdf.drawString(0.5*inch, y, patient_name)
        
        y -= 0.35*inch
        
        # Basic info row
        pdf.setFont("Helvetica", 11)
        age = patient_data.get('age', 'N/A')
        gender = patient_data.get('gender', 'N/A')
        national_id = patient_data.get('national_id', 'N/A')
        
        pdf.drawString(0.5*inch, y, 
                      f"AGE: {age}  •  GENDER: {gender}  •  ID: {national_id}")
        
        y -= 0.5*inch
        
        # ============================================
        # CRITICAL SECTION 1: BLOOD TYPE
        # ============================================
        box_x = 0.5*inch
        box_width = 2.3*inch
        box_height = 1.3*inch
        
        # Blood type box - Red background
        pdf.setFillColorRGB(0.98, 0.85, 0.85)  # Light red
        pdf.setStrokeColorRGB(*EMERGENCY_RED)
        pdf.setLineWidth(3)
        pdf.roundRect(box_x, y - box_height, box_width, box_height, 
                     10, fill=True, stroke=True)
        
        # "BLOOD TYPE" label
        pdf.setFillColorRGB(*EMERGENCY_RED)
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(box_x + 0.15*inch, y - 0.25*inch, "BLOOD TYPE")
        
        # Blood type value - HUGE
        pdf.setFont("Helvetica-Bold", 56)
        blood_type = patient_data.get('blood_type', '?')
        pdf.drawCentredString(box_x + box_width/2, y - 0.95*inch, blood_type)
        
        # ============================================
        # CRITICAL SECTION 2: ALLERGIES
        # ============================================
        box_x2 = 3.0*inch
        box_width2 = 5.0*inch
        
        allergies = patient_data.get('allergies', [])
        if allergies:
            # Allergies box - Orange background
            pdf.setFillColorRGB(1.0, 0.95, 0.85)  # Light orange
            pdf.setStrokeColorRGB(*CRITICAL_ORANGE)
            pdf.setLineWidth(3)
            pdf.roundRect(box_x2, y - box_height, box_width2, box_height,
                         10, fill=True, stroke=True)
            
            # "ALLERGIES" label with warning
            pdf.setFillColorRGB(*CRITICAL_ORANGE)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(box_x2 + 0.15*inch, y - 0.25*inch, "⚠️  ALLERGIES - AVOID THESE")
            
            # Allergies list - Large and clear
            pdf.setFillColorRGB(0.6, 0.2, 0.0)  # Dark orange-brown
            pdf.setFont("Helvetica-Bold", 16)
            
            # Show up to 3 allergies
            allergy_y = y - 0.55*inch
            for allergy in allergies[:3]:
                pdf.drawString(box_x2 + 0.15*inch, allergy_y, f"• {allergy}")
                allergy_y -= 0.28*inch
            
            if len(allergies) > 3:
                pdf.setFont("Helvetica", 10)
                pdf.drawString(box_x2 + 0.15*inch, allergy_y, 
                              f"+ {len(allergies)-3} more allergies")
        else:
            # No allergies - Green box
            pdf.setFillColorRGB(0.9, 0.98, 0.9)  # Light green
            pdf.setStrokeColorRGB(*SUCCESS_GREEN)
            pdf.setLineWidth(2)
            pdf.roundRect(box_x2, y - box_height, box_width2, box_height,
                         10, fill=True, stroke=True)
            
            pdf.setFillColorRGB(*SUCCESS_GREEN)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(box_x2 + 0.15*inch, y - 0.25*inch, "ALLERGIES")
            
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawCentredString(box_x2 + box_width2/2, y - 0.75*inch, 
                                 "✓ NO KNOWN ALLERGIES")
        
        y -= box_height + 0.4*inch
        
        # ============================================
        # SECTION 3: CHRONIC CONDITIONS
        # ============================================
        chronic = patient_data.get('chronic_diseases', [])
        if chronic:
            # Section header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(0.5*inch, y, "CHRONIC CONDITIONS")
            
            y -= 0.05*inch
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.line(0.5*inch, y, width - 0.5*inch, y)
            y -= 0.25*inch
            
            # Conditions in columns
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica", 11)
            
            col1_x = 0.7*inch
            col2_x = 4.5*inch
            
            for i, condition in enumerate(chronic):
                if i < 4:  # First column
                    pdf.drawString(col1_x, y - (i * 0.25*inch), f"• {condition}")
                elif i < 8:  # Second column
                    pdf.drawString(col2_x, y - ((i-4) * 0.25*inch), f"• {condition}")
            
            if len(chronic) > 8:
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawString(col1_x, y - 1.1*inch, f"+ {len(chronic)-8} more conditions")
            
            y -= max(1.2*inch, (min(len(chronic), 4) * 0.25*inch) + 0.3*inch)
        
        # ============================================
        # SECTION 4: CURRENT MEDICATIONS
        # ============================================
        medications = patient_data.get('current_medications', [])
        if medications:
            # Section header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(0.5*inch, y, "CURRENT MEDICATIONS")
            
            y -= 0.05*inch
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.line(0.5*inch, y, width - 0.5*inch, y)
            y -= 0.3*inch
            
            # Medications table
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(0.7*inch, y, "MEDICATION")
            pdf.drawString(3.5*inch, y, "DOSAGE")
            pdf.drawString(5.5*inch, y, "FREQUENCY")
            
            y -= 0.2*inch
            
            pdf.setFont("Helvetica", 10)
            for i, med in enumerate(medications[:5]):  # Show max 5
                if isinstance(med, dict):
                    med_name = med.get('name', 'Unknown')
                    dosage = med.get('dosage', '-')
                    frequency = med.get('frequency', '-')
                else:
                    med_name = str(med)
                    dosage = '-'
                    frequency = '-'
                
                # Truncate if too long
                if len(med_name) > 30:
                    med_name = med_name[:27] + "..."
                
                pdf.drawString(0.7*inch, y, med_name)
                pdf.drawString(3.5*inch, y, dosage)
                pdf.drawString(5.5*inch, y, frequency)
                
                y -= 0.22*inch
            
            if len(medications) > 5:
                pdf.setFont("Helvetica-Oblique", 9)
                pdf.drawString(0.7*inch, y - 0.1*inch, 
                              f"+ {len(medications)-5} more medications")
                y -= 0.2*inch
            
            y -= 0.3*inch
        
        # ============================================
        # SECTION 5: EMERGENCY CONTACT
        # ============================================
        emergency = patient_data.get('emergency_contact', {})
        if emergency:
            # Contact box - Blue background
            contact_height = 0.9*inch
            pdf.setFillColorRGB(0.9, 0.95, 1.0)  # Light blue
            pdf.setStrokeColorRGB(*INFO_BLUE)
            pdf.setLineWidth(2)
            pdf.roundRect(0.5*inch, y - contact_height, 4.5*inch, contact_height,
                         8, fill=True, stroke=True)
            
            # Header
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(0.65*inch, y - 0.25*inch, "EMERGENCY CONTACT")
            
            # Name and relation
            pdf.setFillColorRGB(*DARK_GRAY)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(0.65*inch, y - 0.5*inch, 
                          f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})")
            
            # Phone - Large
            pdf.setFont("Helvetica-Bold", 16)
            pdf.setFillColorRGB(*INFO_BLUE)
            pdf.drawString(0.65*inch, y - 0.75*inch, 
                          f"📞 {emergency.get('phone', 'N/A')}")
        
        # ============================================
        # SECTION 6: RELIGIOUS/SPECIAL CONSIDERATIONS
        # ============================================
        directives = patient_data.get('emergency_directives', {})
        religious = directives.get('religious_preferences', {}) if directives else {}
        
        if religious.get('religion') or religious.get('special_considerations'):
            special_height = 0.75*inch
            pdf.setFillColorRGB(0.98, 0.98, 1.0)  # Very light purple
            pdf.setStrokeColorRGB(0.5, 0.4, 0.7)  # Purple
            pdf.setLineWidth(1.5)
            pdf.roundRect(5.2*inch, y - special_height, 2.8*inch, special_height,
                         8, fill=True, stroke=True)
            
            pdf.setFillColorRGB(0.3, 0.2, 0.5)
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(5.35*inch, y - 0.22*inch, "SPECIAL CONSIDERATIONS")
            
            pdf.setFont("Helvetica", 9)
            if religious.get('religion'):
                pdf.drawString(5.35*inch, y - 0.42*inch, 
                              f"Religion: {religious.get('religion')}")
            
            if religious.get('special_considerations'):
                considerations = religious.get('special_considerations')
                if len(considerations) > 35:
                    considerations = considerations[:32] + "..."
                pdf.drawString(5.35*inch, y - 0.6*inch, considerations)
        
        # ============================================
        # QR CODE - Bottom Right Corner
        # ============================================
        try:
            qr_img = generate_patient_qr(patient_data.get('national_id', ''))
            qr_buffer = io.BytesIO()
            qr_img.save(qr_buffer, format='PNG')
            qr_buffer.seek(0)
            
            qr_size = 1.4*inch
            qr_x = width - qr_size - 0.5*inch
            qr_y = 0.7*inch
            
            # QR box background
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setStrokeColorRGB(0.7, 0.7, 0.7)
            pdf.setLineWidth(1)
            pdf.rect(qr_x - 0.05*inch, qr_y - 0.05*inch, 
                    qr_size + 0.1*inch, qr_size + 0.3*inch,
                    fill=True, stroke=True)
            
            pdf.drawImage(qr_buffer, qr_x, qr_y, 
                         width=qr_size, height=qr_size,
                         preserveAspectRatio=True, mask='auto')
            
            pdf.setFont("Helvetica", 7)
            pdf.setFillColorRGB(0.4, 0.4, 0.4)
            pdf.drawCentredString(qr_x + qr_size/2, qr_y - 0.15*inch, 
                                 "Scan for full medical records")
        except Exception as e:
            print(f"QR code error: {e}")
        
        # ============================================
        # FOOTER - Important Notice
        # ============================================
        footer_y = 0.5*inch
        
        # Footer bar
        pdf.setFillColorRGB(*LIGHT_GRAY)
        pdf.rect(0, footer_y - 0.15*inch, width, 0.35*inch, fill=True, stroke=False)
        
        # MedLink branding
        pdf.setFont("Helvetica-Bold", 9)
        pdf.setFillColorRGB(*INFO_BLUE)
        pdf.drawString(0.5*inch, footer_y + 0.05*inch, "MedLink")
        
        pdf.setFont("Helvetica", 8)
        pdf.setFillColorRGB(0.5, 0.5, 0.5)
        pdf.drawString(0.5*inch, footer_y - 0.1*inch, 
                      "Unified Medical Records System")
        
        # Keep card notice
        pdf.setFont("Helvetica-Bold", 8)
        pdf.setFillColorRGB(*EMERGENCY_RED)
        pdf.drawCentredString(width/2, footer_y, 
                             "⚠️  KEEP THIS CARD WITH YOU AT ALL TIMES")
        
        # Save PDF
        pdf.save()
        return True
        
    except Exception as e:
        print(f"Error generating emergency card: {e}")
        import traceback
        traceback.print_exc()
        return False