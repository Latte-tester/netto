import requests
import os
import re
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def merger_playlist():
    print("Eseguendo il merger_playlist.py...")
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    url1 = "channels_italy.m3u8"
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"
    url5 = "eventisps.m3u8" 
    
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist5 = download_playlist(url5)
    
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist5 

    lista = f'#EXTM3U\n' + lista
    
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
    
def merger_playlistworld():
    print("Eseguendo il merger_playlist.py...")
    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    url1 = "channels_italy.m3u8"  
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u" 
    url4 = "world.m3u8"           
    url5 = "eventisps.m3u8"      
    
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist4 = download_playlist(url4, exclude_group_title="Italy")
    playlist5 = download_playlist(url5)
    
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist4 + "\n" + playlist5

    lista = f'#EXTM3U\n' + lista
    
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
    
def eventi_m3u8_generator_world():
    print("Eseguendo l'eventi_m3u8_generator.py...")
    import json 
    import re 
    import requests 
    from urllib.parse import quote 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()  # Proxy HLS 
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(text_input):
        """
        Pulisce il testo per tvg-id: minuscolo, senza spazi, senza caratteri speciali (solo a-z0-9).
        """
        import re
        cleaned = str(text_input).lower()
        cleaned = re.sub(r'\s+', '', cleaned)
        cleaned = re.sub(r'[^a-z0-9]', '', cleaned)
        return cleaned
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                if logo1_url and logo2_url:
                    try:
                        from os.path import exists, getmtime
                        
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    return output_filename
                        
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status()
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None 
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil:
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status()
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil:
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.")
                        
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        combined.paste(img1, (0, 0), img1)
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        vs_x = (combined_width - 100) // 2
                        
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        combined = combined_with_vs
                        
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        return logo1_url or logo2_url
                
                return logo1_url or logo2_url
            if ':' in event_name:
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        return matches[0]
                
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        return matches[0]
                
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        return None
     
    def get_iframe_url(url): 
        try: 
            resp = session.post(url, timeout=HTTP_TIMEOUT) 
            resp.raise_for_status() 
            match = re.search(r'iframe src="([^"]+)"', resp.text) 
            return match.group(1) if match else None 
        except requests.RequestException as e: 
            print(f"[!] Errore richiesta iframe URL {url}: {e}") 
            return None 
     
    def get_final_m3u8(iframe_url): 
        try: 
            parsed = re.search(r"https?://([^/]+)", iframe_url) 
            if not parsed: 
                print(f"[!] URL iframe non valido: {iframe_url}") 
                return None 
            referer_base = f"https://{parsed.group(1)}" 
     
            page_resp = session.post(iframe_url, timeout=HTTP_TIMEOUT) 
            page_resp.raise_for_status() 
            page = page_resp.text 
     
            key = re.search(r'var channelKey = "(.*?)"', page) 
            ts  = re.search(r'var authTs     = "(.*?)"', page) 
            rnd = re.search(r'var authRnd    = "(.*?)"', page) 
            sig = re.search(r'var authSig    = "(.*?)"', page) 
     
            if not all([key, ts, rnd, sig]): 
                print(f"[!] Mancano variabili auth in pagina {iframe_url}") 
                return None 
     
            channel_key = key.group(1) 
            auth_ts     = ts.group(1) 
            auth_rnd    = rnd.group(1) 
            auth_sig    = quote(sig.group(1), safe='') 
     
            auth_url = f"https://top2new.newkso.ru/auth.php?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}" 
            session.get(auth_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT) 
     
            lookup_url = f"{referer_base}/server_lookup.php?channel_id={quote(channel_key)}" 
            lookup = session.get(lookup_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT) 
            lookup.raise_for_status() 
            data = lookup.json() 
     
            server_key = data.get("server_key") 
            if not server_key: 
                print(f"[!] server_key non trovato per channel {channel_key}") 
                return None 
     
            if server_key == "top1/cdn": 
                return f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8" 
     
            stream_url = (f"{PROXY}https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8") 
            return stream_url 
     
        except requests.RequestException as e: 
            print(f"[!] Errore richiesta get_final_m3u8: {e}") 
            return None 
        except json.JSONDecodeError: 
            print(f"[!] Errore parsing JSON da server_lookup per {iframe_url}") 
            return None 
     
    def get_stream_from_channel_id(channel_id): 
        embed_url = f"{LINK_DADDY}/embed/stream-{channel_id}.php" 
        iframe = get_iframe_url(embed_url) 
        if iframe: 
            return get_final_m3u8(iframe) 
        return None 
     
    def clean_category_name(name): 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it", "uk", "tnt", "usa", "tennis channel", "tennis stream", "la"} 
        now = datetime.now() 
        yesterday_date = (now - timedelta(days=1)).date()
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
     
            if date_obj != now.date(): 
                continue 
     
            date_str = date_obj.strftime("%Y-%m-%d") 
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") 
                    try: 
                        time_obj = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2) 
     
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 
     
                        if now - event_datetime > timedelta(hours=2): 
                            continue 
     
                        time_formatted = time_obj.strftime("%H:%M") 
                    except Exception: 
                        time_formatted = time_str 
     
                    event_title = item.get("event", "Evento") 
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 
     
                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})" 
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title
                            }) 
     
        return categorized_channels 

