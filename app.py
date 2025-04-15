from flask import Flask, render_template, request, session
import requests
from datetime import datetime
import datetime
import pytz
from collections import defaultdict


def format_rupiah(value):
    try:
        value = float(value)  # Konversi ke float jika perlu
        formatted_value = "{:,.2f}".format(
            value
        )  # Format angka dengan pemisah ribuan koma
        formatted_value = (
            formatted_value.replace(",", "X").replace(".", ",").replace("X", ".")
        )  # Tukar simbol dengan benar
        return f"Rp{formatted_value}"
    except (ValueError, TypeError):
        return "Rp0,00"


app = Flask(__name__)
app.secret_key = "supersecretkey"  # Gantilah dengan kunci rahasia yang lebih aman
app.jinja_env.filters["format_rupiah"] = format_rupiah  # Daftarkan filter


def ambil_data(url, retries=3):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        "XSRF-TOKEN": "eyJpdiI6IkFwcGJDRzZOLzEraHNDbU9EMm40S3c9PSIsInZhbHVlIjoiU1B1TDhPaU9Fejlhc1RnRFJTU0tLbHc2a0lHK2FhSkVqKzhubDJqTUtHN1FKUVVFVVdJbkkwTTZPQzRKY3dqZE5OaUwrTEY5djY2UlFBbjgyMDlSd3o5SThUQkZVR3R1M1lkTG51K2hxcWljTS9mQ1NWd2xiTHpZbVFyS2ZHU1AiLCJtYWMiOiJmMDNjNjE4YTQzNDIxYWMxNTUxNTExZjhhYmM4YjM3MGM4YzM5M2ZjYmNkNjUyZmZhZTJiODgzYTk3MjFkZDYxIiwidGFnIjoiIn0%3D",
        "_ga": "GA1.1.140722331.1727057868",
        "_ga_JQ088T32QP": "GS1.1.1727061610.2.1.1727061629.0.0.0",
        "_ga_VNWN27RPNX": "GS1.3.1727061611.2.0.1727061611.60.0.0",
        "ceri_session": "eyJpdiI6IkJxVjA1eW9COG1Tekx6Z01JZG5JcUE9PSIsInZhbHVlIjoiaVlPZHdiWWZ3alpJd0lGTmR1OCswVkVJdTBBbjR3TGp6cDVORWJ6bWErUFU5MERjTUExRE9GWVJ0Rm5BUFZpV3lTZzJyS1VjVHN2OVA1M0oxRG5vT2pmTStxQmk3R01aTFFjRXZMMGM1QjduUDVYYmxNTWJqVkVNZU9KbmFRMlIiLCJtYWMiOiJlZGI3YTQyMTllZGRiODIxMGExODk1NGNmYjcwZGY1ZWQ3NmU2OWI1MTYwNDhiNzExZGNiMWJhMGZiZWZmM2IxIiwidGFnIjoiIn0%3D",
        "cookiesession1": "678B28C4BA1B09254D21278D87A606A5",
        "jr_cookie": "c686aabd2eea2ae0eedde6ce5ccefd67",
        "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6Imp5WFljRklINklVNGpEUk10WXhqL1E9PSIsInZhbHVlIjoiOFptenpqbE03bTM5Ly9iSkRuRm9RQ0FuZGJwMzFESk52anlXbWFwZTVDZ1ZTcENwdGZqdGN0NVdPYytqUDd0ZG1kckw5K05ibnVacmhENWQ0R1pwcUdDZGd6UUJwVm1oQVdaL0ZVc1FUMGVKRyt3SU5oZ2l4Q3E3NWtJcS91VGpWWW1Td1l4ellPK2NHZVRWbXlWOHBRPT0iLCJtYWMiOiIzMWMzODU4ZmI5YWVjZDcwZDE5MzZhNmFiZjBjODFlNjg5ZGUyYzY0ZDc4N2M2MDA2Y2YxMTE2ZTIyMDY3MTdlIiwidGFnIjoiIn0%3D",
    }

    session.cookies.update(cookies)

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                return [
                    {
                        "kode_kantor": item["kode_kantor"],
                        "nama_kantor": item["nama_kantor"],
                        "target": item["target"],
                        "realisasi": item["realisasi"],
                        "real_persen": item["real_persen"],
                        "jml_nopol": item["jml_nopol"],
                        "os_sw_before": item["os_sw_before"],
                        "os_sw_after": item["os_sw_after"],
                        "sw_terkutip": item["sw_terkutip"],
                        "sw_terkutip_persen": item["sw_terkutip_persen"],
                        "jenis_laporan": item["jenis_laporan"],
                    }
                    for item in data.get("data", [])
                ]
            except ValueError:
                print("Response tidak dalam format JSON")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

    return None  # Kembalikan None jika terjadi error


