from flask import make_response

@app.route('/cetak_pasien/<id_pasien_aripin>')
def cetak_pasien(id_pasien_aripin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin WHERE id_pasien_aripin = %s", (id_pasien_aripin,))
        pasien = cursor.fetchone()
        cursor.close()
        conn.close()

        if not pasien:
            return "Data pasien tidak ditemukan."

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Laporan Data Pasien', ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        pdf.cell(40, 10, f"ID Pasien: {pasien['id_pasien_aripin']}", ln=True)
        pdf.cell(40, 10, f"Nama: {pasien['nama_aripin']}", ln=True)
        pdf.cell(40, 10, f"Alamat: {pasien['alamat_aripin']}", ln=True)
        pdf.cell(40, 10, f"Kontak: {pasien['kontak_aripin']}", ln=True)

        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=pasien_{id_pasien_aripin}.pdf'
        return response
    except Exception as e:
        return f"Error: {e}"

@app.route('/cetak_semua_pasien')
def cetak_semua_pasien():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin")
        pasien_list = cursor.fetchall()
        cursor.close()
        conn.close()

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Laporan Semua Pasien', ln=True, align='C')
        pdf.ln(10)
        pdf.set_font('Arial', '', 12)
        for pasien in pasien_list:
            pdf.cell(0, 10, f"{pasien['id_pasien_aripin']} | {pasien['nama_aripin']} | {pasien['alamat_aripin']} | {pasien['kontak_aripin']}", ln=True)

        response = make_response(pdf.output(dest='S').encode('latin-1'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=semua_pasien.pdf'
        return response
    except Exception as e:
        return f"Error: {e}"


from fpdf.enums import XPos, YPos

@app.route('/cetak_pasien/<id_pasien_aripin>')
def cetak_pasien(id_pasien_aripin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin WHERE id_pasien_aripin = %s", (id_pasien_aripin,))
        pasien = cursor.fetchone()
        cursor.close()
        conn.close()

        if not pasien:
            return "Data pasien tidak ditemukan."

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)  # Gunakan Helvetica (core font)
        pdf.cell(0, 10, 'Laporan Data Pasien', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(10)
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(40, 10, f"ID Pasien: {pasien['id_pasien_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Nama: {pasien['nama_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Alamat: {pasien['alamat_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Kontak: {pasien['kontak_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')  # Masih bisa, tapi warning. Untuk versi terbaru:
        # from io import BytesIO
        # buffer = BytesIO()
        # pdf.output(buffer)
        # pdf_bytes = buffer.getvalue()

        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=pasien_{id_pasien_aripin}.pdf'
        return response
    except Exception as e:
        return f"Error: {e}"

@app.route('/cetak_pasien/<id_pasien_aripin>')
def cetak_pasien(id_pasien_aripin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin WHERE id_pasien_aripin = %s", (id_pasien_aripin,))
        pasien = cursor.fetchone()
        cursor.close()
        conn.close()

        if not pasien:
            return "Data pasien tidak ditemukan."

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, 'Laporan Data Pasien', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        pdf.ln(10)
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(40, 10, f"ID Pasien: {pasien['id_pasien_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Nama: {pasien['nama_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Alamat: {pasien['alamat_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(40, 10, f"Kontak: {pasien['kontak_aripin']}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        buffer = BytesIO()
        pdf.output(buffer)
        pdf_bytes = buffer.getvalue()
        response = make_response(pdf_bytes)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=pasien_{id_pasien_aripin}.pdf'
        return response
    except Exception as e:
        return f"Error: {e}"