def eventi_m3u8_generator():
    print("Eseguendo l'eventi_m3u8_generator.py...")
    import json 
    import re 
    import requests 
    from urllib.parse import quote 
    from datetime import datetime, timedelta 
    from dateutil import parser 
    import urllib.parse
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io
    import time

    load_dotenv()
    
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()  # Proxy HLS 
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(text_input):
        """
        Pulisce il testo per tvg-id: minuscolo, senza spazi, senza caratteri speciali (solo a-z0-9).
        """
        import re
        cleaned = str(text_input).lower()
        cleaned = re.sub(r'\s+', '', cleaned)
        cleaned = re.sub(r'[^a-z0-9]', '', cleaned)
        return cleaned
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                if logo1_url and logo2_url:
                    try:
                        from os.path import exists, getmtime
                        
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    return output_filename
                        
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status()
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None 
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil:
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status()
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None 
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: 
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerà l'except sottostante
                        
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        combined.paste(img1, (0, 0), img1)
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        vs_x = (combined_width - 100) // 2
                        
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        combined = combined_with_vs
                        
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        return logo1_url or logo2_url
                
                return logo1_url or logo2_url
            if ':' in event_name:
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
                
                headers = { 
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive"
                } 
                
                response = requests.get(search_url, headers=headers, timeout=10)
                
                if response.status_code == 200: 
                    patterns = [
                        r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                        r'"murl":"(https?://[^"]+)"',
                        r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                        r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                        r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches and len(matches) > 0:
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        return matches[0]
                
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            search_url = f"https://www.bing.com/images/search?q={search_query}&qft=+filterui:photo-transparent+filterui:aspect-square&form=IRFLTR"
            
            headers = { 
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive"
            } 
            
            response = requests.get(search_url, headers=headers, timeout=10)
            
            if response.status_code == 200: 
                patterns = [
                    r'murl&quot;:&quot;(https?://[^&]+)&quot;',
                    r'"murl":"(https?://[^"]+)"',
                    r'"contentUrl":"(https?://[^"]+\.(?:png|jpg|jpeg|svg))"',
                    r'<img[^>]+src="(https?://[^"]+\.(?:png|jpg|jpeg|svg))[^>]+class="mimg"',
                    r'<a[^>]+class="iusc"[^>]+m=\'{"[^"]*":"[^"]*","[^"]*":"(https?://[^"]+)"'
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches and len(matches) > 0:
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        return matches[0]
                
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        json_str = json_match.group(1)
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        return None
     
    def get_iframe_url(url): 
        try: 
            resp = session.post(url, timeout=HTTP_TIMEOUT) 
            resp.raise_for_status() 
            match = re.search(r'iframe src="([^"]+)"', resp.text) 
            return match.group(1) if match else None 
        except requests.RequestException as e: 
            print(f"[!] Errore richiesta iframe URL {url}: {e}") 
            return None 
     
    def get_final_m3u8(iframe_url): 
        try: 
            parsed = re.search(r"https?://([^/]+)", iframe_url) 
            if not parsed: 
                print(f"[!] URL iframe non valido: {iframe_url}") 
                return None 
            referer_base = f"https://{parsed.group(1)}" 
     
            page_resp = session.post(iframe_url, timeout=HTTP_TIMEOUT) 
            page_resp.raise_for_status() 
            page = page_resp.text 
     
            key = re.search(r'var channelKey = "(.*?)"', page) 
            ts  = re.search(r'var authTs     = "(.*?)"', page) 
            rnd = re.search(r'var authRnd    = "(.*?)"', page) 
            sig = re.search(r'var authSig    = "(.*?)"', page) 
     
            if not all([key, ts, rnd, sig]): 
                print(f"[!] Mancano variabili auth in pagina {iframe_url}") 
                return None 
     
            channel_key = key.group(1) 
            auth_ts     = ts.group(1) 
            auth_rnd    = rnd.group(1) 
            auth_sig    = quote(sig.group(1), safe='') 
     
            auth_url = f"https://top2new.newkso.ru/auth.php?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}" 
            session.get(auth_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT) 
     
            lookup_url = f"{referer_base}/server_lookup.php?channel_id={quote(channel_key)}" 
            lookup = session.get(lookup_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT) 
            lookup.raise_for_status() 
            data = lookup.json() 
     
            server_key = data.get("server_key") 
            if not server_key: 
                print(f"[!] server_key non trovato per channel {channel_key}") 
                return None 
     
            if server_key == "top1/cdn": 
                return f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8" 
     
            stream_url = (f"{PROXY}https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8") 
            return stream_url 
     
        except requests.RequestException as e: 
            print(f"[!] Errore richiesta get_final_m3u8: {e}") 
            return None 
        except json.JSONDecodeError: 
            print(f"[!] Errore parsing JSON da server_lookup per {iframe_url}") 
            return None 
     
    def get_stream_from_channel_id(channel_id): 
        embed_url = f"{LINK_DADDY}/embed/stream-{channel_id}.php" 
        iframe = get_iframe_url(embed_url) 
        if iframe: 
            return get_final_m3u8(iframe) 
        return None 
     
    def clean_category_name(name): 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it"} 
        now = datetime.now() 
        yesterday_date = (now - timedelta(days=1)).date() 
     
        with open(path, "r", encoding="utf-8") as f: 
            data = json.load(f) 
     
        categorized_channels = {} 
     
        for date_key, sections in data.items(): 
            date_part = date_key.split(" - ")[0] 
            try: 
                date_obj = parser.parse(date_part, fuzzy=True).date() 
            except Exception as e: 
                print(f"[!] Errore parsing data '{date_part}': {e}") 
                continue 
     
            is_today = (date_obj == now.date())
            is_yesterday_target_event = (date_obj == yesterday_date)

            if not (is_today or is_yesterday_target_event):
                continue 
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00")
                    event_title = item.get("event", "Evento") 
                    
                    try: 
                        event_time_from_json = datetime.strptime(time_str, "%H:%M").time()

                        if is_today:
                            time_obj_corrected = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2) # correzione timezone
                            event_datetime_corrected = datetime.combine(date_obj, time_obj_corrected.time())
                            
                            if now - event_datetime_corrected > timedelta(hours=2):
                                continue
                            time_formatted = time_obj_corrected.strftime("%H:%M")

                        elif is_yesterday_target_event:
                            start_filter_time = datetime.strptime("00:00", "%H:%M").time()
                            end_filter_time = datetime.strptime("04:00", "%H:%M").time()
                            
                            if not (start_filter_time <= event_time_from_json <= end_filter_time):
                                continue
                            
                            time_obj_corrected = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2)
                            time_formatted = time_obj_corrected.strftime("%H:%M")
                        
                        else: 
                            continue 

                    except ValueError:
                        print(f"[!] Orario evento non valido '{time_str}' per l'evento '{event_title}'. Evento saltato.")
                        continue
     
                    for ch in item.get("channels", []): 
                        channel_name = ch.get("channel_name", "") 
                        channel_id = ch.get("channel_id", "") 
     
                        words = set(re.findall(r'\b\w+\b', channel_name.lower())) 
                        if keywords.intersection(words): 
                            tvg_name = f"{event_title} ({time_formatted})"
                            categorized_channels[category].append({ 
                                "tvg_name": tvg_name, 
                                "channel_name": channel_name, 
                                "channel_id": channel_id,
                                "event_title": event_title
                            }) 
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 
     
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live",DADDYLIVE\n')
            f.write("https://example.com.m3u8\n\n")
     
            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
     
                f.write(f'#EXTINF:-1 tvg-name="{category}" group-title="Eventi Live",--- {category} ---\nhttps://exemple.m3u8\n\n') 
     
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    event_title = ch["event_title"]
                    
                    event_based_tvg_id = clean_tvg_id(event_title)
                    
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title) 
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        stream = get_stream_from_channel_id(ch["channel_id"])
                        if stream: 
                            f.write(f'#EXTINF:-1 tvg-id="{event_based_tvg_id}" tvg-name="{tvg_name}"{logo_attribute} group-title="Eventi Live",{tvg_name}\n{stream}\n\n') 
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    if __name__ == "__main__": 
        generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)
        