def ambil_data_sigap_instansi(url, retries=3):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        "XSRF-TOKEN": "eyJpdiI6IkFwcGJDRzZOLzEraHNDbU9EMm40S3c9PSIsInZhbHVlIjoiU1B1TDhPaU9Fejlhc1RnRFJTU0tLbHc2a0lHK2FhSkVqKzhubDJqTUtHN1FKUVVFVVdJbkkwTTZPQzRKY3dqZE5OaUwrTEY5djY2UlFBbjgyMDlSd3o5SThUQkZVR3R1M1lkTG51K2hxcWljTS9mQ1NWd2xiTHpZbVFyS2ZHU1AiLCJtYWMiOiJmMDNjNjE4YTQzNDIxYWMxNTUxNTExZjhhYmM4YjM3MGM4YzM5M2ZjYmNkNjUyZmZhZTJiODgzYTk3MjFkZDYxIiwidGFnIjoiIn0%3D",
        "_ga": "GA1.1.140722331.1727057868",
        "_ga_JQ088T32QP": "GS1.1.1727061610.2.1.1727061629.0.0.0",
        "_ga_VNWN27RPNX": "GS1.3.1727061611.2.0.1727061611.60.0.0",
        "ceri_session": "eyJpdiI6IkJxVjA1eW9COG1Tekx6Z01JZG5JcUE9PSIsInZhbHVlIjoiaVlPZHdiWWZ3alpJd0lGTmR1OCswVkVJdTBBbjR3TGp6cDVORWJ6bWErUFU5MERjTUExRE9GWVJ0Rm5BUFZpV3lTZzJyS1VjVHN2OVA1M0oxRG5vT2pmTStxQmk3R01aTFFjRXZMMGM1QjduUDVYYmxNTWJqVkVNZU9KbmFRMlIiLCJtYWMiOiJlZGI3YTQyMTllZGRiODIxMGExODk1NGNmYjcwZGY1ZWQ3NmU2OWI1MTYwNDhiNzExZGNiMWJhMGZiZWZmM2IxIiwidGFnIjoiIn0%3D",
        "cookiesession1": "678B28C4BA1B09254D21278D87A606A5",
        "jr_cookie": "c686aabd2eea2ae0eedde6ce5ccefd67",
        "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6Imp5WFljRklINklVNGpEUk10WXhqL1E9PSIsInZhbHVlIjoiOFptenpqbE03bTM5Ly9iSkRuRm9RQ0FuZGJwMzFESk52anlXbWFwZTVDZ1ZTcENwdGZqdGN0NVdPYytqUDd0ZG1kckw5K05ibnVacmhENWQ0R1pwcUdDZGd6UUJwVm1oQVdaL0ZVc1FUMGVKRyt3SU5oZ2l4Q3E3NWtJcS91VGpWWW1Td1l4ellPK2NHZVRWbXlWOHBRPT0iLCJtYWMiOiIzMWMzODU4ZmI5YWVjZDcwZDE5MzZhNmFiZjBjODFlNjg5ZGUyYzY0ZDc4N2M2MDA2Y2YxMTE2ZTIyMDY3MTdlIiwidGFnIjoiIn0%3D",
    }

    session.cookies.update(cookies)

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    try:
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                result = []

                for item in data["data"]:
                    result.append(
                        {
                            "kode_kantor": item["kode_kantor"],
                            "nama_kantor": item["nama_kantor"],
                            "jml_nopol": item["jml_nopol"],
                            "os_sw_before": item["os_sw_before"],
                            "os_sw_after": item["os_sw_after"],
                            "sw_terkutip": item["sw_terkutip"],
                            "sw_terkutip_persen": item["sw_terkutip_persen"],
                            "jenis_laporan": item["jenis_laporan"],
                        }
                    )

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


