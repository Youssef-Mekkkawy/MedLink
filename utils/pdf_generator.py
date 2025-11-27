"""
PDF generation for emergency cards and medical records
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import os
from utils.qr_generator import generate_patient_qr, qr_to_bytes
import io


def generate_emergency_card(patient_data: dict, output_path: str) -> bool:
    """
    Generate emergency card PDF for patient

    Args:
        patient_data: Patient information dictionary
        output_path: Path to save PDF

    Returns:
        Success boolean
    """
    try:
        # Create PDF
        pdf = canvas.Canvas(output_path, pagesize=letter)
        width, height = letter

        # Header - Red background
        pdf.setFillColorRGB(0.93, 0.26, 0.26)  # Red
        pdf.rect(0, height - 2*inch, width, 2*inch, fill=True, stroke=False)

        # Title
        pdf.setFillColorRGB(1, 1, 1)  # White text
        pdf.setFont("Helvetica-Bold", 32)
        pdf.drawCentredString(width/2, height - 1*inch, "🆘 EMERGENCY CARD")

        pdf.setFont("Helvetica", 14)
        pdf.drawCentredString(width/2, height - 1.5*inch,
                              "Medical Records System")

        # Patient Name - Large
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica-Bold", 24)
        pdf.drawCentredString(width/2, height - 2.5*inch,
                              patient_data.get('full_name', 'N/A'))

        # National ID
        pdf.setFont("Helvetica", 12)
        pdf.setFillColorRGB(0.4, 0.4, 0.4)
        pdf.drawCentredString(width/2, height - 2.9*inch,
                              f"ID: {patient_data.get('national_id', 'N/A')}")

        # Divider line
        pdf.setStrokeColorRGB(0.8, 0.8, 0.8)
        pdf.setLineWidth(1)
        pdf.line(1*inch, height - 3.2*inch, width - 1*inch, height - 3.2*inch)

        # Critical Information Section
        y_position = height - 3.7*inch

        # Blood Type - Highlighted
        pdf.setFillColorRGB(0.93, 0.26, 0.26)
        pdf.roundRect(1*inch, y_position - 0.3*inch, 2 *
                      inch, 0.5*inch, 0.1*inch, fill=True)
        pdf.setFillColorRGB(1, 1, 1)
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(1.2*inch, y_position - 0.1*inch,
                       f"🩸 {patient_data.get('blood_type', 'Unknown')}")

        # Age & Gender
        pdf.setFillColorRGB(0, 0, 0)
        pdf.setFont("Helvetica", 12)
        pdf.drawString(3.5*inch, y_position,
                       f"Age: {patient_data.get('age', 'N/A')} years")
        pdf.drawString(5*inch, y_position,
                       f"Gender: {patient_data.get('gender', 'N/A')}")

        y_position -= 0.8*inch

        # Allergies - Red box if present
        allergies = patient_data.get('allergies', [])
        if allergies:
            pdf.setFillColorRGB(1, 0.95, 0.95)
            pdf.roundRect(1*inch, y_position - 0.8*inch, width -
                          2*inch, 1*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0.8, 0, 0)
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(1.2*inch, y_position - 0.2*inch, "⚠️ ALLERGIES:")

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica", 11)
            allergy_text = ", ".join(allergies)
            pdf.drawString(1.2*inch, y_position - 0.5*inch, allergy_text)

            y_position -= 1.2*inch
        else:
            pdf.setFont("Helvetica", 11)
            pdf.drawString(1*inch, y_position, "✓ No known allergies")
            y_position -= 0.4*inch

        # Chronic Diseases
        chronic = patient_data.get('chronic_diseases', [])
        if chronic:
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1*inch, y_position, "🏥 Chronic Conditions:")
            pdf.setFont("Helvetica", 11)
            chronic_text = ", ".join(chronic)
            pdf.drawString(1*inch, y_position - 0.25*inch, chronic_text)
            y_position -= 0.6*inch

        # Current Medications
        medications = patient_data.get('current_medications', [])
        if medications:
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1*inch, y_position, "💊 Current Medications:")
            y_position -= 0.3*inch

            pdf.setFont("Helvetica", 10)
            for i, med in enumerate(medications[:3], 1):  # Show first 3
                med_text = f"{i}. {med.get('name', 'N/A')} - {med.get('dosage', '')} {med.get('frequency', '')}"
                pdf.drawString(1.2*inch, y_position, med_text)
                y_position -= 0.25*inch

            y_position -= 0.2*inch

        # Emergency Contact
        emergency = patient_data.get('emergency_contact', {})
        if emergency:
            pdf.setFillColorRGB(0.95, 0.98, 1)
            pdf.roundRect(1*inch, y_position - 0.9*inch, width -
                          2*inch, 1*inch, 0.1*inch, fill=True)

            pdf.setFillColorRGB(0, 0, 0)
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(1.2*inch, y_position - 0.2 *
                           inch, "📞 Emergency Contact:")

            pdf.setFont("Helvetica", 11)
            pdf.drawString(1.2*inch, y_position - 0.45*inch,
                           f"{emergency.get('name', 'N/A')} ({emergency.get('relation', 'N/A')})")
            pdf.drawString(1.2*inch, y_position - 0.7*inch,
                           f"Phone: {emergency.get('phone', 'N/A')}")

            y_position -= 1.3*inch

        # QR Code
        try:
            qr_img = generate_patient_qr(patient_data.get('national_id', ''))
            qr_bytes = qr_to_bytes(qr_img)
            qr_image = RLImage(io.BytesIO(qr_bytes),
                               width=1.5*inch, height=1.5*inch)

            # Draw QR code
            pdf.drawImage(RLImage(io.BytesIO(qr_bytes), width=1.5*inch, height=1.5*inch),
                          width - 2.5*inch, 1*inch, width=1.5*inch, height=1.5*inch,
                          preserveAspectRatio=True, mask='auto')

            pdf.setFont("Helvetica", 8)
            pdf.setFillColorRGB(0.5, 0.5, 0.5)
            pdf.drawCentredString(width - 1.75*inch, 0.7 *
                                  inch, "Scan for quick access")
        except Exception as e:
            print(f"QR code generation error: {e}")

        # Footer
        pdf.setFont("Helvetica", 8)
        pdf.setFillColorRGB(0.5, 0.5, 0.5)
        pdf.drawString(
            1*inch, 0.7*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        pdf.drawCentredString(
            width/2, 0.5*inch, "MedLink - Unified Medical Records System")

        # Instructions at bottom
        pdf.setFont("Helvetica-Bold", 9)
        pdf.setFillColorRGB(0, 0, 0)
        pdf.drawString(1*inch, 0.3*inch,
                       "⚠️ KEEP THIS CARD WITH YOU AT ALL TIMES")

        # Save PDF
        pdf.save()
        return True

    except Exception as e:
        print(f"Error generating emergency card: {e}")
        return False


def generate_medical_record_pdf(patient_data: dict, visits: list,
                                lab_results: list, imaging_results: list,
                                output_path: str) -> bool:
    """
    Generate complete medical record PDF

    Args:
        patient_data: Patient information
        visits: List of visits
        lab_results: List of lab results
        imaging_results: List of imaging results
        output_path: Path to save PDF

    Returns:
        Success boolean
    """
    try:
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=12,
            spaceBefore=20
        )

        # Title
        story.append(Paragraph("🏥 Medical Records Report", title_style))
        story.append(Spacer(1, 0.3*inch))

        # Patient Information
        story.append(Paragraph("Patient Information", heading_style))

        patient_info = [
            ['Full Name:', patient_data.get('full_name', 'N/A')],
            ['National ID:', patient_data.get('national_id', 'N/A')],
            ['Date of Birth:', patient_data.get('date_of_birth', 'N/A')],
            ['Age:', f"{patient_data.get('age', 'N/A')} years"],
            ['Gender:', patient_data.get('gender', 'N/A')],
            ['Blood Type:', patient_data.get('blood_type', 'N/A')],
            ['Phone:', patient_data.get('phone', 'N/A')],
        ]

        patient_table = Table(patient_info, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        story.append(patient_table)
        story.append(Spacer(1, 0.3*inch))

        # Medical Alerts
        allergies = patient_data.get('allergies', [])
        chronic = patient_data.get('chronic_diseases', [])

        if allergies or chronic:
            story.append(Paragraph("⚠️ Medical Alerts", heading_style))

            if allergies:
                story.append(
                    Paragraph(f"<b>Allergies:</b> {', '.join(allergies)}", styles['Normal']))
            if chronic:
                story.append(Paragraph(
                    f"<b>Chronic Conditions:</b> {', '.join(chronic)}", styles['Normal']))

            story.append(Spacer(1, 0.2*inch))

        # Visit Summary
        story.append(
            Paragraph(f"📋 Medical Visits ({len(visits)} total)", heading_style))

        if visits:
            for visit in visits[:10]:  # Show last 10
                visit_text = f"<b>{visit.get('date', 'N/A')}</b> - {visit.get('doctor_name', 'N/A')}<br/>"
                visit_text += f"Diagnosis: {visit.get('diagnosis', 'N/A')}"
                story.append(Paragraph(visit_text, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("No visits recorded", styles['Normal']))

        story.append(Spacer(1, 0.2*inch))

        # Lab Results Summary
        story.append(
            Paragraph(f"🧪 Lab Results ({len(lab_results)} total)", heading_style))

        if lab_results:
            for result in lab_results[:5]:  # Show last 5
                lab_text = f"<b>{result.get('date', 'N/A')}</b> - {result.get('test_type', 'N/A')}<br/>"
                lab_text += f"Lab: {result.get('lab_name', 'N/A')} | Status: {result.get('status', 'N/A')}"
                story.append(Paragraph(lab_text, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(
                Paragraph("No lab results recorded", styles['Normal']))

        story.append(Spacer(1, 0.2*inch))

        # Imaging Results Summary
        story.append(
            Paragraph(f"📷 Imaging Results ({len(imaging_results)} total)", heading_style))

        if imaging_results:
            for result in imaging_results[:5]:  # Show last 5
                imaging_text = f"<b>{result.get('date', 'N/A')}</b> - {result.get('imaging_type', 'N/A')}<br/>"
                imaging_text += f"Body Part: {result.get('body_part', 'N/A')} | Center: {result.get('imaging_center', 'N/A')}"
                story.append(Paragraph(imaging_text, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(
                Paragraph("No imaging results recorded", styles['Normal']))

        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_text = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | MedLink Medical Records System"
        story.append(Paragraph(footer_text, ParagraphStyle('Footer', parent=styles['Normal'],
                                                           fontSize=8, textColor=colors.grey,
                                                           alignment=TA_CENTER)))

        # Build PDF
        doc.build(story)
        return True

    except Exception as e:
        print(f"Error generating medical record PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