def eventi_sps():
    import requests
    import re
    import os
    from bs4 import BeautifulSoup
    from urllib.parse import quote_plus
    from datetime import datetime
    from dotenv import load_dotenv

    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()

    base_url = "https://www.sportstreaming.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Origin": "https://www.sportstreaming.net",
        "Referer": "https://www.sportstreaming.net/"
    }

    def format_event_date(date_text):
        """
        Formatta la data dell'evento e restituisce la stringa formattata completa e una stringa DD/MM per il confronto.
        Restituisce: (full_formatted_date, simple_date_dd_mm)
        Esempio: ("20:45 23/07", "23/07") o ("", "") se non parsabile.
        """
        if not date_text:
            return "", ""
        match = re.search(
            r'(?:[a-zA-Zì]+\s+)?(\d{1,2})\s+([a-zA-Z]+)\s+(?:ore\s+)?(\d{1,2}:\d{2})',
            date_text,
            re.IGNORECASE
        )
        if match:
            day_str = match.group(1).zfill(2)
            month_name = match.group(2).lower()
            time = match.group(3)
            month_number = ITALIAN_MONTHS_MAP.get(month_name)
            if month_number:
                return f"{time} {day_str}/{month_number}", f"{day_str}/{month_number}"
        return "", ""

    ITALIAN_MONTHS_MAP = {
        "gennaio": "01", "febbraio": "02", "marzo": "03", "aprile": "04",
        "maggio": "05", "giugno": "06", "luglio": "07", "agosto": "08",
        "settembre": "09", "ottobre": "10", "novembre": "11", "dicembre": "12"
    }

    def find_event_pages():
        try:
            response = requests.get(base_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            event_links = []
            seen_links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if re.match(r'/live-(perma-)?\d+', href):
                    full_url = base_url + href.lstrip('/')
                    if full_url not in seen_links:
                        event_links.append(full_url)
                        seen_links.add(full_url)
                elif re.match(r'https://www\.sportstreaming\.net/live-(perma-)?\d+', href):
                    if href not in seen_links:
                        event_links.append(href)
                        seen_links.add(href)

            return event_links

        except requests.RequestException as e:
            print(f"Errore durante la ricerca delle pagine evento: {e}")
            return []

    def get_event_details(event_url):
        try:
            response = requests.get(event_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            stream_url = None
            element = None
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src')
                if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts|html|php)', src, re.IGNORECASE)):
                    stream_url = src
                    element = iframe
                    break

            if not stream_url:
                for embed in soup.find_all('embed'):
                    src = embed.get('src')
                    if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts|html|php)', src, re.IGNORECASE)):
                        stream_url = src
                        element = embed
                        break

            if not stream_url:
                for video in soup.find_all('video'):
                    src = video.get('src')
                    if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts)', src, re.IGNORECASE)):
                        stream_url = src
                        element = video
                        break
                    for source in video.find_all('source'):
                        src = source.get('src')
                        if src and ("stream" in src.lower() or re.search(r'\.(m3u8|mp4|ts)', src, re.IGNORECASE)):
                            stream_url = src
                            element = source
                            break

            full_event_datetime_str = ""
            event_date_comparable = ""
            event_time_str = ""  
            date_span = soup.find('span', class_='uk-text-meta uk-text-small')
            if date_span:
                date_text = date_span.get_text(strip=True)
                full_event_datetime_str, event_date_comparable = format_event_date(date_text)
                if full_event_datetime_str:
                    time_match = re.match(r'(\d{1,2}:\d{2})', full_event_datetime_str)
                    if time_match:
                        event_time_str = time_match.group(1)
     
            event_title_from_html = "Unknown Event"
            title_tag = soup.find('title')
            if title_tag:
                event_title_from_html = title_tag.get_text(strip=True)
                event_title_from_html = re.sub(r'\s*\|\s*Sport Streaming\s*$', '', event_title_from_html, flags=re.IGNORECASE).strip()

            league_info = "Event" 
            is_perma_channel = "perma" in event_url.lower()

            if is_perma_channel:
                if event_title_from_html and event_title_from_html != "Unknown Event":
                    league_info = event_title_from_html
            else:
                league_spans = soup.find_all(
                    lambda tag: tag.name == 'span' and \
                                'uk-text-small' in tag.get('class', []) and \
                                'uk-text-meta' not in tag.get('class', []) 
                )
                if league_spans:
                    league_info = ' '.join(league_spans[0].get_text(strip=True).split())

            return stream_url, event_date_comparable, event_time_str, event_title_from_html, league_info

        except requests.RequestException as e:
            print(f"Errore durante l'accesso a {event_url}: {e}")
            return None, "", "", "Unknown Event", "Event"

    def update_m3u_file(video_streams, m3u_file="eventisps.m3u8"):
        REPO_PATH = os.getenv('GITHUB_WORKSPACE', '.')
        file_path = os.path.join(REPO_PATH, m3u_file)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            f.write(f'#EXTINF:-1 tvg-name="SPORTSTREAMING" group-title="Eventi Live",SPORTSTREAMING\n')
            f.write("https://example.com.m3u8\n\n")

            perma_count = 1

            for event_url, stream_url, event_time, event_title, league_info in video_streams:
                if not stream_url:
                    continue

                is_perma = "perma" in event_url.lower()
                if is_perma:
                    image_url = f"https://sportstreaming.net/assets/img/live/perma/live{perma_count}.png"
                    perma_count += 1
                else:
                    match = re.search(r'live-(\d+)', event_url)
                    if match:
                        live_number = match.group(1)
                        image_url = f"https://sportstreaming.net/assets/img/live/standard/live{live_number}.png"
                    else:
                        image_url = "https://sportstreaming.net/assets/img/live/standard/live1.png"

                tvg_name_prefix = f"{event_time} " if event_time else ""
                tvg_name_final = f"{event_title} | {league_info} | {tvg_name_prefix}".strip()
                if not tvg_name_final:
                    tvg_name_final = "Eventi Live"

                encoded_ua = quote_plus(headers["User-Agent"])
                encoded_referer = quote_plus(headers["Referer"])
                encoded_origin = quote_plus(headers["Origin"])

                final_stream_url = f"{PROXY}{stream_url}&h_user-agent={encoded_ua}&h_referer={encoded_referer}&h_origin={encoded_origin}"

                group_title_text = "Sport" if is_perma else "Eventi Live"

                f.write(f"#EXTINF:-1 tvg-name=\"{tvg_name_final} (SPS)\"group-title=\"{group_title_text}\" tvg-logo=\"{image_url}\",{tvg_name_final} (SPS)\n")
                f.write(f"{final_stream_url}\n")
                f.write("\n")


        print(f"File M3U8 aggiornato con successo: {file_path}")

    if __name__ == "__main__":
        current_date_dd_mm = datetime.now().strftime("%d/%m")
        print(f"Recupero eventi per il giorno: {current_date_dd_mm}")

        event_pages = find_event_pages()
        if not event_pages:
            print("Nessuna pagina evento trovata.")
        else:
            video_streams = []
            for event_url in event_pages:
                stream_url, event_date_str, event_time, event_title, league_info = get_event_details(event_url)
                
                if stream_url:
                    is_perma = "perma" in event_url.lower()
                    if not is_perma and (event_date_str == current_date_dd_mm):
                        print(f"Includo: {event_title} (URL: {event_url}, Data evento: {event_date_str})")
                        video_streams.append((event_url, stream_url, event_time, event_title, league_info))
                    elif is_perma:
                        print(f"Scarto canale perma: {event_title} (URL: {event_url})")
                else:
                    print(f"Nessun flusso trovato per {event_url}")

            if video_streams:
                update_m3u_file(video_streams)
            else:
                print("Nessun flusso video trovato in tutte le pagine evento.")
    