def ambil_data_merchant(url, retries=3):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        "XSRF-TOKEN": "eyJpdiI6Ik93S3E0L0FlOGN6Skk3amhHMDNrQ1E9PSIsInZhbHVlIjoiOVpySjBwc2NXYnhqTkN1VUE4YlE0UjZ1d3ZFMmpBSS9JZk1zRWNRR0dJcVR5RWJGSGJVVHd3cTdYOFZaM3BBSmxsK2RhYkZyNEFXZ2RiNnliU0lpZ3M3SzFtRTZramlJRjdNMmpaKzBsMHh5d20vQTRzVnV2RnNSSXQ0T0tMVGUiLCJtYWMiOiI0MTEwNTcyMWMyYjc0MWE0Yjk0YWNjY2E5MWVmZDRhOGIwNDAwZTk1NGFlMjM0ZWEyNTk4ZmZkYTYzYzNiODU1IiwidGFnIjoiIn0%3D",
        "_ga": "GA1.1.140722331.1727057868",
        "_ga_JQ088T32QP": "GS1.1.1727061610.2.1.1727061629.0.0.0",
        "_ga_VNWN27RPNX": "GS1.3.1727061611.2.0.1727061611.60.0.0",
        "cookiesession1": "678B28E3D57096F3CACCD7149E1DBECE",
        "jrreward_session": "eyJpdiI6ImordTczdVlUN0tTdWtaZkQrbzl5S2c9PSIsInZhbHVlIjoiRytJUnc3Yzl5QnBWclhTTkRhWnQzMTFMZGZWdzNHOVNWc3ZreFRUS0Q5d3NCb2VoODBUYUwyT0ltbDQ2OEV1MEdoNXVKTTZyTi9oRHZjRS96M0w3UW1mVUtyN2x3azFzRmdMZjNMZmMyNTFzVXArMDJzaStCVmpwSGhYQzV4SmYiLCJtYWMiOiJlNDlkZjM0ODJjM2U1NDAzODZjOWY2MjNhM2QyNjBhNjExMzc0NThkM2JjMGExZmM4OWQ5NWRhMjQxMjM1ZmZiIiwidGFnIjoiIn0%3D",
        "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6IlVGZ3ViU3VKbWR4YW1adWpucjkzNVE9PSIsInZhbHVlIjoialF5blJ6blBxdG9DVTBuRG05ZGROWmFzUWNNVEpjUXpINk1TKzNhZ0ZnUVA1d2FvdzdwQnAzeWtoeUpCNWZrT1phc1JvTWNOZ2szRVpwWUtmcGY0RCtJaC92a1VrclhtMmRWbTNhSnQ3NXczcGdpUFo0SXVtY1hqWmNUa1dPdysxUWpzTjNrNVBFRjlzbTNWeW1mSTRVYkpDTXpHRjNTd1p0VG1IYldnbkc1bnpITVcwNkI4dC8rYVhlTmRiK0p1MFpMT1pKbTMvQmZlUUN5MnV2NnM5Sk10WUlOQm15SUNHNlJnV1ZhbjRkUT0iLCJtYWMiOiI4ZjdiZGZjNzc3MDNhY2I1ZjAzZGM1Y2E5YTA2MjM2OTM5NGFjOGFiZDBiNzg3OWVjMGJkMmExZTliNzY3OTU2IiwidGFnIjoiIn0%3D",
    }

    session.cookies.update(cookies)

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    try:
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                result = []

                for item in data["data"]:
                    result.append(
                        {
                            "merchant_name": item["merchant_name"],
                            "campaign_name": item["campaign_name"],
                            "name": item["name"],
                            "no_polisi": item["no_polisi"],
                            "email": item["email"],
                            "code": item["code"],
                            "status": item["status"],
                            "created_at": item["created_at"],
                            "area": item["area"],
                        }
                    )

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


