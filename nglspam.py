import requests
import uuid
import time

def nglspam(username, text, amount):
    headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'referer': f'https://ngl.link/{username}',
        'sec-ch-ua': '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    
    cookies = { AJA SENDIRI }
    
    session = requests.Session()
    session.headers.update(headers)
    session.cookies.update(cookies)
    
    success = 0
    failed = 0
    
    for i in range(amount):
        try:
            device_id = str(uuid.uuid4())
            
            form_data = {
                'username': username,
                'question': text,
                'deviceId': device_id,
                'gameSlug': '',
                'referrer': ''
            }
            
            response = session.post('https://ngl.link/api/submit', data=form_data, timeout=10)
            
            if response.status_code == 200:
                success += 1
                print(f"[{i+1}] Berhasil: {text}")
            else:
                failed += 1
                print(f"[{i+1}] Gagal: {response.status_code}")
            
            time.sleep(0.5)
            
        except Exception as e:
            failed += 1
            print(f"[{i+1}] Error: {e}")
    
    print(f"\nSelesai! Berhasil: {success}, Gagal: {failed}")
    return {'success': success, 'failed': failed}

username = input('Masukan usernamenya:\n')
teks = input('Masukan teksnya:\n')
jumlah = int(input('Masukan jumlah spam:\n'))

nglspam(username , teks, jumlah)
