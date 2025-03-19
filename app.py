from flask import Flask, render_template, request, session
import requests
from datetime import datetime

def format_rupiah(value):
    
    try:
        value = float(value)  # Konversi ke float jika perlu
        formatted_value = "Rp{:,.2f}".format(value).replace(',', '.').replace('.', ',', 1)
        return formatted_value
    except (ValueError, TypeError):
        return "Rp0,00"



app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Gantilah dengan kunci rahasia yang lebih aman
app.jinja_env.filters['format_rupiah'] = format_rupiah  # Daftarkan filter

def get_default_dates(year):
    return f"{year}-01-01", f"{year}-12-31"

def ambil_data(url, retries=3, timeout=10):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6Ik1MR2ZMb2dwcnhCWVYybzkrRTdJV1E9PSIsInZhbHVlIjoidUVTTE5jVzdiUThONUt1Ykh1QVlJTU5jTnVrcHc4aUczWGJiWTVjWFFvZFVaUkV1T2d5b2gwMXVjYlpIaW03RkUyZmtBaFp4SXRuWWo3LzRzZmN2MEQvWUNpeVBQaE5DZ0xQVTFHVW1DZzhCN2QrTVJRSHYyWVczOXBOUDF5MnEiLCJtYWMiOiI4MmIzYmY0MDA1ZjhmZTYwYTA2Y2Y1NDM0OGNmNzdjN2U4YjliZjMzNmQ1MTFiMzA1MmJkOGJjZjUyZjJlMGJjIiwidGFnIjoiIn0%3D',
        '_ga': 'GA1.1.140722331.1727057868',
        '_ga_JQ088T32QP': 'GS1.1.1727061610.2.1.1727061629.0.0.0', 
        '_ga_VNWN27RPNX': 'GS1.3.1727061611.2.0.1727061611.60.0.0', 
        'ceri_session': 'eyJpdiI6IlNDclZjeHlIcVVKQVRCUzlCcDFWMlE9PSIsInZhbHVlIjoiYW5RTHlrTXloUkhqZDdqdnovL1diNlFlczFuY241eFdJSHRBcFFxdHQremNKMG9kTEJmOG9XMDZ5bFFwa1h1Q3E2ZWd3RmZ1S29WTlFTcHp5YnZYNGl0N3Q5NHZ6NWxVOWtYbFI4d1d1VzB6ay9wamV4VEFkbW1pODBmV1FtTWMiLCJtYWMiOiI2YjI2N2RlZTQwMGZjYTliNzEwYWVlMmNiN2M4Y2FkZjlkYmY1YWJiYTVlZWM5YzQyYjJhYTM5M2M1Mzc2YmNiIiwidGFnIjoiIn0%3D',
        'cookiesession1': '678B28C4BA1B09254D21278D87A606A5',
        'jr_cookie': 'c686aabd2eea2ae0eedde6ceabf2da67',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6IklZUjRMeExtYTFtTU9rM0t6YXBrOWc9PSIsInZhbHVlIjoiZVFVOWJ2Wk9scmp3bWx1eEVONGZxR0J4bG01bGpmd0FSZVNYVG9YSlQ3eUxiVTBacUxacC9xS1RMN09QdFFkYkZ2TTV1VFhrd2ZUV1Bxb3BvVzBXSzFFOGxpNkRjcnpCaEFtVVRSdUNEZSt6UVc2amUxVG1YcFE1V2ZhNUhBdmtOUnVuWms4WjlESDhTYUd1dHUrbmN3PT0iLCJtYWMiOiIzMmViMjQzOWQyZjI2YjQ2YzZiYjAyNTczZDY0MGJiMjZjZGExMDI3ZDk1YTg5ZGJiZDk0NDY4ZjE3ZTc2NGQ1IiwidGFnIjoiIn0%3D'
    }

    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    try:
        response = session.get(url, headers=headers, timeout=timeout)
        if response.status_code == 200:
            try:
                data = response.json()
                return [
                    {
                        'kode_kantor': item['kode_kantor'],
                        'nama_kantor': item['nama_kantor'],
                        'target': item['target'],
                        'realisasi': item['realisasi'],
                        'real_persen': item['real_persen'],
                        'jml_nopol': item['jml_nopol'],
                        'os_sw_before': item['os_sw_before'],
                        'os_sw_after': item['os_sw_after'],
                        'sw_terkutip': item['sw_terkutip'],
                        'sw_terkutip_persen': item['sw_terkutip_persen'],
                        'jenis_laporan': item['jenis_laporan']
                    }
                    for item in data.get('data', [])
                ]
            except ValueError:
                print("Response tidak dalam format JSON")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
    
    return None  # Kembalikan None jika terjadi error