def ambil_data_merchant_merchant(url, retries=3):
    session = requests.Session()

    # Masukkan cookies yang relevan dari browser Anda ke sini
    cookies = {
        "XSRF-TOKEN": "eyJpdiI6Ik93S3E0L0FlOGN6Skk3amhHMDNrQ1E9PSIsInZhbHVlIjoiOVpySjBwc2NXYnhqTkN1VUE4YlE0UjZ1d3ZFMmpBSS9JZk1zRWNRR0dJcVR5RWJGSGJVVHd3cTdYOFZaM3BBSmxsK2RhYkZyNEFXZ2RiNnliU0lpZ3M3SzFtRTZramlJRjdNMmpaKzBsMHh5d20vQTRzVnV2RnNSSXQ0T0tMVGUiLCJtYWMiOiI0MTEwNTcyMWMyYjc0MWE0Yjk0YWNjY2E5MWVmZDRhOGIwNDAwZTk1NGFlMjM0ZWEyNTk4ZmZkYTYzYzNiODU1IiwidGFnIjoiIn0%3D",
        "_ga": "GA1.1.140722331.1727057868",
        "_ga_JQ088T32QP": "GS1.1.1727061610.2.1.1727061629.0.0.0",
        "_ga_VNWN27RPNX": "GS1.3.1727061611.2.0.1727061611.60.0.0",
        "cookiesession1": "678B28E3D57096F3CACCD7149E1DBECE",
        "jrreward_session": "eyJpdiI6ImordTczdVlUN0tTdWtaZkQrbzl5S2c9PSIsInZhbHVlIjoiRytJUnc3Yzl5QnBWclhTTkRhWnQzMTFMZGZWdzNHOVNWc3ZreFRUS0Q5d3NCb2VoODBUYUwyT0ltbDQ2OEV1MEdoNXVKTTZyTi9oRHZjRS96M0w3UW1mVUtyN2x3azFzRmdMZjNMZmMyNTFzVXArMDJzaStCVmpwSGhYQzV4SmYiLCJtYWMiOiJlNDlkZjM0ODJjM2U1NDAzODZjOWY2MjNhM2QyNjBhNjExMzc0NThkM2JjMGExZmM4OWQ5NWRhMjQxMjM1ZmZiIiwidGFnIjoiIn0%3D",
        "remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d": "eyJpdiI6IlVGZ3ViU3VKbWR4YW1adWpucjkzNVE9PSIsInZhbHVlIjoialF5blJ6blBxdG9DVTBuRG05ZGROWmFzUWNNVEpjUXpINk1TKzNhZ0ZnUVA1d2FvdzdwQnAzeWtoeUpCNWZrT1phc1JvTWNOZ2szRVpwWUtmcGY0RCtJaC92a1VrclhtMmRWbTNhSnQ3NXczcGdpUFo0SXVtY1hqWmNUa1dPdysxUWpzTjNrNVBFRjlzbTNWeW1mSTRVYkpDTXpHRjNTd1p0VG1IYldnbkc1bnpITVcwNkI4dC8rYVhlTmRiK0p1MFpMT1pKbTMvQmZlUUN5MnV2NnM5Sk10WUlOQm15SUNHNlJnV1ZhbjRkUT0iLCJtYWMiOiI4ZjdiZGZjNzc3MDNhY2I1ZjAzZGM1Y2E5YTA2MjM2OTM5NGFjOGFiZDBiNzg3OWVjMGJkMmExZTliNzY3OTU2IiwidGFnIjoiIn0%3D",
    }

    session.cookies.update(cookies)

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    try:
        response = session.get(url, headers=headers)

        if response.status_code == 200:
            try:
                data = response.json()
                result = []

                for item in data["data"]:
                    result.append(
                        {
                            "data_id": item["data_id"],
                            "users": item["users"],
                            "phone": item["phone"],
                            "cities_id": item["cities_id"],
                            "users_id": item["users_id"],
                            "name": item["name"],
                            "wilayah": item["wilayah"],
                            "category_name": item["category_name"],
                            "status": item["status"],
                        }
                    )

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


