import requests
import json
import time
import uuid

def aqaspam(username, text, amount):
    
    get_user_url = "https://aqa.link/portal/user/getInfoByUserName"
    
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en,en-US;q=0.9,en-GB-oxendict;q=0.8,id;q=0.7",
        "content-type": "application/json",
        "origin": "https://aqa.link",
        "referer": f"https://aqa.link/{username}",
        "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }
    
    payload = {"userName": username}
    
    try:
        response = requests.post(get_user_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            user_data = response.json()
            
            if user_data.get('code') == 200 and user_data.get('data'):
                userid = user_data['data']['id']
            else:
                return {"success": False, "sent": 0, "failed": 0, "errors": ["User tidak ditemukan"]}
        else:
            return {"success": False, "sent": 0, "failed": 0, "errors": [f"HTTP {response.status_code}"]}
            
    except Exception as e:
        return {"success": False, "sent": 0, "failed": 0, "errors": [str(e)]}
    
    send_url = "https://aqa.link/portal/message/send"
    
    headers_spam = {
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
    
    device_id = str(uuid.uuid4())
    
    results = {
        "success": True,
        "sent": 0,
        "failed": 0,
        "errors": [],
        "username": str(username),
        "user_id": str(userid)
    }
    
    print(f"\n{'='*60}")
    print(f"🚀 MEMULAI SPAM KE USERNAME: {username} (ID: {userid})")
    print(f"{'='*60}")
    print(f"📌 Username     : {username}")
    print(f"🆔 User ID      : {userid}")
    print(f"📝 Pesan        : {text[:50]}{'...' if len(text) > 50 else ''}")
    print(f"🔢 Jumlah       : {amount} kali")
    print(f"🆔 Device ID    : {device_id}")
    print(f"{'='*60}\n")
    
    for i in range(amount):
        payload_spam = {
            "toUserId": int(userid),
            "content": text,
            "deviceId": device_id,
            "topic": 1
        }
        
        try:
            start_time = time.time()
            response = requests.post(
                send_url,
                headers=headers_spam,
                json=payload_spam,
                timeout=30
            )
            elapsed_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                try:
                    resp_data = response.json()
                    results["sent"] += 1
                    print(f"[{i+1}/{amount}] ✅ BERHASIL | {elapsed_ms:.0f}ms")
                    if resp_data.get('code') and resp_data.get('code') != 0:
                        print(f"     ⚠️  Server note: {resp_data.get('message', 'No message')}")
                except:
                    results["sent"] += 1
                    print(f"[{i+1}/{amount}] ✅ BERHASIL | {elapsed_ms:.0f}ms")
                    
            elif response.status_code == 429:
                print(f"[{i+1}/{amount}] ⏰ RATE LIMITED | Delay 3 detik...")
                time.sleep(3)
                results["failed"] += 1
                results["errors"].append("Rate limited")
                
            elif response.status_code == 401:
                print(f"[{i+1}/{amount}] 🔒 SESSION EXPIRED | Perlu login!")
                results["failed"] += 1
                results["success"] = False
                results["errors"].append("Session expired - perlu cookies/auth")
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
    🎯 Target Username : {username}
    🆔 Target User ID  : {userid}
    ✅ Berhasil        : {results['sent']}/{amount}
    📈 Success Rate    : {success_rate:.1f}%
    {'='*60}
    """)
    
    return results


print("""
╔═════════════════════════════════════════════════╗
║                   AQA SPAM TOOL                 ║
╚═════════════════════════════════════════════════╝
""")
    
username = input("Masukan username:\n")
teks = input('Masukan teksnya:\n')
jumlah = int(input('Masukan jumlah spam:\n'))
    
aqaspam(username, teks, jumlah)
