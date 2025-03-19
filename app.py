from flask import Flask, render_template, request, session
import requests
from datetime import datetime
import datetime
import pytz

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



def ambil_data(url, retries=3, timeout=10):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        'XSRF-TOKEN': 'eyJpdiI6IkZXVGVRTi94eXhCTlh0YThEcmk2V2c9PSIsInZhbHVlIjoiTmJZdUJTQVlZcUhkbEhFL2lZbVZOZVV6WG1pNnBBQ1ptaUdoSzNZYTNCWkE3YlRtcWUxZUlpZWZjbnpzYklLcGErVzMxU0FiZGQrUEN5ZVZ6cDFlZnprN2h4K21YdnR0WnM3NE1JWEhtQVNMYm1jV2hzWll0WHpnbWNQNTZxOWYiLCJtYWMiOiIxMjMzZTE5NDA2NjgxZDIwZWU0Njk0NGZhMjcxYTY2M2E2MTRkYjhjODg5YjQ3OWFhN2Y1NWFiN2U4ZDZiMDVmIiwidGFnIjoiIn0%3D',
        '_ga': 'GA1.1.140722331.1727057868',
        '_ga_JQ088T32QP': 'GS1.1.1727061610.2.1.1727061629.0.0.0', 
        '_ga_VNWN27RPNX': 'GS1.3.1727061611.2.0.1727061611.60.0.0', 
        'ceri_session': 'eyJpdiI6InZvaUFCYThNNTFDVlZKbTFQZ21vVGc9PSIsInZhbHVlIjoiVVZvSVN1U3hqUUN1bkdsdTJJVFdtM0hTSDNLYVlVakJQQjFZN0tGNDI4T2tsRUZGZ2xTdVdTSFAvSHF0dE5qUGIwQlNBZ0xFeUxwYmcwT1luZDJCc051bEdWNnd4SkY5Sk13TXFaYitHd1IwTjBsTHgvcnZKcVB1T2FEVGVYbU0iLCJtYWMiOiI2NGZiYTE4Y2RhZTQ5NTQ0NDYyYzA0ZjViMGRhY2VlOTU0OWU2MGNlY2NmM2I2MDVlNzk4ZGU1NDM5M2FmYzM5IiwidGFnIjoiIn0%3D',
        'cookiesession1': '678B28C4BA1B09254D21278D87A606A5',
        'jr_cookie': '98122d81101bed08eedde6ce20feda67',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6IlEyVEJBcW9Za2tCUFNJWFpvV2VUNGc9PSIsInZhbHVlIjoiM0NwSGwwdUVwbEVhVGtKVm5hdGJSbUxmSlpUQ0JjZkZPL0pFbEE5K3c3WmtPM3RpZHpkaUlhaldXMThRVlQzNnNKNVcxdTdaTDBMdWttOTlOUDd0cmwvQm50WXBiN2lMVlpSV213Umw2d0lpOUNaSzI4TjNoQ0xraENqRmRON3haWU1ROHVrZTlvZTdxdGM2SUtDME5BPT0iLCJtYWMiOiI0MWUxNTY1MjE5YzBiOTAxZmQwYzcwM2RkMzQwMTViYmU0NDI1OTg5MjY1NDgzZDdmYTliNTMwZWMxNDQwOGUyIiwidGFnIjoiIn0%3D'
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
        'XSRF-TOKEN': 'eyJpdiI6IkZXVGVRTi94eXhCTlh0YThEcmk2V2c9PSIsInZhbHVlIjoiTmJZdUJTQVlZcUhkbEhFL2lZbVZOZVV6WG1pNnBBQ1ptaUdoSzNZYTNCWkE3YlRtcWUxZUlpZWZjbnpzYklLcGErVzMxU0FiZGQrUEN5ZVZ6cDFlZnprN2h4K21YdnR0WnM3NE1JWEhtQVNMYm1jV2hzWll0WHpnbWNQNTZxOWYiLCJtYWMiOiIxMjMzZTE5NDA2NjgxZDIwZWU0Njk0NGZhMjcxYTY2M2E2MTRkYjhjODg5YjQ3OWFhN2Y1NWFiN2U4ZDZiMDVmIiwidGFnIjoiIn0%3D',
        '_ga': 'GA1.1.140722331.1727057868',
        '_ga_JQ088T32QP': 'GS1.1.1727061610.2.1.1727061629.0.0.0', 
        '_ga_VNWN27RPNX': 'GS1.3.1727061611.2.0.1727061611.60.0.0', 
        'ceri_session': 'eyJpdiI6InZvaUFCYThNNTFDVlZKbTFQZ21vVGc9PSIsInZhbHVlIjoiVVZvSVN1U3hqUUN1bkdsdTJJVFdtM0hTSDNLYVlVakJQQjFZN0tGNDI4T2tsRUZGZ2xTdVdTSFAvSHF0dE5qUGIwQlNBZ0xFeUxwYmcwT1luZDJCc051bEdWNnd4SkY5Sk13TXFaYitHd1IwTjBsTHgvcnZKcVB1T2FEVGVYbU0iLCJtYWMiOiI2NGZiYTE4Y2RhZTQ5NTQ0NDYyYzA0ZjViMGRhY2VlOTU0OWU2MGNlY2NmM2I2MDVlNzk4ZGU1NDM5M2FmYzM5IiwidGFnIjoiIn0%3D',
        'cookiesession1': '678B28C4BA1B09254D21278D87A606A5',
        'jr_cookie': '98122d81101bed08eedde6ce20feda67',
        'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d': 'eyJpdiI6IlEyVEJBcW9Za2tCUFNJWFpvV2VUNGc9PSIsInZhbHVlIjoiM0NwSGwwdUVwbEVhVGtKVm5hdGJSbUxmSlpUQ0JjZkZPL0pFbEE5K3c3WmtPM3RpZHpkaUlhaldXMThRVlQzNnNKNVcxdTdaTDBMdWttOTlOUDd0cmwvQm50WXBiN2lMVlpSV213Umw2d0lpOUNaSzI4TjNoQ0xraENqRmRON3haWU1ROHVrZTlvZTdxdGM2SUtDME5BPT0iLCJtYWMiOiI0MWUxNTY1MjE5YzBiOTAxZmQwYzcwM2RkMzQwMTViYmU0NDI1OTg5MjY1NDgzZDdmYTliNTMwZWMxNDQwOGUyIiwidGFnIjoiIn0%3D'
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
    indonesia_tz = pytz.timezone('Asia/Jakarta')  # WIB (GMT+7), bisa diganti 'Asia/Makassar' untuk WITA, 'Asia/Jayapura' untuk WIT
    current_year = datetime.datetime.now(indonesia_tz).year
    previous_year = current_year - 1
    
    
    today = datetime.datetime.now(indonesia_tz)
    today_form = datetime.datetime.now(indonesia_tz).strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    now = datetime.datetime.now(indonesia_tz).date()
    yesterday = now - datetime.timedelta(days=1)


    # Default values
    
    
    start_date_2024 = f"{today.year}-01-01"
    end_date_2024 = today_form

    
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
                           end_date_2024=end_date_2024, today=today, today_form=today_form,
                           data_2024_sigap_instansi=data_2024_sigap_instansi or [],
                           data_2024=data_2024 or [])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5550)