WILAYAH_KE_KANTOR = {
    # 0400 - KANTOR WILAYAH JAWA TENGAH
    "Demak": "0400 - KANTOR WILAYAH JAWA TENGAH",
    "Grobogan": "0400 - KANTOR WILAYAH JAWA TENGAH",
    "Kendal": "0400 - KANTOR WILAYAH JAWA TENGAH",
    "Salatiga": "0400 - KANTOR WILAYAH JAWA TENGAH",
    # 0401 - KANTOR CABANG SURAKARTA
    "Boyolali": "0401 - KANTOR CABANG SURAKARTA",
    "Klaten": "0401 - KANTOR CABANG SURAKARTA",
    "Sragen": "0401 - KANTOR CABANG SURAKARTA",
    "Surakarta": "0401 - KANTOR CABANG SURAKARTA",
    # 0402 - KANTOR CABANG MAGELANG
    "Kebumen": "0402 - KANTOR CABANG MAGELANG",
    "Magelang": "0402 - KANTOR CABANG MAGELANG",
    "Purworejo": "0402 - KANTOR CABANG MAGELANG",
    "Temanggung": "0402 - KANTOR CABANG MAGELANG",
    "Wonosobo": "0402 - KANTOR CABANG MAGELANG",
    # 0403 - KANTOR CABANG PURWOKERTO
    "Banjarnegara": "0403 - KANTOR CABANG PURWOKERTO",
    "Banyumas": "0403 - KANTOR CABANG PURWOKERTO",
    "Cilacap": "0403 - KANTOR CABANG PURWOKERTO",
    "Purbalingga": "0403 - KANTOR CABANG PURWOKERTO",
    # 0404 - KANTOR CABANG PEKALONGAN
    "Batang": "0404 - KANTOR CABANG PEKALONGAN",
    "Brebes": "0404 - KANTOR CABANG PEKALONGAN",
    "Pekalongan": "0404 - KANTOR CABANG PEKALONGAN",
    "Pemalang": "0404 - KANTOR CABANG PEKALONGAN",
    "Tegal": "0404 - KANTOR CABANG PEKALONGAN",
    # 0405 - KANTOR CABANG PATI
    "Blora": "0405 - KANTOR CABANG PATI",
    "Jepara": "0405 - KANTOR CABANG PATI",
    "Kudus": "0405 - KANTOR CABANG PATI",
    "Pati": "0405 - KANTOR CABANG PATI",
    "Rembang": "0405 - KANTOR CABANG PATI",
    # 0406 - KANTOR CABANG SEMARANG
    "Semarang": "0406 - KANTOR CABANG SEMARANG",
    # 0407 - KANTOR CABANG SUKOHARJO
    "Karanganyar": "0407 - KANTOR CABANG SUKOHARJO",
    "Sukoharjo": "0407 - KANTOR CABANG SUKOHARJO",
    "Wonogiri": "0407 - KANTOR CABANG SUKOHARJO",
}


def hitung_jumlah_merchant_per_kantor_detail(data_merchant):
    hasil = {kode: {"jumlah": 0, "data": []} for kode in WILAYAH_KE_KANTOR.values()}

    for merchant in data_merchant:
        wilayah = merchant.get("wilayah", "")
        kata_pertama = wilayah.split(",")[0].strip()
        kantor = WILAYAH_KE_KANTOR.get(kata_pertama, "LAINNYA / TIDAK DIKETAHUI")

        hasil.setdefault(kantor, {"jumlah": 0, "data": []})
        hasil[kantor]["jumlah"] += 1
        hasil[kantor]["data"].append(merchant)

    return hasil


def hitung_jumlah_merchant_diklaim(data_merchant):
    hasil = {kode: {"jumlah": 0, "data": []} for kode in WILAYAH_KE_KANTOR.values()}

    for merchant in data_merchant:
        wilayah = merchant.get("area", "")
        kata_pertama = wilayah.split(",")[0].strip()
        kantor = WILAYAH_KE_KANTOR.get(kata_pertama, "LAINNYA / TIDAK DIKETAHUI")

        hasil.setdefault(kantor, {"jumlah": 0, "data": []})
        hasil[kantor]["jumlah"] += 1
        hasil[kantor]["data"].append(merchant)

    return hasil


