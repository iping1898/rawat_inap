from flask import Flask, render_template, request, redirect, make_response
import mysql.connector
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from io import BytesIO

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rawatinap_aripin'
}

def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

app = Flask(__name__) 

def get_next_id_transaksi():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(CAST(id_transaksi_aripin AS UNSIGNED)) FROM transaksi_aripin")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result[0] is None:
        return 1
    else:
        return result[0] + 1

@app.route('/', methods=['GET'])
def tampil():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                t.id_transaksi_aripin, 
                t.id_pasien_aripin, 
                p.nama_aripin, 
                k.kelas_aripin,
                k.harga_aripin, 
                r.tgl_masuk_aripin, 
                r.tgl_keluar_aripin,
                t.total_biaya_aripin,
                t.status_pembayaran_aripin,
                t.tgl_aripin
            FROM transaksi_aripin t 
            JOIN pasien_aripin p ON t.id_pasien_aripin = p.id_pasien_aripin 
            JOIN rawat_inap_aripin r ON p.id_pasien_aripin = r.id_pasien_aripin
            JOIN kamar_aripin k ON r.id_kamar_aripin = k.id_kamar_aripin
        """)
        transaksi = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('tampil.html', transaksi=transaksi)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('tampil.html', transaksi=[])

@app.route('/tampil_pasien', methods=['GET'])
def tampil_pasien():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin")
        pasien = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('tampil_pasien.html', pasien=pasien)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('tampil_pasien.html', pasien=[])

@app.route('/tabel', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        id_pasien_aripin = request.form['id_pasien_aripin']
        status_pembayaran_aripin = request.form['status_pembayaran_aripin']
        tgl_aripin = request.form['tgl_aripin']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            sql_rawat = """
                SELECT r.tgl_masuk_aripin, r.tgl_keluar_aripin, k.harga_aripin
                FROM rawat_inap_aripin r 
                JOIN kamar_aripin k ON r.id_kamar_aripin = k.id_kamar_aripin
                WHERE r.id_pasien_aripin = %s
            """
            cursor.execute(sql_rawat, (id_pasien_aripin,))
            rawat = cursor.fetchone()

            if not rawat:
                return "Data rawat inap tidak ditemukan untuk pasien ini."

            tgl_masuk = rawat['tgl_masuk_aripin']
            tgl_keluar = rawat['tgl_keluar_aripin']
            harga = rawat['harga_aripin']

            selisih = (tgl_keluar - tgl_masuk).days
            jumlah_hari = selisih if selisih > 0 else 1 

            total_biaya_aripin = jumlah_hari * harga

            id_transaksi_aripin = get_next_id_transaksi()

            sql_insert = """
                INSERT INTO transaksi_aripin
                (id_transaksi_aripin, id_pasien_aripin, total_biaya_aripin,
                 status_pembayaran_aripin, tgl_aripin)
                VALUES (%s, %s, %s, %s, %s)
            """
            val = (id_transaksi_aripin, id_pasien_aripin, total_biaya_aripin, 
                   status_pembayaran_aripin, tgl_aripin)

            cursor = conn.cursor()
            cursor.execute(sql_insert, val)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/')

        except Exception as e:
            return f"Gagal menyimpan data: {e}"

    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id_pasien_aripin, nama_aripin FROM pasien_aripin")
            pasien_list = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('index.html', pasien_list=pasien_list)
        except Exception as e:
            return render_template('index.html', pasien_list=[])


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

@app.route('/cetak_semua_pasien')
def cetak_semua_pasien():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pasien_aripin")
        data_pasien = cursor.fetchall()
        cursor.close()
        conn.close()

        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 16)
        
        pdf.cell(0, 10, 'Laporan Data Pasien', align='C', new_x='LMARGIN', new_y='NEXT')
        pdf.ln(5)

        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_fill_color(200, 220, 255)
        
        col_id = 30
        col_nama = 50
        col_alamat = 60
        col_kontak = 40

        pdf.cell(col_id, 10, 'ID Pasien', border=1, align='C', fill=True)
        pdf.cell(col_nama, 10, 'Nama', border=1, align='C', fill=True)
        pdf.cell(col_alamat, 10, 'Alamat', border=1, align='C', fill=True)
        pdf.cell(col_kontak, 10, 'Kontak', border=1, align='C', fill=True)
        pdf.ln()

        pdf.set_font('Helvetica', '', 10)
        for row in data_pasien:
            pdf.cell(col_id, 10, str(row['id_pasien_aripin']), border=1)
            pdf.cell(col_nama, 10, str(row['nama_aripin']), border=1)
            pdf.cell(col_alamat, 10, str(row['alamat_aripin']), border=1)
            pdf.cell(col_kontak, 10, str(row['kontak_aripin']), border=1)
            pdf.ln()

        pdf_bytes = pdf.output()
        
        response = make_response(bytes(pdf_bytes))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=laporan_pasien.pdf'
        return response

    except Exception as e:
        return f"<h1>Gagal Mencetak PDF</h1><p>Error: {e}</p>"

@app.route('/delete/<id_transaksi_aripin>')
def delete(id_transaksi_aripin):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM transaksi_aripin WHERE id_transaksi_aripin = %s"
        cursor.execute(sql, (id_transaksi_aripin,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/')
    except Exception as e:
        return f"Gagal menghapus: {e}"

@app.route('/edit/<id_transaksi_aripin>', methods=['GET', 'POST'])
def edit(id_transaksi_aripin):
    if request.method == 'POST':
        id_pasien_aripin = request.form['id_pasien_aripin']
        status_pembayaran_aripin = request.form['status_pembayaran_aripin']
        tgl_aripin = request.form['tgl_aripin']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT r.tgl_masuk_aripin, r.tgl_keluar_aripin, k.harga_aripin
                FROM rawat_inap_aripin r 
                JOIN kamar_aripin k ON r.id_kamar_aripin = k.id_kamar_aripin
                WHERE id_pasien_aripin = %s
            """, (id_pasien_aripin,))
            rawat = cursor.fetchone()

            if not rawat:
                return "Data rawat inap tidak ditemukan"

            selisih = (rawat['tgl_keluar_aripin'] - rawat['tgl_masuk_aripin']).days
            jumlah_hari = selisih if selisih > 0 else 1
            total_biaya_aripin = jumlah_hari * rawat['harga_aripin']

            sql = """
                UPDATE transaksi_aripin
                SET id_pasien_aripin = %s,
                    total_biaya_aripin = %s,
                    status_pembayaran_aripin = %s,
                    tgl_aripin = %s
                WHERE id_transaksi_aripin = %s
            """
            val = (id_pasien_aripin, total_biaya_aripin, status_pembayaran_aripin, 
                   tgl_aripin, id_transaksi_aripin)

            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/')
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM transaksi_aripin WHERE id_transaksi_aripin = %s", (id_transaksi_aripin,))
            transaksi = cursor.fetchone()
            cursor.execute("SELECT id_pasien_aripin, nama_aripin FROM pasien_aripin")
            pasien_list = cursor.fetchall()
            cursor.close()
            conn.close()
            return render_template('edit.html', transaksi=transaksi, pasien_list=pasien_list)
        except Exception as e:
            return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)