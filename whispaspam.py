import requests
import json
import time
import random

def whispaspam(username, text, amount):
    if len(text.strip()) < 8:
        print(f"\n❌ ERROR: Pesan terlalu pendek! Minimal 8 karakter. (Anda memasukkan {len(text.strip())} karakter)")
        return {'success': 0, 'failed': 1}
    
    headers_profile = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'origin': 'https://whispa.sh',
        'referer': 'https://whispa.sh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    }
    
    print("\n[+] Mengambil informasi profil...")
    
    profile_url = f"https://apiv4.whispa.sh/users/public-profile/{username}"
    
    try:
        profile_response = requests.get(profile_url, headers=headers_profile)
        profile_data = profile_response.json()
        receiver_id = profile_data.get('id')
        
        if not receiver_id:
            print(f"❌ ERROR: Username '{username}' tidak ditemukan!")
            return {'success': 0, 'failed': 1}
        
        print(f"✅ Berhasil mendapatkan ID user: {receiver_id}")
        print(f"👤 Target: @{profile_data.get('name', username)}")
        print(f"📝 Pesan: {text}")
        print(f"🔁 Jumlah spam: {amount}")
        print("\n" + "="*50)
        print("MEMULAI PENGIRIMAN PESAN...")
        print("="*50 + "\n")
            
    except Exception as e:
        print(f"❌ ERROR: Gagal mendapatkan profil: {str(e)}")
        return {'success': 0, 'failed': 1}
    
    headers_feedback = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://whispa.sh',
        'referer': 'https://whispa.sh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36'
    }
    
    feedback_url = "https://apiv4.whispa.sh/feedbacks"
    
    success = 0
    failed = 0
    
    for i in range(amount):
        try:
            payload = {
                "content": text,
                "receiverId": receiver_id,
                "authorId": None,
                "analytics": {
                    "audio": {
                        "sampleHash": random.uniform(1000, 2000),
                        "oscillator": "sine",
                        "maxChannels": 1,
                        "channelCountMode": "max"
                    },
                    "canvas": {
                        "commonImageDataHash": "361cb9fc38adb6a64137dd245501c6c2"
                    },
                    "fonts": {
                        "Arial Black": 531.9140625,
                        "Arial Narrow": 367.3828125,
                        "Calibri": 420.046875,
                        "Georgia": 475.2421875,
                        "Impact": 395.54296875,
                        "Roboto": 448.62890625,
                        "Segoe UI": 450,
                        "Tahoma": 432.45703125,
                        "Verdana": 486.5625
                    },
                    "hardware": {
                        "videocard": {
                            "vendor": "WebKit",
                            "renderer": "WebKit WebGL",
                            "version": "WebGL 1.0 (OpenGL ES 2.0 Chromium)",
                            "shadingLanguageVersion": "WebGL GLSL ES 1.0"
                        },
                        "architecture": 255,
                        "deviceMemory": "8",
                        "jsHeapSizeLimit": 2248146944
                    },
                    "locales": {
                        "languages": "id-ID",
                        "timezone": "Asia/Jakarta"
                    },
                    "system": {
                        "platform": "Win32",
                        "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "hardwareConcurrency": 4,
                        "cookieEnabled": True
                    }
                }
            }
            
            response = requests.post(feedback_url, headers=headers_feedback, json=payload, timeout=10)
            
            if response.status_code == 201:
                success += 1
                response_data = response.json()
                print(f"✅ [{i+1}/{amount}] PESAN BERHASIL TERKIRIM!")
                print(f"   📨 ID Pesan: {response_data.get('id', 'N/A')}")
                print(f"   ⏰ Waktu: {response_data.get('createdAt', 'N/A')}")
                print(f"   💬 Isi: {text[:50]}{'...' if len(text) > 50 else ''}")
                print("-" * 50)
            else:
                failed += 1
                print(f"❌ [{i+1}/{amount}] PESAN GAGAL TERKIRIM!")
                print(f"   📡 Status Code: {response.status_code}")
                if response.status_code == 429:
                    print(f"   ⚠️  Rate limit! Coba kurangi kecepatan.")
                print("-" * 50)
            
            time.sleep(random.uniform(1.0, 2.5))
            
        except requests.exceptions.Timeout:
            failed += 1
            print(f"❌ [{i+1}/{amount}] ERROR: Timeout - Koneksi terlalu lambat!")
            print("-" * 50)
        except Exception as e:
            failed += 1
            print(f"❌ [{i+1}/{amount}] ERROR: {str(e)[:100]}")
            print("-" * 50)
    
    print("\n" + "="*50)
    print("📊 RINGKASAN PENGIRIMAN")
    print("="*50)
    print(f"✅ BERHASIL: {success} pesan")
    print(f"❌ GAGAL: {failed} pesan")
    if (success+failed) > 0:
        print(f"📈 TINGKAT SUKSES: {success/(success+failed)*100:.1f}%")
    else:
        print("📈 TINGKAT SUKSES: 0%")
    print("="*50)
    
    return {'success': success, 'failed': failed}

print("""
╔══════════════════════════════════════════════════════════════╗
║                    WHISPA SPAM TOOL                          ║
╚══════════════════════════════════════════════════════════════╝
""")

print("📌 INFORMASI:")
print("   • Minimal pesan 8 karakter")
print("   • Rate limit: 100 pesan/menit")
print("   • Delay antar pesan: 1-2.5 detik")
print()

username = input("🔹 Masukkan username target (tanpa @): ")
teks = input("🔹 Masukkan teks pesan (minimal 8 karakter): ")
jumlah = int(input("🔹 Masukkan jumlah spam: "))

print(f"🎯 Target: @{username}")
print(f"💬 Pesan: {teks}")
print(f"🔁 Jumlah: {jumlah} kali")

whispaspam(username, teks, jumlah)