def schedule_extractor():
    print("Eseguendo lo schedule_extractor.py...")
    from playwright.sync_api import sync_playwright
    import os
    import json
    from datetime import datetime
    import re
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    
    load_dotenv()
    
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    
    def html_to_json(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}
        
        date_rows = soup.find_all('tr', class_='date-row')
        if not date_rows:
            print("AVVISO: Nessuna riga di data trovata nel contenuto HTML!")
            return {}
    
        current_date = None
        current_category = None
    
        for row in soup.find_all('tr'):
            if 'date-row' in row.get('class', []):
                current_date = row.find('strong').text.strip()
                result[current_date] = {}
                current_category = None
    
            elif 'category-row' in row.get('class', []) and current_date:
                current_category = row.find('strong').text.strip() + "</span>"
                result[current_date][current_category] = []
    
            elif 'event-row' in row.get('class', []) and current_date and current_category:
                time_div = row.find('div', class_='event-time')
                info_div = row.find('div', class_='event-info')
    
                if not time_div or not info_div:
                    continue
    
                time_strong = time_div.find('strong')
                event_time = time_strong.text.strip() if time_strong else ""
                event_info = info_div.text.strip()
    
                event_data = {
                    "time": event_time,
                    "event": event_info,
                    "channels": []
                }
    
                next_row = row.find_next_sibling('tr')
                if next_row and 'channel-row' in next_row.get('class', []):
                    channel_links = next_row.find_all('a', class_='channel-button-small')
                    for link in channel_links:
                        href = link.get('href', '')
                        channel_id_match = re.search(r'stream-(\d+)\.php', href)
                        if channel_id_match:
                            channel_id = channel_id_match.group(1)
                            channel_name = link.text.strip()
                            channel_name = re.sub(r'\s*\(CH-\d+\)$', '', channel_name)
    
                            event_data["channels"].append({
                                "channel_name": channel_name,
                                "channel_id": channel_id
                            })
    
                result[current_date][current_category].append(event_data)
    
        return result
    
    def modify_json_file(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        current_month = datetime.now().strftime("%B")
    
        for date in list(data.keys()):
            match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\d{4})", date)
            if match:
                day_part = match.group(1)
                suffix = match.group(2)
                year_part = match.group(3)
                new_date = f"{day_part}{suffix} {current_month} {year_part}"
                data[new_date] = data.pop(date)
    
        with open(json_file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        
        print(f"File JSON modificato e salvato in {json_file_path}")
    
    def extract_schedule_container():
        url = f"{LINK_DADDY}/"
    
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_output = os.path.join(script_dir, "daddyliveSchedule.json")
    
        print(f"Accesso alla pagina {url} per estrarre il main-schedule-container...")
    
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
    
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"Tentativo {attempt} di {max_attempts}...")
                    page.goto(url)
                    print("Attesa per il caricamento completo...")
                    page.wait_for_timeout(10000)  # 10 secondi
    
                    schedule_content = page.evaluate("""() => {
                        const container = document.getElementById('main-schedule-container');
                        return container ? container.outerHTML : '';
                    }""")
    
                    if not schedule_content:
                        print("AVVISO: main-schedule-container non trovato o vuoto!")
                        if attempt == max_attempts:
                            browser.close()
                            return False
                        else:
                            continue
    
                    print("Conversione HTML in formato JSON...")
                    json_data = html_to_json(schedule_content)
    
                    with open(json_output, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, indent=4)
    
                    print(f"Dati JSON salvati in {json_output}")
    
                    modify_json_file(json_output)
                    browser.close()
                    return True
    
                except Exception as e:
                    print(f"ERRORE nel tentativo {attempt}: {str(e)}")
                    if attempt == max_attempts:
                        print("Tutti i tentativi falliti!")
                        browser.close()
                        return False
                    else:
                        print(f"Riprovando... (tentativo {attempt + 1} di {max_attempts})")
    
            browser.close()
            return False
    
    if __name__ == "__main__":
        success = extract_schedule_container()
        if not success:
            exit(1)