def ambil_data_sigap_instansi(url, retries=3, timeout=10):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6Ik1MR2ZMb2dwcnhCWVYybzkrRTdJV1E9PSIsInZhbHVlIjoidUVTTE5jVzdiUThONUt1Ykh1QVlJTU5jTnVrcHc4aUczWGJiWTVjWFFvZFVaUkV1T2d5b2gwMXVjYlpIaW03RkUyZmtBaFp4SXRuWWo3LzRzZmN2MEQvWUNpeVBQaE5DZ0xQVTFHVW1DZzhCN2QrTVJRSHYyWVczOXBOUDF5MnEiLCJtYWMiOiI4MmIzYmY0MDA1ZjhmZTYwYTA2Y2Y1NDM0OGNmNzdjN2U4YjliZjMzNmQ1MTFiMzA1MmJkOGJjZjUyZjJlMGJjIiwidGFnIjoiIn0%3D',
        '_ga': 'GA1.1.140722331.1727057868',
        '_ga_JQ088T32QP': 'GS1.1.1727061610.2.1.1727061629.0.0.0', 
        '_ga_VNWN27RPNX': 'GS1.3.1727061611.2.0.1727061611.60.0.0', 
        'ceri_session': 'eyJpdiI6IlNDclZjeHlIcVVKQVRCUzlCcDFWMlE9PSIsInZhbHVlIjoiYW5RTHlrTXloUkhqZDdqdnovL1diNlFlczFuY241eFdJSHRBcFFxdHQremNKMG9kTEJmOG9XMDZ5bFFwa1h1Q3E2ZWd3RmZ1S29WTlFTcHp5YnZYNGl0N3Q5NHZ6NWxVOWtYbFI4d1d1VzB6ay9wamV4VEFkbW1pODBmV1FtTWMiLCJtYWMiOiI2YjI2N2RlZTQwMGZjYTliNzEwYWVlMmNiN2M4Y2FkZjlkYmY1YWJiYTVlZWM5YzQyYjJhYTM5M2M1Mzc2YmNiIiwidGFnIjoiIn0%3D',
        'cookiesession1': '678B28C4BA1B09254D21278D87A606A5',
        'jr_cookie': 'c686aabd2eea2ae0eedde6ceabf2da67',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6IklZUjRMeExtYTFtTU9rM0t6YXBrOWc9PSIsInZhbHVlIjoiZVFVOWJ2Wk9scmp3bWx1eEVONGZxR0J4bG01bGpmd0FSZVNYVG9YSlQ3eUxiVTBacUxacC9xS1RMN09QdFFkYkZ2TTV1VFhrd2ZUV1Bxb3BvVzBXSzFFOGxpNkRjcnpCaEFtVVRSdUNEZSt6UVc2amUxVG1YcFE1V2ZhNUhBdmtOUnVuWms4WjlESDhTYUd1dHUrbmN3PT0iLCJtYWMiOiIzMmViMjQzOWQyZjI2YjQ2YzZiYjAyNTczZDY0MGJiMjZjZGExMDI3ZDk1YTg5ZGJiZDk0NDY4ZjE3ZTc2NGQ1IiwidGFnIjoiIn0%3D'
    }

    session.cookies.update(cookies)

    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }
    
    try:
        response = session.get(url, headers=headers, timeout=timeout)

        if response.status_code == 200:
            try:
                data = response.json()
                result = []

                for item in data['data']:
                    result.append({
                        'kode_kantor': item['kode_kantor'],
                        'nama_kantor': item['nama_kantor'],
                        'jml_nopol': item['jml_nopol'],
                        'os_sw_before': item['os_sw_before'],
                        'os_sw_after': item['os_sw_after'],
                        'sw_terkutip': item['sw_terkutip'],
                        'sw_terkutip_persen': item['sw_terkutip_persen'],
                        'jenis_laporan': item['jenis_laporan']
                    })

                return result
            except ValueError:
                print("Response tidak dalam format JSON")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None
    
@app.context_processor
def utility_processor():
    return dict(format_rupiah=format_rupiah)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    current_year = datetime.now().year
    previous_year = current_year - 1
    
    today = datetime.today().strftime('%Y-%m-%d')  # Ambil tanggal hari ini

    # Default values
    
    start_date_2024, end_date_2024 = get_default_dates(current_year)

    
    data_2024 = None
    
    data_2024_sigap_instansi = None

    if request.method == 'POST':
        
        start_date_2024 = request.form.get('start_date_2024', start_date_2024)
        end_date_2024 = request.form.get('end_date_2024', end_date_2024)

        
        url_2024 = f'https://ceri.jasaraharja.co.id/monitoring/operasi_gabungan/datatables/{start_date_2024}_{end_date_2024}_0400001_1'
        
        url_2024_sigap_instansi = f'https://ceri.jasaraharja.co.id/monitoring/crm_sigap/datatables/{start_date_2024}_{end_date_2024}_0400001_1'
        

        
        data_2024 = ambil_data(url_2024)
        
        data_2024_sigap_instansi = ambil_data_sigap_instansi(url_2024_sigap_instansi)
        
        

    return render_template('index.html',
                           previous_year=previous_year,
                           current_year=current_year,
                           start_date_2024=start_date_2024,
                           end_date_2024=end_date_2024, today=today,
                           data_2024_sigap_instansi=data_2024_sigap_instansi or [],
                           data_2024=data_2024 or [])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5550)