def hitung_jumlah_merchant_diklaim_selesai(data_merchant):
    hasil = {kode: {"jumlah": 0, "data": []} for kode in WILAYAH_KE_KANTOR.values()}

    for merchant in data_merchant:
        # Tambahkan kondisi untuk memeriksa status adalah "approve"
        if merchant.get("status") == "approve":
            wilayah = merchant.get("area", "")
            kata_pertama = wilayah.split(",")[0].strip()
            kantor = WILAYAH_KE_KANTOR.get(kata_pertama, "LAINNYA / TIDAK DIKETAHUI")

            hasil.setdefault(kantor, {"jumlah": 0, "data": []})
            hasil[kantor]["jumlah"] += 1
            hasil[kantor]["data"].append(merchant)

    return hasil


@app.context_processor
def utility_processor():
    return dict(format_rupiah=format_rupiah)


@app.route("/", methods=["GET", "POST"])
def index():
    indonesia_tz = pytz.timezone(
        "Asia/Jakarta"
    )  # WIB (GMT+7), bisa diganti 'Asia/Makassar' untuk WITA, 'Asia/Jayapura' untuk WIT
    current_year = datetime.datetime.now(indonesia_tz).year
    previous_year = current_year - 1

    today = datetime.datetime.now(indonesia_tz)
    today_form = datetime.datetime.now(indonesia_tz).strftime(
        "%Y-%m-%d"
    )  # Format: YYYY-MM-DD
    now = datetime.datetime.now(indonesia_tz).date()
    yesterday = now - datetime.timedelta(days=1)

    # Default values

    start_date_2024 = f"{today.year}-01-01"
    end_date_2024 = today_form

    data_2024 = None

    data_2024_sigap_instansi = None

    data_2024_merchant = None
    data_2024_merchant_merchant = None
    data_per_kantor = None
    data_per_kantor_diklaim = None
    data_per_kantor_diklaim_selesai = None
    url_2024_merchant_merchant = f"https://merchant.jasaraharja.co.id/merchant/datatables?draw=1&columns%5B0%5D%5Bdata%5D=name&columns%5B0%5D%5Bname%5D=name&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=category_name&columns%5B1%5D%5Bname%5D=category_name&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=phone&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=wilayah&columns%5B3%5D%5Bname%5D=wilayah&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=picture&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=status&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=asc&start=0&length=1000&search%5Bvalue%5D=&search%5Bregex%5D=false&category_id=all&province_id=all&_=174263731193"
    data_2024_merchant_merchant = ambil_data_merchant_merchant(
        url_2024_merchant_merchant
    )
    data_per_kantor = hitung_jumlah_merchant_per_kantor_detail(
        data_2024_merchant_merchant
    )

    url_2024_merchant = f"https://merchant.jasaraharja.co.id/home/datatables?"

    data_2024_merchant = ambil_data_merchant(url_2024_merchant)

    data_per_kantor_diklaim = hitung_jumlah_merchant_diklaim(data_2024_merchant)
    data_per_kantor_diklaim_selesai = hitung_jumlah_merchant_diklaim_selesai(
        data_2024_merchant
    )

    if request.method == "POST":

        start_date_2024 = request.form.get("start_date_2024", start_date_2024)
        end_date_2024 = request.form.get("end_date_2024", end_date_2024)

        url_2024 = f"https://ceri.jasaraharja.co.id/monitoring/operasi_gabungan/datatables/{start_date_2024}_{end_date_2024}_0400001_1"

        url_2024_sigap_instansi = f"https://ceri.jasaraharja.co.id/monitoring/crm_sigap/datatables/{start_date_2024}_{end_date_2024}_0400001_1"

        data_2024 = ambil_data(url_2024)

        data_2024_sigap_instansi = ambil_data_sigap_instansi(url_2024_sigap_instansi)

    return render_template(
        "index.html",
        previous_year=previous_year,
        current_year=current_year,
        start_date_2024=start_date_2024,
        end_date_2024=end_date_2024,
        today=today,
        today_form=today_form,
        data_2024_sigap_instansi=data_2024_sigap_instansi or [],
        data_2024=data_2024 or [],
        data_kantor=data_per_kantor,
        data_per_kantor_diklaim=data_per_kantor_diklaim,
        data_per_kantor_diklaim_selesai=data_per_kantor_diklaim_selesai,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5550)