def epg_eventi_generator_world():
    print("Eseguendo l'epg_eventi_generator_world.py...")
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        text = clean_text(text)
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        if not text:
            text = "unknownchannel"
        return text
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name_original = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_name = event_name_original.replace('&', 'and')
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    channel_id = clean_channel_id(event_name)
    
                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        announcement_stop_local = event_datetime_local
    
                        if channel_id in last_event_end_time_per_channel_on_date:
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
    
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.'
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: 
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2)
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False

def epg_eventi_generator():
    print("Eseguendo l'epg_eventi_generator.py...")
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        text = clean_text(text)
        text = re.sub(r'\s+', '', text)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        if not text:
            text = "unknownchannel"
        return text
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            last_event_end_time_per_channel_on_date = {}
    
            try:
                date_str_from_key = date_key.split(' - ')[0]
                date_str_cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str_from_key)
                event_date_part = datetime.strptime(date_str_cleaned, "%A %d %B %Y").date()
            except ValueError as e:
                print(f"[!] Errore nel parsing della data EPG: '{date_str_from_key}'. Errore: {e}")
                continue
            except IndexError as e:
                print(f"[!] Formato data non valido: '{date_key}'. Errore: {e}")
                continue
    
            if event_date_part < current_datetime_local.date():
                continue
    
            for category_name, events_list in categories.items():
                try:
                    sorted_events_list = sorted(
                        events_list,
                        key=lambda x: datetime.strptime(x.get("time", "00:00"), "%H:%M").time()
                    )
                except Exception as e_sort:
                    print(f"[!] Attenzione: Impossibile ordinare gli eventi per la categoria '{category_name}' nella data '{date_key}'. Si procede senza ordinamento. Errore: {e_sort}")
                    sorted_events_list = events_list
    
                for event_info in sorted_events_list:
                    time_str_utc = event_info.get("time", "00:00")
                    event_name = clean_text(event_info.get("event", "Evento Sconosciuto"))
                    event_desc = event_info.get("description", f"Trasmesso in diretta.")
    
                    channel_id = clean_channel_id(event_name)
    
                    try:
                        event_time_utc_obj = datetime.strptime(time_str_utc, "%H:%M").time()
                        event_datetime_utc = datetime.combine(event_date_part, event_time_utc_obj)
                        event_datetime_local = event_datetime_utc + italian_offset
                    except ValueError as e:
                        print(f"[!] Errore parsing orario UTC '{time_str_utc}' per EPG evento '{event_name}'. Errore: {e}")
                        continue
                    
                    if event_datetime_local < (current_datetime_local - timedelta(hours=2)):
                        continue
    
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        announcement_stop_local = event_datetime_local 
    
                        if channel_id in last_event_end_time_per_channel_on_date:
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
    
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.'
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else:
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2)
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        last_event_end_time_per_channel_on_date[channel_id] = main_event_stop_local
        
        epg_content += "</tv>\n"
        return epg_content
    
    def save_epg_xml(epg_content, output_file_path):
        """Salva il contenuto EPG XML su file"""
        try:
            with open(output_file_path, "w", encoding="utf-8") as file:
                file.write(epg_content)
            print(f"[✓] File EPG XML salvato con successo: {output_file_path}")
            return True
        except Exception as e:
            print(f"[!] Errore nel salvataggio del file EPG XML: {e}")
            return False
        
