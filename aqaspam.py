import requests
import json
import time
import uuid
import re

def aqaspam(userid, text, amount):
    
    send_url = "https://aqa.link/portal/message/send"
    
    cookies = ( AJA SENDIRI }
    
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,en-US;q=0.9,en-GB-oxendict;q=0.8,id;q=0.7",
        "content-type": "application/json",
        "origin": "https://aqa.link",
        "referer": "https://aqa.link/",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    print(f"[*] Target User ID: {userid}")
    
    if not str(userid).isdigit():
        print("✗ User ID harus berupa angka!")
        return {"success": False, "sent": 0, "failed": 0, "errors": ["Invalid User ID - harus angka"]}
    
    device_id = str(uuid.uuid4())
    
    results = {
        "success": True,
        "sent": 0,
        "failed": 0,
        "errors": [],
        "user_id": str(userid)
    }
    
    print(f"\n{'='*60}")
    print(f"🚀 MEMULAI SPAM KE USER ID: {userid}")
    print(f"{'='*60}")
    print(f"📌 User ID      : {userid}")
    print(f"📝 Pesan        : {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"🔢 Jumlah       : {amount} kali")
    print(f"🆔 Device ID    : {device_id}")
    print(f"{'='*60}\n")
    
    for i in range(amount):
        payload = {
            "toUserId": int(userid),
            "content": text,
            "deviceId": device_id,
            "topic": 1
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                send_url,
                headers=headers,
                cookies=cookies,
                json=payload,
                timeout=30
            )
            elapsed_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                try:
                    resp_data = response.json()
                    if resp_data.get("code") == 0 or resp_data.get("success") == True:
                        results["sent"] += 1
                        print(f"[{i+1}/{amount}] ✅ BERHASIL | {elapsed_ms:.0f}ms")
                    else:
                        results["failed"] += 1
                        error_msg = resp_data.get('message', 'Unknown')
                        print(f"[{i+1}/{amount}] ❌ GAGAL | {error_msg}")
                        results["errors"].append(error_msg)
                except:
                    results["sent"] += 1
                    print(f"[{i+1}/{amount}] ✅ BERHASIL | {elapsed_ms:.0f}ms")
                    
            elif response.status_code == 429:
                print(f"[{i+1}/{amount}] ⏰ RATE LIMITED | Delay 3 detik...")
                time.sleep(3)
                results["failed"] += 1
                results["errors"].append("Rate limited")
                
            elif response.status_code == 401:
                print(f"[{i+1}/{amount}] 🔒 SESSION EXPIRED | Cookies tidak valid!")
                results["failed"] += 1
                results["success"] = False
                results["errors"].append("Session expired")
                break
                
            else:
                results["failed"] += 1
                print(f"[{i+1}/{amount}] ❌ GAGAL | Status {response.status_code}")
                results["errors"].append(f"HTTP {response.status_code}")
                
        except Exception as e:
            results["failed"] += 1
            print(f"[{i+1}/{amount}] ❌ ERROR | {str(e)[:50]}")
            results["errors"].append(str(e))
        
        if i < amount - 1:
            time.sleep(0.8)
    
    success_rate = (results['sent'] / amount * 100) if amount > 0 else 0
    
    print(f"""
    {'='*60}
    📊 RINGKASAN PENGIRIMAN
    {'='*60}
    🎯 Target User ID : {userid}
    ✅ Berhasil       : {results['sent']}/{amount}
    📈 Success Rate   : {success_rate:.1f}%
    {'='*60}
    """)
    
    return results

userid = input("""
╔══════════════════════════════════════════════════════════════╗
║                        AQA SPAM TOOL                         ║
╚══════════════════════════════════════════════════════════════╝

📖 CARA MENDAPATKAN USER ID:
    
1. Buka https://aqa.link/[username_target] di browser
2. Tekan F12 (Developer Tools)
3. Klik tab "Network"
4. Kirim 1 pesan ke target
5. Cari request "send" di Network tab
6. Klik request tersebut
7. Lihat tab "Payload"
8. Cari field "toUserId" - copy angkanya

Masukan User ID (angka):\n""")
teks = input('Masukan teksnya:\n')
jumlah = int(input('Masukan jumlah spam:\n'))

aqaspam(userid, teks, jumlah)
