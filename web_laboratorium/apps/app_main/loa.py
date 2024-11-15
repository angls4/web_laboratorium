from fpdf import FPDF
from datetime import datetime
import locale

def generate_loa_pdf(pendaftaran):
    pdf = FPDF()
    pdf.add_page()

    # Font selection (try to find similar fonts to the original)
    pdf.set_font("Arial", size=10)

    # Header
    pdf.set_font("Arial", size=14, style="B")  # Bold for header
    pdf.cell(0, 10, "UNIVERSITAS MUHAMMADIYAH SURAKARTA", ln=True, align="C")
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 5, "FAKULTAS TEKNIK", ln=True, align="C")
    pdf.cell(0, 5, "LABORATORIUM TEKNIK INDUSTRI", ln=True, align="C")
    pdf.set_font("Arial", size=10)
    pdf.cell(
        0,
        5,
        "Gedung Umar Usman Lantai 2, Jl. A. Yani Tromol Pos I, Surakarta 57132",
        ln=True,
        align="C",
    )
    pdf.ln(5)  # Add some space

    # Set locale to Indonesian
    locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')

    # Get current date and format it
    current_date = datetime.now()
    formatted_current_date = current_date.strftime('%d %B %Y')
    # Date
    pdf.cell(0, 10, f"Surakarta, {formatted_current_date}", ln=True, align="R")

    # Title
    pdf.set_font("Arial", size=12, style="B")
    pdf.cell(0, 10, "HASIL OPEN RECRUITMENT", ln=True, align="C")
    pdf.cell(0, 5, f"ASISTEN {pendaftaran.persyaratan.__str__().upper()}", ln=True, align="C")
    pdf.ln(10)

    # Body
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(
        0,
        5,
        f"Berdasarkan hasil wawancara dengan karyawan, dengan sistem laboratorium, dan pengetahuan, dia tercatat dengan Eagle Laboratorium yang dilaksanakan dalam agenda Open Recruitment Asisten {pendaftaran.persyaratan}, dengan ini kami menyebutkan bahwa Saudara:",
    )
    pdf.ln(5)

    # Student Information (adjust spacing as needed)
    pdf.cell(30, 5, "Nama", ln=0)
    pdf.cell(5, 5, ":", ln=0)
    pdf.cell(0, 5, pendaftaran.user.first_name.upper(), ln=True)

    pdf.cell(30, 5, "NIM", ln=0)
    pdf.cell(5, 5, ":", ln=0)
    pdf.cell(0, 5, pendaftaran.user.nim.upper(), ln=True)

    pdf.cell(30, 5, "Dinyatakan", ln=0)
    pdf.cell(5, 5, ":", ln=0)
    pdf.set_font("Arial", size=10, style="B")  # Bold for result
    pdf.cell(0, 5, "DITERIMA", ln=True)
    pdf.set_font("Arial", size=10)  # Back to normal font

    pdf.cell(0, 5, f"Menjadi Asisten Praktikum {pendaftaran.praktikum}", ln=True)

    pdf.ln(5)

    pdf.multi_cell(
        0,
        5,
        "Jangan pernah menganggap dirimu hebat, meskipun rendah hati. Jangan pernah merasa malu dengan cara merendahkan orang lain. Bersikap rendah hati mereka yang rendah hati. Jangan sombong karena kalau tidak kamu, insyaAllah banyak mereka yang sesuatu yang berarti.",
    )
    pdf.ln(5)

    pdf.multi_cell(
        0,
        5,
        "Demikian pengumuman ini kami sampaikan. Apabila terdapat kata kami mohon maaf yang sebesar-besarnya.",
    )
    pdf.ln(10)

    # Signatures (adjust spacing)
    pdf.cell(0, 5, "Wassalamualaikum Warahmatullahi Wabarakatuh", ln=True, align="C")
    pdf.ln(15)

    pdf.cell(0, 5, "Hormat Kami,", ln=True, align="R")
    pdf.ln(10)

    pdf.cell(0, 5, "Tim Asisten", ln=True, align="R")
    pdf.cell(0, 5, pendaftaran.praktikum.__str__(), ln=True, align="R")

    # Footer (optional, add page number, etc.)

    # Output the PDF
    return pdf.output(dest='S').encode('latin1')

def loa_attatchment(pendaftaran):
    return (f"LOA_{pendaftaran.user.first_name.upper()}_{pendaftaran.user.nim.upper()}_{pendaftaran.praktikum.praktikum_name.upper()}.pdf", generate_loa_pdf(pendaftaran), "application/pdf")