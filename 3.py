import json
import os
import subprocess

# === CONFIG GITHUB & FILE ===
USER = "nurdianzz97-blip"
REPO = "Gdhj"
BRANCH = "main"
DB_FILE = "database_drama.json"
OUTPUT_FILE = "Dramabox_Elite.m3u"

# Gunakan 'origin' sebagai pengganti link panjang + token
REMOTE_URL = "origin"

def generate_m3u():
    print("🎬 Tahap 1: Membuat file M3U...")
    if not os.path.exists(DB_FILE):
        print("❌ Database drama gak ketemu!")
        return False

    try:
        with open(DB_FILE, 'r') as f:
            db = json.load(f)
    except Exception as e:
        print(f"❌ Error baca JSON: {e}")
        return False

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n\n")
        
        count = 0
        for d_id, info in db.items():
            title = info.get('title', 'Unknown Drama')
            logo_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/{d_id}.jpg"
            group_name = f"DRAMABOX - {title}"
            
            # Pastikan kunci 'episodes' ada dan tipenya list
            episodes = info.get('episodes', [])
            if isinstance(episodes, list):
                for ep in episodes:
                    ep_num = ep.get('episode', '?')
                    url = ep.get('url', '')
                    
                    if url:
                        f.write(f'#EXTINF:-1 tvg-logo="{logo_url}" group-title="{group_name}", DRAMABOX: {title} - Eps {ep_num}\n')
                        f.write(f'#EXTVLCOPT:http-referrer=https://www.dramaboxdb.com/\n')
                        f.write(f"{url}\n\n")
                        count += 1
    
    print(f"✅ File {OUTPUT_FILE} berhasil dibuat dengan {count} episode.")
    return True

def push_to_github():
    print("🚀 Tahap 2: Sinkronisasi ke GitHub...")
    try:
        # 1. Tandai semua perubahan
        subprocess.run(["git", "add", "."], check=True)
        
        # 2. Commit jika ada perubahan
        check_diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if check_diff.returncode != 0:
            subprocess.run(["git", "commit", "-m", "Update Playlist & Logo"], check=True)
        else:
            print("ℹ️ Tidak ada perubahan data.")

        # 3. Pull agar tidak bentrok (pakai rebase agar rapi)
        print("📥 Menarik data terbaru...")
        subprocess.run(["git", "pull", REMOTE_URL, BRANCH, "--rebase"], check=True)

        # 4. Push ke GitHub
        print("📤 Mengirim update...")
        subprocess.run(["git", "push", REMOTE_URL, f"main:{BRANCH}"], check=True)
        
        print("🎉 MANTAP! Playlist sudah live di GitHub.")
        print(f"🔗 Link Raw: https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/{OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Terjadi kesalahan Git: {e}")

if __name__ == "__main__":
    if generate_m3u():
        push_to_github()