def italy_channels():
    print("Eseguendo il italy_channels.py...")

    import requests
    import re
    import os
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv
    import urllib.parse 
    import json 
    from bs4 import BeautifulSoup

    load_dotenv()

    LINK_SS = os.getenv("LINK_SKYSTREAMING", "https://skystreaming.yoga").strip()
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()
    EPG_FILE = "epg.xml"
    LOGOS_FILE = "logos.txt"
    OUTPUT_FILE = "channels_italy.m3u8"
    DEFAULT_TVG_ICON = ""
    HTTP_TIMEOUT = 20 

    session = requests.Session()

    BASE_URLS = [
        "https://vavoo.to"
    ]

    CATEGORY_KEYWORDS = {
        "Rai": ["rai"],
        "Mediaset": ["twenty seven", "twentyseven", "mediaset", "italia 1", "italia 2", "canale 5"],
        "Sport": ["inter", "milan", "lazio", "calcio", "tennis", "sport", "super tennis", "supertennis", "dazn", "eurosport", "sky sport", "rai sport"],
        "Film & Serie TV": ["crime", "primafila", "cinema", "movie", "film", "serie", "hbo", "fox", "rakuten", "atlantic"],
        "News": ["news", "tg", "rai news", "sky tg", "tgcom"],
        "Bambini": ["frisbee", "super!", "fresbee", "k2", "cartoon", "boing", "nick", "disney", "baby", "rai yoyo"],
        "Documentari": ["documentaries", "discovery", "geo", "history", "nat geo", "nature", "arte", "documentary"],
        "Musica": ["deejay", "rds", "hits", "rtl", "mtv", "vh1", "radio", "music", "kiss", "kisskiss", "m2o", "fm"],
        "Altro": ["focus", "real time"]
    }

    def fetch_epg(epg_file):
        try:
            tree = ET.parse(epg_file)
            return tree.getroot()
        except Exception as e:
            print(f"Errore durante la lettura del file EPG: {e}")
            return None

    def fetch_logos(logos_file):
        logos_dict = {}
        try:
            with open(logos_file, "r", encoding="utf-8") as f:
                for line in f:
                    match = re.match(r'\s*"(.+?)":\s*"(.+?)",?', line)
                    if match:
                        channel_name, logo_url = match.groups()
                        logos_dict[channel_name.lower()] = logo_url
        except Exception as e:
            print(f"Errore durante la lettura del file dei loghi: {e}")
        return logos_dict

    def normalize_channel_name(name):
        name = re.sub(r"\s+", "", name.strip().lower())
        name = re.sub(r"\.it\b", "", name)
        name = re.sub(r"hd|fullhd", "", name)
        return name

    def create_channel_id_map(epg_root):
        channel_id_map = {}
        for channel in epg_root.findall('channel'):
            tvg_id = channel.get('id')
            display_name = channel.find('display-name').text
            if tvg_id and display_name:
                normalized_name = normalize_channel_name(display_name)
                channel_id_map[normalized_name] = tvg_id
        return channel_id_map

    def fetch_channels(base_url):
        try:
            response = session.get(f"{base_url}/channels", timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []

    def clean_channel_name(name):
        name = re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name)
        name = re.sub(r"\s*\(.*?\)", "", name)
        if "zona dazn" in name.lower() or "dazn 1" in name.lower():
            return "DAZN2"
        if "mediaset 20" in name.lower():
            return "20 MEDIASET"
        if "mediaset italia 2" in name.lower():
            return "ITALIA 2"
        if "mediaset 1" in name.lower():
            return "ITALIA 1"
        return name.strip()

    def filter_italian_channels(channels, base_url):
        seen = {}
        results = []
        for ch in channels:
            if ch.get("country") == "Italy":
                clean_name = clean_channel_name(ch["name"])
                if clean_name.lower() in ["dazn", "dazn 2"]:
                    continue
                count = seen.get(clean_name, 0) + 1
                seen[clean_name] = count
                if count > 1:
                    clean_name = f"{clean_name} ({count})"
                results.append((clean_name, f"{base_url}/play/{ch['id']}/index.m3u8"))
        return results

    def classify_channel(name):
        for category, words in CATEGORY_KEYWORDS.items():
            if any(word in name.lower() for word in words):
                return category
        return "Altro"

    def get_manual_channels():
        return [
            {"name": "SKY SPORT 251 (SS)", "url": f"https://hls.kangal.icu/hls/sky251/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..251.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 252 (SS)", "url": f"https://hls.kangal.icu/hls/sky252/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..252.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 253 (SS)", "url": f"https://hls.kangal.icu/hls/sky253/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..253.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 254 (SS)", "url": f"https://hls.kangal.icu/hls/sky254/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..254.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 255 (SS)", "url": f"https://hls.kangal.icu/hls/sky255/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..255.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 256 (SS)", "url": f"https://hls.kangal.icu/hls/sky256/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..256.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 257 (SS)", "url": f"https://hls.kangal.icu/hls/sky257/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..257.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 258 (SS)", "url": f"https://hls.kangal.icu/hls/sky258/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..258.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 259 (SS)", "url": f"https://hls.kangal.icu/hls/sky259/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..259.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 260 (SS)", "url": f"https://hls.kangal.icu/hls/sky260/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..260.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
            {"name": "SKY SPORT 261 (SS)", "url": f"https://hls.kangal.icu/hls/sky261/index.m3u8&h_user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36&h_referer={LINK_SS}/&h_origin={LINK_SS}", "tvg_id": "sky.sport..261.it", "logo": "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png", "category": "Sport"},
        ]

    def get_iframe_url(url):
        try:
            resp = session.post(url, timeout=HTTP_TIMEOUT)
            resp.raise_for_status()
            match = re.search(r'iframe src="([^"]+)"', resp.text)
            return match.group(1) if match else None
        except requests.RequestException as e:
            print(f"[!] Errore richiesta iframe URL {url}: {e}")
            return None

    def get_final_m3u8(iframe_url):
        try:
            parsed_iframe_url = urllib.parse.urlparse(iframe_url)
            if not parsed_iframe_url.scheme or not parsed_iframe_url.netloc:
                print(f"[!] URL iframe non valido: {iframe_url}")
                return None
            referer_base = f"{parsed_iframe_url.scheme}://{parsed_iframe_url.netloc}"

            page_resp = session.post(iframe_url, timeout=HTTP_TIMEOUT)
            page_resp.raise_for_status()
            page = page_resp.text

            key_match = re.search(r'var channelKey = "(.*?)"', page)
            ts_match  = re.search(r'var authTs     = "(.*?)"', page)
            rnd_match = re.search(r'var authRnd    = "(.*?)"', page)
            sig_match = re.search(r'var authSig    = "(.*?)"', page)

            if not all([key_match, ts_match, rnd_match, sig_match]):
                print(f"[!] Mancano variabili auth in pagina {iframe_url}")
                return None

            channel_key = key_match.group(1)
            auth_ts     = ts_match.group(1)
            auth_rnd    = rnd_match.group(1)
            auth_sig    = urllib.parse.quote(sig_match.group(1), safe='')

            auth_url = f"https://top2new.newkso.ru/auth.php?channel_id={channel_key}&ts={auth_ts}&rnd={auth_rnd}&sig={auth_sig}"
            session.get(auth_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT)

            lookup_url = f"{referer_base}/server_lookup.php?channel_id={urllib.parse.quote(channel_key)}"
            lookup_resp = session.get(lookup_url, headers={"Referer": referer_base}, timeout=HTTP_TIMEOUT)
            lookup_resp.raise_for_status()
            data = lookup_resp.json()

            server_key = data.get("server_key")
            if not server_key:
                print(f"[!] server_key non trovato per channel {channel_key} da {iframe_url}")
                return None

            if server_key == "top1/cdn":
                raw_m3u8_url = f"https://top1.newkso.ru/top1/cdn/{channel_key}/mono.m3u8"
            else:
                raw_m3u8_url = f"https://{server_key}new.newkso.ru/{server_key}/{channel_key}/mono.m3u8"

            return raw_m3u8_url

        except requests.RequestException as e:
            print(f"[!] Errore richiesta in get_final_m3u8 per {iframe_url}: {e}")
            return None
        except json.JSONDecodeError:
            print(f"[!] Errore parsing JSON da server_lookup per {iframe_url}")
            return None
        except Exception as e:
            print(f"[!] Errore imprevisto in get_final_m3u8 per {iframe_url}: {e}")
            return None

    def get_stream_from_channel_id(channel_id):
        embed_url = f"{LINK_DADDY.rstrip('/')}/embed/stream-{channel_id}.php"
        iframe = get_iframe_url(embed_url)
        if iframe:
            return get_final_m3u8(iframe)
        return None

    def fetch_channels_from_daddylive_page(page_url, base_daddy_url):
        print(f"Tentativo di fetch dei canali da: {page_url}")
        channels = []
        seen_daddy_channel_ids = set()
        try:
            response = session.get(page_url, timeout=HTTP_TIMEOUT, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            non_italian_markers = [
                " (de)", " (fr)", " (es)", " (uk)", " (us)", " (pt)", " (gr)", " (nl)", " (tr)", " (ru)",
                " deutsch", " france", " español", " arabic", " greek", " turkish", " russian", " albania",
                " portugal" 
            ]

            grid_items = soup.find_all('div', class_='grid-item')
            print(f"Trovati {len(grid_items)} elementi 'grid-item' nella pagina Daddylive.")

            for item in grid_items:
                link_tag = item.find('a', href=re.compile(r'/stream/stream-\d+\.php'))
                if not link_tag:
                    continue

                strong_tag = link_tag.find('strong')
                if not strong_tag:
                    continue

                channel_name_raw = strong_tag.text.strip()
                href = link_tag.get('href')
                
                channel_id_match = re.search(r'/stream/stream-(\d+)\.php', href)

                if channel_id_match and channel_name_raw:
                    channel_id = channel_id_match.group(1)
                    lower_channel_name = channel_name_raw.lower()

                    if channel_id in seen_daddy_channel_ids:
                        print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché l'ID è già stato processato.")
                        continue 

                    if "italy" in lower_channel_name:
                        is_confirmed_non_italian_by_marker = False
                        for marker in non_italian_markers:
                            if marker in lower_channel_name:
                                is_confirmed_non_italian_by_marker = True
                                print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché, pur contenendo 'italy', ha anche un marcatore non italiano: '{marker}'")
                                break
                        
                        if not is_confirmed_non_italian_by_marker:
                            seen_daddy_channel_ids.add(channel_id)
                            print(f"Trovato canale potenzialmente ITALIANO (Daddylive HTML): {channel_name_raw}, ID: {channel_id}. Tentativo di risoluzione stream...")
                            stream_url = get_stream_from_channel_id(channel_id)
                            if stream_url:
                                channels.append((channel_name_raw, stream_url))
                                print(f"Risolto e aggiunto stream per {channel_name_raw}: {stream_url}")
                            else:
                                print(f"Impossibile risolvere lo stream per {channel_name_raw} (ID: {channel_id})")

            if not channels:
                print(f"Nessun canale estratto/risolto da {page_url}. Controlla la logica di parsing o la struttura della pagina.")

        except requests.RequestException as e:
            print(f"Errore durante il download da {page_url}: {e}")
        except Exception as e:
            print(f"Errore imprevisto durante il parsing di {page_url}: {e}")
        return channels

    def save_m3u8(organized_channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')
            for category, channels in organized_channels.items():
                channels.sort(key=lambda x: x["name"].lower())
                for ch in channels:
                    tvg_name_cleaned = re.sub(r"\s*\(.*?\)", "", ch["name"])
                    final_url = ch['url']
                    if PROXY:
                        final_url = f"{PROXY.rstrip('/')}{final_url}"
                    
                    f.write(f'#EXTINF:-1 tvg-id="{ch.get("tvg_id", "")}" tvg-name="{tvg_name_cleaned}" tvg-logo="{ch.get("logo", DEFAULT_TVG_ICON)}" group-title="{category}",{ch["name"]}\n')
                    f.write(f"{final_url}\n\n")

    def main():
        epg_root = fetch_epg(EPG_FILE)
        if epg_root is None:
            print("Impossibile recuperare il file EPG, procedura interrotta.")
            return
        logos_dict = fetch_logos(LOGOS_FILE)
        channel_id_map = create_channel_id_map(epg_root)
        
        all_fetched_channels = [] 

        print("\n--- Fetching canali da sorgenti Vavoo (JSON) ---")
        for base_vavoo_url in BASE_URLS:
            json_channels_data = fetch_channels(base_vavoo_url)
            all_fetched_channels.extend(filter_italian_channels(json_channels_data, base_vavoo_url))

        print("\n--- Fetching canali da Daddylive (HTML) ---")
        daddylive_247_page_url = f"{LINK_DADDY.rstrip('/')}/24-7-channels.php"
        scraped_daddylive_channels = fetch_channels_from_daddylive_page(daddylive_247_page_url, LINK_DADDY)

        processed_scraped_channels = []
        seen_scraped_names = {}
        seen_daddy_transformed_base_names = {}
        for raw_name, stream_url in scraped_daddylive_channels:
            name_after_initial_clean = clean_channel_name(raw_name)

            base_daddy_name = re.sub(r'italy', '', name_after_initial_clean, flags=re.IGNORECASE).strip()
            base_daddy_name = re.sub(r'\s+', ' ', base_daddy_name).strip()
            base_daddy_name = base_daddy_name.upper()
            sky_calcio_rename_map = {
                "SKY CALCIO 1": "SKY SPORT 251",
                "SKY CALCIO 2": "SKY SPORT 252",
                "SKY CALCIO 3": "SKY SPORT 253",
                "SKY CALCIO 4": "SKY SPORT 254",
                "SKY CALCIO 5": "SKY SPORT 255",
                "SKY CALCIO 6": "SKY SPORT 256",
                "SKY CALCIO 7": "DAZN 1"
            }

            if base_daddy_name in sky_calcio_rename_map:
                original_bdn_for_log = base_daddy_name
                base_daddy_name = sky_calcio_rename_map[base_daddy_name]
                print(f"Rinominato canale Daddylive (HTML) da '{original_bdn_for_log}' a '{base_daddy_name}'")

            if base_daddy_name == "DAZN" or base_daddy_name == "DAZN2":
                print(f"Skipping canale Daddylive (HTML) a causa della regola DAZN: {raw_name} (base trasformato: {base_daddy_name})")
                continue
            
            count = seen_daddy_transformed_base_names.get(base_daddy_name, 0) + 1
            seen_daddy_transformed_base_names[base_daddy_name] = count
            
            final_name = base_daddy_name
            if count > 1:
                final_name = f"{base_daddy_name} ({count})" 
            final_name = f"{final_name} (D)"
            
            processed_scraped_channels.append((final_name, stream_url))

        all_fetched_channels.extend(processed_scraped_channels)

        manual_channels_data = get_manual_channels()

        print("\n--- Organizzazione canali ---")
        organized_channels = {category: [] for category in CATEGORY_KEYWORDS.keys()}

        for name, url in all_fetched_channels:
            category = classify_channel(name)

            name_for_lookup = name
            if name_for_lookup.upper().endswith(" (D)"):
                match_d_suffix = re.search(r'\s*\([Dd]\)$', name_for_lookup)
                if match_d_suffix:
                    name_for_lookup = name_for_lookup[:match_d_suffix.start()]
            
            name_for_lookup = re.sub(r'\s*\(\d+\)$', '', name_for_lookup).strip()

            final_logo_url = DEFAULT_TVG_ICON 
            sky_sport_daddy_logo = "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png"

            if name.upper().endswith(" (D)"): 
                if re.match(r"SKY SPORT (25[1-6])$", name_for_lookup.upper()):
                    final_logo_url = sky_sport_daddy_logo
                    print(f"Logo specifico '{final_logo_url}' assegnato a Daddylive channel '{name}' (lookup name: '{name_for_lookup}')")
                else:
                    final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)
            else:
                final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)

            organized_channels.setdefault(category, []).append({
                "name": name, 
                "url": url,
                "tvg_id": channel_id_map.get(normalize_channel_name(name_for_lookup), ""),
                "logo": final_logo_url 
            })

        for ch_data in manual_channels_data:
            cat = ch_data.get("category") or classify_channel(ch_data["name"])
            organized_channels.setdefault(cat, []).append({
                "name": ch_data["name"],
                "url": ch_data["url"],
                "tvg_id": ch_data.get("tvg_id", ""),
                "logo": ch_data.get("logo", DEFAULT_TVG_ICON)
            })

        save_m3u8(organized_channels)
        print(f"\nFile {OUTPUT_FILE} creato con successo!")

    if __name__ == "__main__":
        main()

def world_channels_generator():
    print("Eseguendo il world_channels_generator.py...")
    import requests
    import re
    import os
    from collections import defaultdict
    from dotenv import load_dotenv
    
    load_dotenv()

    PROXY = os.getenv("PROXYIP", "").strip()
    OUTPUT_FILE = "world.m3u8"
    BASE_URLS = [
        "https://vavoo.to"
    ]
    
    def fetch_channels(base_url):
        try:
            response = requests.get(f"{base_url}/channels", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []
    
    def clean_channel_name(name):
        return re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name).strip()
    
    def save_m3u8(channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    
        grouped_channels = defaultdict(list)
        for name, url, country in channels:
            grouped_channels[country].append((name, url))
    
        sorted_categories = sorted(grouped_channels.keys())
    
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')
    
            for country in sorted_categories:
                grouped_channels[country].sort(key=lambda x: x[0].lower())
    
                for name, url in grouped_channels[country]:
                    f.write(f'#EXTINF:-1 tvg-name="{name}" group-title="{country}", {name}\n')
                    f.write(f"{PROXY}{url}\n\n")
    
    def main():
        all_channels = []
        for url in BASE_URLS:
            channels = fetch_channels(url)
            for ch in channels:
                clean_name = clean_channel_name(ch["name"])
                country = ch.get("country", "Unknown") 
                all_channels.append((clean_name, f"{url}/play/{ch['id']}/index.m3u8", country))
    
        save_m3u8(all_channels)
        print(f"File {OUTPUT_FILE} creato con successo!")
    
    if __name__ == "__main__":
        main()

def removerworld():
    import os
    
    files_to_delete = ["eventisps.m3u8", "world.m3u8", "channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")
            
def remover():
    import os
    
    files_to_delete = ["eventisps.m3u8", "channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

def main():
    try:
        schedule_success = schedule_extractor()
    except Exception as e:
        print(f"Errore durante l'esecuzione di schedule_extractor: {e}")
        
    # try:
    #     eventi_sps()
    # except Exception as e:
    #     print(f"Errore durante l'esecuzione di eventi_sps: {e}")
    #     return

    eventi_en = os.getenv("EVENTI_EN", "no").strip().lower()
    world_flag = os.getenv("WORLD", "si").strip().lower()

    # try:
    #     if eventi_en == "si":
    #         epg_eventi_generator_world()
    #     else:
    #         epg_eventi_generator()
    # except Exception as e:
    #     print(f"Errore durante la generazione EPG eventi: {e}")
    #     return

    # try:
    #     if eventi_en == "si":
    #         eventi_m3u8_generator_world()
    #     else:
    #         eventi_m3u8_generator()
    # except Exception as e:
    #     print(f"Errore durante la generazione eventi.m3u8: {e}")
    #     return

    try:
        epg_merger()
    except Exception as e:
        print(f"Errore durante l'esecuzione di epg_merger: {e}")
        return

    try:
        italy_channels()
    except Exception as e:
        print(f"Errore durante l'esecuzione di italy_channels: {e}")
        return

    try:
        if world_flag == "si":
            world_channels_generator()
            merger_playlistworld()
            removerworld()
        elif world_flag == "no":
            merger_playlist()
            remover()
        else:
            print(f"Valore WORLD non valido: '{world_flag}'. Usa 'si' o 'no'.")
            return
    except Exception as e:
        print(f"Errore nella fase finale: {e}")
        return

    print("Tutti gli script sono stati eseguiti correttamente!")

if __name__ == "__main__":
    main()
