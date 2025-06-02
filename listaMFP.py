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
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  # File locale
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"  # Remoto
    url5 = "eventisps.m3u8"      # File locale (aggiunto come in merger_playlistworld)
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist5 = download_playlist(url5) # Aggiunto download per url5
    
    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist5 # Aggiunto playlist5 all'unione
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")
    
# Funzione per il primo script (merger_playlist.py)
def merger_playlistworld():
    # Codice del primo script qui
    # Aggiungi il codice del tuo script "merger_playlist.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo il merger_playlist.py...")
    # Il codice che avevi nello script "merger_playlist.py" va qui, senza modifiche.
    import requests
    import os
    from dotenv import load_dotenv

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    NOMEREPO = os.getenv("NOMEREPO", "").strip()
    NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
    
    # Percorsi o URL delle playlist M3U8
    url1 = "channels_italy.m3u8"  # File locale
    url2 = "eventi.m3u8"   
    url3 = "https://raw.githubusercontent.com/Brenders/Pluto-TV-Italia-M3U/main/PlutoItaly.m3u"  # Remoto
    url4 = "world.m3u8"           # File locale
    url5 = "eventisps.m3u8"      # File locale
    
    # Funzione per scaricare o leggere una playlist
    def download_playlist(source, append_params=False, exclude_group_title=None):
        if source.startswith("http"):
            response = requests.get(source)
            response.raise_for_status()
            playlist = response.text
        else:
            with open(source, 'r', encoding='utf-8') as f:
                playlist = f.read()
        
        # Rimuovi intestazione iniziale
        playlist = '\n'.join(line for line in playlist.split('\n') if not line.startswith('#EXTM3U'))
    
        if exclude_group_title:
            playlist = '\n'.join(line for line in playlist.split('\n') if exclude_group_title not in line)
    
        return playlist
    
    # Ottieni la directory dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Scarica/leggi le playlist
    playlist1 = download_playlist(url1)
    playlist2 = download_playlist(url2, append_params=True)
    playlist3 = download_playlist(url3)
    playlist4 = download_playlist(url4, exclude_group_title="Italy")
    playlist5 = download_playlist(url5)
    
    # Unisci le playlist
    lista = playlist1 + "\n" + playlist2 + "\n" + playlist3 + "\n" + playlist4 + "\n" + playlist5
    
    # Aggiungi intestazione EPG
    lista = f'#EXTM3U x-tvg-url="https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/refs/heads/main/epg.xml"\n' + lista
    
    # Salva la playlist
    output_filename = os.path.join(script_directory, "lista.m3u")
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(lista)
    
    print(f"Playlist combinata salvata in: {output_filename}")

# Funzione per il secondo script (epg_merger.py)
def epg_merger():
    # Codice del secondo script qui
    # Aggiungi il codice del tuo script "epg_merger.py" in questa funzione.
    # Ad esempio:
    print("Eseguendo l'epg_merger.py...")
    # Il codice che avevi nello script "epg_merger.py" va qui, senza modifiche.
    import requests
    import gzip
    import os
    import xml.etree.ElementTree as ET
    import io

    # URL dei file GZIP o XML da elaborare
    urls_gzip = [
        'https://www.open-epg.com/files/italy1.xml',
        'https://www.open-epg.com/files/italy2.xml',
        'https://www.open-epg.com/files/italy3.xml',
        'https://www.open-epg.com/files/italy4.xml',
        'https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz'
    ]

    # File di output
    output_xml = 'epg.xml'    # Nome del file XML finale

    # URL remoto di it.xml
    url_it = 'https://raw.githubusercontent.com/matthuisman/i.mjh.nz/master/PlutoTV/it.xml'

    # File eventi locale
    path_eventi = 'eventi.xml'

    def download_and_parse_xml(url):
        """Scarica un file .xml o .gzip e restituisce l'ElementTree."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Prova a decomprimere come GZIP
            try:
                with gzip.open(io.BytesIO(response.content), 'rb') as f_in:
                    xml_content = f_in.read()
            except (gzip.BadGzipFile, OSError):
                # Non è un file gzip, usa direttamente il contenuto
                xml_content = response.content

            return ET.ElementTree(ET.fromstring(xml_content))
        except requests.exceptions.RequestException as e:
            print(f"Errore durante il download da {url}: {e}")
        except ET.ParseError as e:
            print(f"Errore nel parsing del file XML da {url}: {e}")
        return None

    # Creare un unico XML vuoto
    root_finale = ET.Element('tv')
    tree_finale = ET.ElementTree(root_finale)

    # Processare ogni URL
    for url in urls_gzip:
        tree = download_and_parse_xml(url)
        if tree is not None:
            root = tree.getroot()
            for element in root:
                root_finale.append(element)

    # Aggiungere eventi.xml da file locale
    if os.path.exists(path_eventi):
        try:
            tree_eventi = ET.parse(path_eventi)
            root_eventi = tree_eventi.getroot()
            for programme in root_eventi.findall(".//programme"):
                root_finale.append(programme)
        except ET.ParseError as e:
            print(f"Errore nel parsing del file eventi.xml: {e}")
    else:
        print(f"File non trovato: {path_eventi}")

    # Aggiungere it.xml da URL remoto
    tree_it = download_and_parse_xml(url_it)
    if tree_it is not None:
        root_it = tree_it.getroot()
        for programme in root_it.findall(".//programme"):
            root_finale.append(programme)
    else:
        print(f"Impossibile scaricare o analizzare il file it.xml da {url_it}")

    # Funzione per pulire attributi
    def clean_attribute(element, attr_name):
        if attr_name in element.attrib:
            old_value = element.attrib[attr_name]
            new_value = old_value.replace(" ", "").lower()
            element.attrib[attr_name] = new_value

    # Pulire gli ID dei canali
    for channel in root_finale.findall(".//channel"):
        clean_attribute(channel, 'id')

    # Pulire gli attributi 'channel' nei programmi
    for programme in root_finale.findall(".//programme"):
        clean_attribute(programme, 'channel')

    # Salvare il file XML finale
    with open(output_xml, 'wb') as f_out:
        tree_finale.write(f_out, encoding='utf-8', xml_declaration=True)
    print(f"File XML salvato: {output_xml}")
             
# Funzione per il terzo script (eventi_m3u8_generator.py)
def eventi_m3u8_generator_world():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
    import json
    import re
    import requests
    import urllib.parse # Consolidato
    from datetime import datetime, timedelta
    from dateutil import parser
    import os
    from dotenv import load_dotenv
    from PIL import Image, ImageDraw, ImageFont
    import io # Aggiunto per encoding URL
    import time
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    PROXY = os.getenv("PROXYIP", "").strip()  # Proxy HLS 
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
    MFP_IP = os.getenv("IPMFP", "").strip()
    MFP_PASSWORD = os.getenv("PASSMFP", "").strip()
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo
        """
        # import re # 're' è già importato a livello di funzione
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        cleaned = re.sub(r'[^a-zA-Z0-9Ã-Ã¿]', '', tvg_id)
        return cleaned.lower()
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerà l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id): 
        # Costruisce l'URL .php per Daddylive
        # La seconda definizione di eventi_m3u8_generator_world usa /embed/stream-{id}.php
        embed_url = f"{LINK_DADDY}/embed/stream-{channel_id}.php" 

        if MFP_IP:
            encoded_php_url = urllib.parse.quote(embed_url, safe='')
            return f"{MFP_IP.rstrip('/')}/extractor/video?host=DLHD&api_password={MFP_PASSWORD}&redirect_stream=true&d={encoded_php_url}"
        else:
            print(f"[!] MFP_IP non impostato. Impossibile generare l'URL extractor per il canale Daddylive {channel_id}.")
            return None
     
    # def clean_category_name(name): # Rimossa definizione duplicata
    #     # Rimuove tag html come </span> o simili
    #     return re.sub(r'<[^>]+>', '', name).strip()
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it", "uk", "tnt", "usa", "tennis channel", "tennis stream", "la"} 
        now = datetime.now()  # ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
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
            
            # Determina se processare questa data
            process_this_date = False
            is_yesterday_early_morning_event_check = False

            if date_obj == now.date():
                process_this_date = True
            elif date_obj == yesterday_date:
                process_this_date = True
                is_yesterday_early_morning_event_check = True # Flag per eventi di ieri mattina presto
            else:
                # Salta date che non sono né oggi né ieri
                continue

            if not process_this_date:
                continue
     
            for category_raw, event_items in sections.items(): 
                category = clean_category_name(category_raw) 
                if category not in categorized_channels: 
                    categorized_channels[category] = [] 
     
                for item in event_items: 
                    time_str = item.get("time", "00:00") # Orario originale dal JSON
                    event_title = item.get("event", "Evento") 
     
                    try: 
                        # Parse orario evento originale (dal JSON)
                        original_event_time_obj = datetime.strptime(time_str, "%H:%M").time()

                        # Costruisci datetime completo dell'evento con la sua data originale
                        # e l'orario originale, poi applica il timedelta(hours=2) (per "correzione timezone?")
                        # Questo event_datetime_adjusted è quello che viene usato per il filtro "meno di 2 ore fa" per oggi
                        # e per il nome del canale.
                        event_datetime_adjusted_for_display_and_filter = datetime.combine(date_obj, original_event_time_obj) + timedelta(hours=2)

                        if is_yesterday_early_morning_event_check:
                            # Filtro per eventi di ieri mattina presto (00:00 - 04:00, ora JSON)
                            start_filter_time = datetime.strptime("00:00", "%H:%M").time()
                            end_filter_time = datetime.strptime("04:00", "%H:%M").time()
                            # Confronta l'orario originale dell'evento
                            if not (start_filter_time <= original_event_time_obj <= end_filter_time):
                                # Evento di ieri, ma non nell'intervallo 00:00-04:00 -> salto
                                continue
                        else: # Eventi di oggi
                            # Controllo: includi solo se l'evento è iniziato da meno di 2 ore
                            # Usa event_datetime_adjusted_for_display_and_filter che ha già il +2h
                            if now - event_datetime_adjusted_for_display_and_filter > timedelta(hours=2):
                                # Evento di oggi iniziato da più di 2 ore -> salto
                                continue
                        
                        time_formatted = event_datetime_adjusted_for_display_and_filter.strftime("%H:%M")
                    except Exception as e_time:
                        print(f"[!] Errore parsing orario '{time_str}' per evento '{event_title}' in data '{date_key}': {e_time}")
                        time_formatted = time_str # Fallback
     
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
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                            }) 
     
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 
     
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Aggiungi il canale iniziale/informativo
            f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live",DADDYLIVE\n')
            f.write("https://example.com.m3u8\n\n")
     
            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
     
                # Spacer con nome categoria pulito e group-title "Eventi Live" 
                f.write(f'#EXTINF:-1 tvg-name="{category}" group-title="Eventi Live",--- {category} ---\nhttps://exemple.m3u8\n\n') 
     
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title)
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        stream = get_stream_from_channel_id(channel_id) 
                        if stream: 
                            cleaned_event_id = clean_tvg_id(event_title) # Usa event_title per tvg-id
                            f.write(f'#EXTINF:-1 tvg-id="{cleaned_event_id}" tvg-name="{tvg_name}"{logo_attribute} group-title="Eventi Live",{tvg_name}\n{stream}\n\n')
                            print(f"[✓] {tvg_name}" + (f" (logo trovato)" if logo_url else " (nessun logo trovato)")) 
                        else: 
                            print(f"[✗] {tvg_name} - Nessuno stream trovato") 
                    except Exception as e: 
                        print(f"[!] Errore su {tvg_name}: {e}") 
     
    # Esegui la generazione quando la funzione viene chiamata
    generate_m3u_from_schedule(JSON_FILE, OUTPUT_FILE)

# Funzione per il terzo script (eventi_m3u8_generator.py)
def eventi_m3u8_generator():
    # Codice del terzo script qui
    # Aggiungi il codice del tuo script "eventi_m3u8_generator.py" in questa funzione.
    print("Eseguendo l'eventi_m3u8_generator.py...")
    # Il codice che avevi nello script "eventi_m3u8_generator.py" va qui, senza modifiche.
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
    import urllib.parse # Aggiunto per encoding URL
    import time

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    MFP_IP = os.getenv("IPMFP", "").strip()
    MFP_PASSWORD = os.getenv("PASSMFP", "").strip()
    JSON_FILE = "daddyliveSchedule.json" 
    OUTPUT_FILE = "eventi.m3u8" 
     
    HEADERS = { 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36" 
    } 
     
    HTTP_TIMEOUT = 10 
    session = requests.Session() 
    session.headers.update(HEADERS) 
    # Definisci current_time e three_hours_in_seconds per la logica di caching
    current_time = time.time()
    three_hours_in_seconds = 3 * 60 * 60
    
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip()
        
    def clean_tvg_id(tvg_id):
        """
        Pulisce il tvg-id rimuovendo caratteri speciali, spazi e convertendo tutto in minuscolo
        """
        import re
        # Rimuove caratteri speciali comuni mantenendo solo lettere e numeri
        cleaned = re.sub(r'[^a-zA-Z0-9Ã-Ã¿]', '', tvg_id)
        return cleaned.lower()
     
    def search_logo_for_event(event_name): 
        """ 
        Cerca un logo per l'evento specificato utilizzando un motore di ricerca 
        Restituisce l'URL dell'immagine trovata o None se non trovata 
        """ 
        try: 
            # Rimuovi eventuali riferimenti all'orario dal nome dell'evento
            # Cerca pattern come "Team A vs Team B (20:00)" e rimuovi la parte dell'orario
            clean_event_name = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_name)
            # Se c'Ã¨ un ':', prendi solo la parte dopo
            if ':' in clean_event_name:
                clean_event_name = clean_event_name.split(':', 1)[1].strip()
            
            # Verifica se l'evento contiene "vs" o "-" per identificare le due squadre
            teams = None
            if " vs " in clean_event_name:
                teams = clean_event_name.split(" vs ")
            elif " VS " in clean_event_name:
                teams = clean_event_name.split(" VS ")
            elif " VS. " in clean_event_name:
                teams = clean_event_name.split(" VS. ")
            elif " vs. " in clean_event_name:
                teams = clean_event_name.split(" vs. ")
            
            # Se abbiamo identificato due squadre, cerchiamo i loghi separatamente
            if teams and len(teams) == 2:
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                
                print(f"[🔍] Ricerca logo per Team 1: {team1}")
                logo1_url = search_team_logo(team1)
                
                print(f"[🔍] Ricerca logo per Team 2: {team2}")
                logo2_url = search_team_logo(team2)
                
                # Se abbiamo trovato entrambi i loghi, creiamo un'immagine combinata
                if logo1_url and logo2_url:
                    # Scarica i loghi e l'immagine VS
                    try:
                        from os.path import exists, getmtime
                        
                        # Crea la cartella logos se non esiste
                        logos_dir = "logos"
                        os.makedirs(logos_dir, exist_ok=True)
                        
                        # Verifica se l'immagine combinata esiste giÃ  e non Ã¨ obsoleta
                        output_filename = f"logos/{team1}_vs_{team2}.png"
                        if exists(output_filename):
                            file_age = current_time - os.path.getmtime(output_filename)
                            if file_age <= three_hours_in_seconds:
                                print(f"[✓] Utilizzo immagine combinata esistente: {output_filename}")
                                
                                # Carica le variabili d'ambiente per GitHub
                                NOMEREPO = os.getenv("NOMEREPO", "").strip()
                                NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                                
                                # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                                if NOMEGITHUB and NOMEREPO:
                                    github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                                    print(f"[✓] URL GitHub generato per logo esistente: {github_raw_url}")
                                    return github_raw_url
                                else:
                                    # Altrimenti restituisci il percorso locale
                                    return output_filename
                        
                        # Scarica i loghi
                        img1, img2 = None, None
                        
                        if logo1_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response1 = requests.get(logo1_url, headers=logo_headers, timeout=10)
                                response1.raise_for_status() # Controlla errori HTTP
                                if 'image' in response1.headers.get('Content-Type', '').lower():
                                    img1 = Image.open(io.BytesIO(response1.content))
                                    print(f"[✓] Logo1 scaricato con successo da: {logo1_url}")
                                else:
                                    print(f"[!] URL logo1 ({logo1_url}) non è un'immagine (Content-Type: {response1.headers.get('Content-Type')}).")
                                    logo1_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo1 ({logo1_url}): {e_req}")
                                logo1_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo1 ({logo1_url}): {e_pil}")
                                logo1_url = None
                        
                        if logo2_url:
                            try:
                                # Aggiungi un User-Agent simile a un browser
                                logo_headers = {
                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                                }
                                response2 = requests.get(logo2_url, headers=logo_headers, timeout=10)
                                response2.raise_for_status() # Controlla errori HTTP
                                if 'image' in response2.headers.get('Content-Type', '').lower():
                                    img2 = Image.open(io.BytesIO(response2.content))
                                    print(f"[✓] Logo2 scaricato con successo da: {logo2_url}")
                                else:
                                    print(f"[!] URL logo2 ({logo2_url}) non è un'immagine (Content-Type: {response2.headers.get('Content-Type')}).")
                                    logo2_url = None # Invalida URL se non è un'immagine
                            except requests.exceptions.RequestException as e_req:
                                print(f"[!] Errore scaricando logo2 ({logo2_url}): {e_req}")
                                logo2_url = None
                            except Exception as e_pil: # Errore specifico da PIL durante Image.open
                                print(f"[!] Errore PIL aprendo logo2 ({logo2_url}): {e_pil}")
                                logo2_url = None
                        
                        # Carica l'immagine VS (assicurati che esista nella directory corrente)
                        vs_path = "vs.png"
                        if exists(vs_path):
                            img_vs = Image.open(vs_path)
                            # Converti l'immagine VS in modalitÃ  RGBA se non lo Ã¨ giÃ 
                            if img_vs.mode != 'RGBA':
                                img_vs = img_vs.convert('RGBA')
                        else:
                            # Crea un'immagine di testo "VS" se il file non esiste
                            img_vs = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                            from PIL import ImageDraw, ImageFont
                            draw = ImageDraw.Draw(img_vs)
                            try:
                                font = ImageFont.truetype("arial.ttf", 40)
                            except:
                                font = ImageFont.load_default()
                            draw.text((30, 30), "VS", fill=(255, 0, 0), font=font)
                        
                        # Procedi con la combinazione solo se entrambi i loghi sono stati caricati con successo
                        if not (img1 and img2):
                            print(f"[!] Impossibile caricare entrambi i loghi come immagini valide per la combinazione. Logo1 caricato: {bool(img1)}, Logo2 caricato: {bool(img2)}.")
                            raise ValueError("Uno o entrambi i loghi non sono stati caricati correttamente.") # Questo forzerà l'except sottostante
                        
                        # Ridimensiona le immagini a dimensioni uniformi
                        size = (150, 150)
                        img1 = img1.resize(size)
                        img2 = img2.resize(size)
                        img_vs = img_vs.resize((100, 100))
                        
                        # Assicurati che tutte le immagini siano in modalitÃ  RGBA per supportare la trasparenza
                        if img1.mode != 'RGBA':
                            img1 = img1.convert('RGBA')
                        if img2.mode != 'RGBA':
                            img2 = img2.convert('RGBA')
                        
                        # Crea una nuova immagine con spazio per entrambi i loghi e il VS
                        combined_width = 300
                        combined = Image.new('RGBA', (combined_width, 150), (255, 255, 255, 0))
                        
                        # Posiziona le immagini con il VS sovrapposto al centro
                        # Posiziona il primo logo a sinistra
                        combined.paste(img1, (0, 0), img1)
                        # Posiziona il secondo logo a destra
                        combined.paste(img2, (combined_width - 150, 0), img2)
                        
                        # Posiziona il VS al centro, sovrapposto ai due loghi
                        vs_x = (combined_width - 100) // 2
                        
                        # Crea una copia dell'immagine combinata prima di sovrapporre il VS
                        # Questo passaggio Ã¨ importante per preservare i dettagli dei loghi sottostanti
                        combined_with_vs = combined.copy()
                        combined_with_vs.paste(img_vs, (vs_x, 25), img_vs)
                        
                        # Usa l'immagine con VS sovrapposto
                        combined = combined_with_vs
                        
                        # Salva l'immagine combinata
                        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                        combined.save(output_filename)
                        
                        print(f"[✓] Immagine combinata creata: {output_filename}")
                        
                        # Carica le variabili d'ambiente per GitHub
                        NOMEREPO = os.getenv("NOMEREPO", "").strip()
                        NOMEGITHUB = os.getenv("NOMEGITHUB", "").strip()
                        
                        # Se le variabili GitHub sono disponibili, restituisci l'URL raw di GitHub
                        if NOMEGITHUB and NOMEREPO:
                            github_raw_url = f"https://raw.githubusercontent.com/{NOMEGITHUB}/{NOMEREPO}/main/{output_filename}"
                            print(f"[✓] URL GitHub generato: {github_raw_url}")
                            return github_raw_url
                        else:
                            # Altrimenti restituisci il percorso locale
                            return output_filename
                        
                    except Exception as e:
                        print(f"[!] Errore nella creazione dell'immagine combinata: {e}")
                        # Se fallisce, restituisci solo il primo logo trovato
                        return logo1_url or logo2_url
                
                # Se non abbiamo trovato entrambi i loghi, restituisci quello che abbiamo
                return logo1_url or logo2_url
            if ':' in event_name:
                # Usa la parte prima dei ":" per la ricerca
                prefix_name = event_name.split(':', 1)[0].strip()
                print(f"[🔍] Tentativo ricerca logo con prefisso: {prefix_name}")
                
                # Prepara la query di ricerca con il prefisso
                search_query = urllib.parse.quote(f"{prefix_name} logo")
                
                # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                    # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                            # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                            for match in matches:
                                if '.png' in match.lower() or '.svg' in match.lower():
                                    print(f"[✓] Logo trovato con prefisso: {match}")
                                    return match
                            # Se non troviamo PNG o SVG, prendi il primo risultato
                            print(f"[✓] Logo trovato con prefisso: {matches[0]}")
                            return matches[0]
            
            # Se non riusciamo a identificare le squadre e il prefisso non ha dato risultati, procedi con la ricerca normale
            print(f"[🔍] Ricerca standard per: {clean_event_name}")
            
            
            # Se non riusciamo a identificare le squadre, procedi con la ricerca normale
            # Prepara la query di ricerca piÃ¹ specifica
            search_query = urllib.parse.quote(f"{clean_event_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{clean_event_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{event_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None

    def search_team_logo(team_name):
        """
        Funzione dedicata alla ricerca del logo di una singola squadra
        """
        try:
            # Prepara la query di ricerca specifica per la squadra
            search_query = urllib.parse.quote(f"{team_name} logo")
            
            # Utilizziamo l'API di Bing Image Search con parametri migliorati
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
                # Metodo 1: Cerca pattern per murl (URL dell'immagine media)
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
                        # Prendi il primo risultato che sembra un logo (preferibilmente PNG o SVG)
                        for match in matches:
                            if '.png' in match.lower() or '.svg' in match.lower():
                                return match
                        # Se non troviamo PNG o SVG, prendi il primo risultato
                        return matches[0]
                
                # Metodo alternativo: cerca JSON incorporato nella pagina
                json_match = re.search(r'var\s+IG\s*=\s*(\{.+?\});\s*', response.text)
                if json_match:
                    try:
                        # Estrai e analizza il JSON
                        json_str = json_match.group(1)
                        # Pulisci il JSON se necessario
                        json_str = re.sub(r'([{,])\s*([a-zA-Z0-9_]+):', r'\1"\2":', json_str)
                        data = json.loads(json_str)
                        
                        # Cerca URL di immagini nel JSON
                        if 'images' in data and len(data['images']) > 0:
                            for img in data['images']:
                                if 'murl' in img:
                                    return img['murl']
                    except Exception as e:
                        print(f"[!] Errore nell'analisi JSON: {e}")
                
                print(f"[!] Nessun logo trovato per '{team_name}' con i pattern standard")
                
                # Ultimo tentativo: cerca qualsiasi URL di immagine nella pagina
                any_img = re.search(r'(https?://[^"\']+\.(?:png|jpg|jpeg|svg|webp))', response.text)
                if any_img:
                    return any_img.group(1)
                    
        except Exception as e: 
            print(f"[!] Errore nella ricerca del logo per '{team_name}': {e}") 
        
        # Se non troviamo nulla, restituiamo None 
        return None
     
    def get_stream_from_channel_id(channel_id): 
        # Costruisce l'URL .php per Daddylive
        # eventi_m3u8_generator usa /embed/stream-{id}.php
        embed_url = f"{LINK_DADDY}/embed/stream-{channel_id}.php" 

        if MFP_IP:
            encoded_php_url = urllib.parse.quote(embed_url, safe='')
            return f"{MFP_IP.rstrip('/')}/extractor/video?host=DLHD&api_password={MFP_PASSWORD}&redirect_stream=true&d={encoded_php_url}"
        else:
            print(f"[!] MFP_IP non impostato. Impossibile generare l'URL extractor per il canale Daddylive {channel_id}.")
            return None
     
    def clean_category_name(name): 
        # Rimuove tag html come </span> o simili 
        return re.sub(r'<[^>]+>', '', name).strip() 
     
    def extract_channels_from_json(path): 
        keywords = {"italy", "rai", "italia", "it"} 
        now = datetime.now()  # ora attuale completa (data+ora) 
        yesterday_date = (now - timedelta(days=1)).date() # Data di ieri
     
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
     
            # filtro solo per eventi del giorno corrente 
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
                        # Parse orario evento 
                        time_obj = datetime.strptime(time_str, "%H:%M") + timedelta(hours=2)  # correzione timezone? 
     
                        # crea datetime completo con data evento e orario evento 
                        event_datetime = datetime.combine(date_obj, time_obj.time()) 
     
                        # Controllo: includi solo se l'evento è iniziato da meno di 2 ore 
                        if now - event_datetime > timedelta(hours=2): 
                            # Evento iniziato da più di 2 ore -> salto 
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
                                "event_title": event_title  # Aggiungiamo il titolo dell'evento per la ricerca del logo
                            }) 
     
        return categorized_channels 
     
    def generate_m3u_from_schedule(json_file, output_file): 
        categorized_channels = extract_channels_from_json(json_file) 
     
        with open(output_file, "w", encoding="utf-8") as f: 
            f.write("#EXTM3U\n") 

            # Aggiungi il canale iniziale/informativo
            f.write(f'#EXTINF:-1 tvg-name="DADDYLIVE" group-title="Eventi Live",DADDYLIVE\n')
            f.write("https://example.com.m3u8\n\n")
     
            for category, channels in categorized_channels.items(): 
                if not channels: 
                    continue 
     
                # Spacer con nome categoria pulito e group-title "Eventi Live" 
                f.write(f'#EXTINF:-1 tvg-name="{category}" group-title="Eventi Live",--- {category} ---\nhttps://exemple.m3u8\n\n') 
     
                for ch in channels: 
                    tvg_name = ch["tvg_name"] 
                    channel_id = ch["channel_id"] 
                    event_title = ch["event_title"]  # Otteniamo il titolo dell'evento
                    
                    # Cerca un logo per questo evento
                    # Rimuovi l'orario dal titolo dell'evento prima di cercare il logo
                    clean_event_title = re.sub(r'\s*\(\d{1,2}:\d{2}\)\s*$', '', event_title)
                    print(f"[🔍] Ricerca logo per: {clean_event_title}") 
                    logo_url = search_logo_for_event(clean_event_title)
                    logo_attribute = f' tvg-logo="{logo_url}"' if logo_url else ''
     
                    try: 
                        stream = get_stream_from_channel_id(channel_id) 
                        if stream: 
                            cleaned_event_id = clean_tvg_id(event_title) # Usa event_title per tvg-id
                            f.write(f'#EXTINF:-1 tvg-id="{cleaned_event_id}" tvg-name="{tvg_name}"{logo_attribute} group-title="Eventi Live",{tvg_name}\n{stream}\n\n')
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
    from datetime import datetime # Aggiunto import per la data corrente
    from dotenv import load_dotenv

    load_dotenv()

    # Prefisso per il proxy dello stream
    MFP_IP = os.getenv("IPMFP", "").strip()
    MFP_PASSWORD = os.getenv("PASSMFP", "").strip()

    # URL di partenza (homepage o pagina con elenco eventi)
    base_url = "https://www.sportstreaming.net/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
        "Origin": "https://www.sportstreaming.net",
        "Referer": "https://www.sportstreaming.net/"
    }

    # Funzione helper per formattare la data dell'evento
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

    # Mappa dei mesi italiani per la formattazione della data
    ITALIAN_MONTHS_MAP = {
        "gennaio": "01", "febbraio": "02", "marzo": "03", "aprile": "04",
        "maggio": "05", "giugno": "06", "luglio": "07", "agosto": "08",
        "settembre": "09", "ottobre": "10", "novembre": "11", "dicembre": "12"
    }

    # Funzione per trovare i link alle pagine evento
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

    # Funzione per estrarre il flusso video e i dettagli dell'evento dalla pagina evento
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

            # Estrai data e ora formattate
            full_event_datetime_str = ""
            event_date_comparable = "" # Conterrà "DD/MM" per il confronto
            event_time_str = ""        # Conterrà "HH:MM"
            date_span = soup.find('span', class_='uk-text-meta uk-text-small')
            if date_span:
                date_text = date_span.get_text(strip=True)
                full_event_datetime_str, event_date_comparable = format_event_date(date_text)
                if full_event_datetime_str:
                    # Estrai solo l'orario (es. "20:45" da "20:45 23/07")
                    time_match = re.match(r'(\d{1,2}:\d{2})', full_event_datetime_str)
                    if time_match:
                        event_time_str = time_match.group(1)
     
            # Estrai il titolo dell'evento dal tag <title>
            event_title_from_html = "Unknown Event"
            title_tag = soup.find('title')
            if title_tag:
                event_title_from_html = title_tag.get_text(strip=True)
                event_title_from_html = re.sub(r'\s*\|\s*Sport Streaming\s*$', '', event_title_from_html, flags=re.IGNORECASE).strip()

            # Estrai informazioni sulla lega/competizione
            league_info = "Event" # Default
            is_perma_channel = "perma" in event_url.lower()

            if is_perma_channel:
                if event_title_from_html and event_title_from_html != "Unknown Event":
                    league_info = event_title_from_html
                # Se il titolo del canale perma non è stato trovato, league_info resta "Event"
            else:
                # Per canali non-perma (eventi specifici), cerca lo span della lega/competizione
                league_spans = soup.find_all(
                    lambda tag: tag.name == 'span' and \
                                'uk-text-small' in tag.get('class', []) and \
                                'uk-text-meta' not in tag.get('class', []) # Escludi lo span della data
                )
                if league_spans:
                    # Prendi il testo del primo span corrispondente, pulito
                    league_info = ' '.join(league_spans[0].get_text(strip=True).split())
                # Se lo span non viene trovato per un evento non-perma, league_info resta "Event"

            return stream_url, event_date_comparable, event_time_str, event_title_from_html, league_info

        except requests.RequestException as e:
            print(f"Errore durante l'accesso a {event_url}: {e}")
            return None, "", "", "Unknown Event", "Event"

    # Funzione per aggiornare il file M3U8
    def update_m3u_file(video_streams, m3u_file="eventisps.m3u8"):
        REPO_PATH = os.getenv('GITHUB_WORKSPACE', '.')
        file_path = os.path.join(REPO_PATH, m3u_file)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")

            # Aggiungi il canale iniziale/informativo
            f.write(f'#EXTINF:-1 tvg-name="SportStreaming.net" group-title="Eventi Live",SportStreaming.net\n')
            f.write("https://example.com.m3u8\n\n")

            perma_count = 1

            for event_url, stream_url, event_time, event_title, league_info in video_streams:
                if not stream_url:
                    continue

                # Determina se è un canale permanente o standard
                is_perma = "perma" in event_url.lower()
                if is_perma:
                    image_url = f"https://sportstreaming.net/assets/img/live/perma/live{perma_count}.png"
                    perma_count += 1
                else:
                    # Estrai il numero dall'URL per i canali standard (es. live-3 -> 3)
                    match = re.search(r'live-(\d+)', event_url)
                    if match:
                        live_number = match.group(1)
                        image_url = f"https://sportstreaming.net/assets/img/live/standard/live{live_number}.png"
                    else:
                        image_url = "https://sportstreaming.net/assets/img/live/standard/live1.png"  # Fallback

                tvg_name_prefix = f"{event_time} " if event_time else ""
                tvg_name_final = f"{event_title} | {league_info} | {tvg_name_prefix}".strip()
                if not tvg_name_final: # Fallback se il titolo è vuoto
                    tvg_name_final = "Eventi Live"

                # Codifica gli header per l'URL
                encoded_ua = quote_plus(headers["User-Agent"])
                encoded_referer = quote_plus(headers["Referer"])
                encoded_origin = quote_plus(headers["Origin"])

                # Costruisci l'URL finale con il proxy e gli header
                # stream_url qui è l'URL originale dello stream (es. https://xuione.sportstreaming.net/...)
                final_stream_url = f"{MFP_IP.rstrip('/')}/proxy/hls/manifest.m3u8?api_password={MFP_PASSWORD}&d={stream_url}&h_user-agent={encoded_ua}&h_referer={encoded_referer}&h_origin={encoded_origin}"

                group_title_text = "Sport" if is_perma else "Eventi Live"

                f.write(f"#EXTINF:-1 tvg-name=\"{tvg_name_final} (SPS)\"group-title=\"{group_title_text}\" tvg-logo=\"{image_url}\",{tvg_name_final} (SPS)\n")
                f.write(f"{final_stream_url}\n")
                f.write("\n") # Aggiungi una riga vuota dopo ogni canale


        print(f"File M3U8 aggiornato con successo: {file_path}")

    # Esegui lo script
    if __name__ == "__main__":
        current_date_dd_mm = datetime.now().strftime("%d/%m")
        print(f"Recupero eventi per il giorno: {current_date_dd_mm}")

        event_pages = find_event_pages()
        if not event_pages:
            print("Nessuna pagina evento trovata.")
        else:
            video_streams = []
            for event_url in event_pages:
                # print(f"Analizzo: {event_url}") # Rimosso per output più pulito, riattivare se necessario
                stream_url, event_date_str, event_time, event_title, league_info = get_event_details(event_url)
                
                if stream_url:
                    is_perma = "perma" in event_url.lower()
                    # Modifica: Includi solo se NON è perma E la data corrisponde
                    if not is_perma and (event_date_str == current_date_dd_mm):
                        print(f"Includo: {event_title} (URL: {event_url}, Data evento: {event_date_str})")
                        video_streams.append((event_url, stream_url, event_time, event_title, league_info))
                    elif is_perma:
                        print(f"Scarto canale perma: {event_title} (URL: {event_url})")
                    # else: # Evento non perma ma di un altro giorno
                        # print(f"Scarto evento (data non corrispondente): {event_title} (Data evento: {event_date_str}, Richiesta: {current_date_dd_mm})")
                else:
                    print(f"Nessun flusso trovato per {event_url}")

            if video_streams:
                update_m3u_file(video_streams)
            else:
                print("Nessun flusso video trovato in tutte le pagine evento.")

# Funzione per il quarto script (schedule_extractor.py)
def schedule_extractor():
    # Codice del quarto script qui
    # Aggiungi il codice del tuo script "schedule_extractor.py" in questa funzione.
    print("Eseguendo lo schedule_extractor.py...")
    # Il codice che avevi nello script "schedule_extractor.py" va qui, senza modifiche.
    from playwright.sync_api import sync_playwright
    import os
    import json
    from datetime import datetime
    import re
    from bs4 import BeautifulSoup
    from dotenv import load_dotenv
    
    # Carica le variabili d'ambiente dal file .env
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
    
                # Cerca la riga dei canali successiva
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
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator_world.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it', 'uk', 'tnt', 'usa', 'tennis channel', 'tennis stream', 'la']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events: # Original loop for events
                    # Filtra gli eventi in base all'orario specificato (00:00 - 04:00)
                    event_time_str = event_info.get("time", "00:00") # Prende l'orario dell'evento, default a "00:00" se mancante
                    try:
                        event_actual_time = datetime.strptime(event_time_str, "%H:%M").time()
                        
                        # Definisci gli orari limite per il filtro
                        filter_start_time = datetime.strptime("00:00", "%H:%M").time()
                        filter_end_time = datetime.strptime("04:00", "%H:%M").time()

                        # Escludi eventi se l'orario Ã¨ compreso tra 00:00 e 04:00 inclusi
                        if filter_start_time <= event_actual_time <= filter_end_time:
                            continue # Salta questo evento e passa al successivo
                    except ValueError:
                        print(f"[!] Orario evento non valido '{event_time_str}' per l'evento '{event_info.get('event', 'Sconosciuto')}' durante il caricamento JSON. Evento saltato.")
                        continue

                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
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
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
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
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
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
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
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
    
    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso
        
        # Percorso del file XML di output
        output_xml_path = "eventi.xml"
        
        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)

# Funzione per il quinto script (epg_eventi_generator.py)
def epg_eventi_generator():
    # Codice del quinto script qui
    # Aggiungi il codice del tuo script "epg_eventi_generator.py" in questa funzione.
    print("Eseguendo l'epg_eventi_generator.py...")
    # Il codice che avevi nello script "epg_eventi_generator.py" va qui, senza modifiche.
    import os
    import re
    import json
    from datetime import datetime, timedelta
    
    # Funzione di utilitÃ  per pulire il testo (rimuovere tag HTML span)
    def clean_text(text):
        return re.sub(r'</?span.*?>', '', str(text))
    
    # Funzione di utilitÃ  per pulire il Channel ID (rimuovere spazi e caratteri speciali)
    def clean_channel_id(text):
        """Rimuove caratteri speciali e spazi dal channel ID lasciando tutto attaccato"""
        # Rimuovi prima i tag HTML
        text = clean_text(text)
        # Rimuovi tutti gli spazi
        text = re.sub(r'\s+', '', text)
        # Mantieni solo caratteri alfanumerici (rimuovi tutto il resto)
        text = re.sub(r'[^a-zA-Z0-9]', '', text)
        # Assicurati che non sia vuoto
        if not text:
            text = "unknownchannel"
        return text
    
    # --- SCRIPT 5: epg_eventi_xml_generator (genera eventi.xml) ---
    def load_json_for_epg(json_file_path):
        """Carica e filtra i dati JSON per la generazione EPG"""
        if not os.path.exists(json_file_path):
            print(f"[!] File JSON non trovato per EPG: {json_file_path}")
            return {}
        
        try:
            with open(json_file_path, "r", encoding="utf-8") as file:
                json_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"[!] Errore nel parsing del file JSON: {e}")
            return {}
        except Exception as e:
            print(f"[!] Errore nell'apertura del file JSON: {e}")
            return {}
            
        # Lista delle parole chiave per canali italiani
        keywords = ['italy', 'rai', 'italia', 'it']
        
        filtered_data = {}
        for date, categories in json_data.items():
            filtered_categories = {}
            for category, events in categories.items():
                filtered_events = []
                for event_info in events:
                    filtered_channels = []
                    # Utilizza .get("channels", []) per gestire casi in cui "channels" potrebbe mancare
                    for channel in event_info.get("channels", []): 
                        channel_name = clean_text(channel.get("channel_name", "")) # Usa .get per sicurezza
                        
                        # Filtra per canali italiani - solo parole intere
                        channel_words = channel_name.lower().split()
                        if any(word in keywords for word in channel_words):
                            filtered_channels.append(channel)
                    
                    if filtered_channels:
                        # Assicura che event_info sia un dizionario prima dello unpacking
                        if isinstance(event_info, dict):
                            filtered_events.append({**event_info, "channels": filtered_channels})
                        else:
                            # Logga un avviso se il formato dell'evento non Ã¨ quello atteso
                            print(f"[!] Formato evento non valido durante il filtraggio per EPG: {event_info}")
                
                if filtered_events:
                    filtered_categories[category] = filtered_events
            
            if filtered_categories:
                filtered_data[date] = filtered_categories
        
        return filtered_data
    
    def generate_epg_xml(json_data):
        """Genera il contenuto XML EPG dai dati JSON filtrati"""
        epg_content = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
        
        italian_offset = timedelta(hours=2)
        italian_offset_str = "+0200" 
    
        current_datetime_utc = datetime.utcnow()
        current_datetime_local = current_datetime_utc + italian_offset
    
        # Tiene traccia degli ID dei canali per cui Ã¨ giÃ  stato scritto il tag <channel>
        channel_ids_processed_for_channel_tag = set() 
    
        for date_key, categories in json_data.items():
            # Dizionario per memorizzare l'ora di fine dell'ultimo evento per ciascun canale IN QUESTA DATA SPECIFICA
            # Viene resettato per ogni nuova data.
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
                # Ordina gli eventi per orario di inizio (UTC) per garantire la corretta logica "evento precedente"
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
    
                    # USA EVENT NAME COME CHANNEL ID - PULITO DA CARATTERI SPECIALI E SPAZI
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
    
                    # Verifica che ci siano canali disponibili
                    channels_list = event_info.get("channels", [])
                    if not channels_list:
                        print(f"[!] Nessun canale disponibile per l'evento '{event_name}'")
                        continue
    
                    for channel_data in channels_list:
                        if not isinstance(channel_data, dict):
                            print(f"[!] Formato canale non valido per l'evento '{event_name}': {channel_data}")
                            continue
    
                        channel_name_cleaned = clean_text(channel_data.get("channel_name", "Canale Sconosciuto"))
    
                        # Crea tag <channel> se non giÃ  processato
                        if channel_id not in channel_ids_processed_for_channel_tag:
                            epg_content += f'  <channel id="{channel_id}">\n'
                            epg_content += f'    <display-name>{event_name}</display-name>\n'
                            epg_content += f'  </channel>\n'
                            channel_ids_processed_for_channel_tag.add(channel_id)
                        
                        # --- LOGICA ANNUNCIO MODIFICATA ---
                        announcement_stop_local = event_datetime_local # L'annuncio termina quando inizia l'evento corrente
    
                        # Determina l'inizio dell'annuncio
                        if channel_id in last_event_end_time_per_channel_on_date:
                            # C'Ã¨ stato un evento precedente su questo canale in questa data
                            previous_event_end_time_local = last_event_end_time_per_channel_on_date[channel_id]
                            
                            # Assicurati che l'evento precedente termini prima che inizi quello corrente
                            if previous_event_end_time_local < event_datetime_local:
                                announcement_start_local = previous_event_end_time_local
                            else:
                                # Sovrapposizione o stesso orario di inizio, problematico.
                                # Fallback a 00:00 del giorno, o potresti saltare l'annuncio.
                                print(f"[!] Attenzione: L'evento '{event_name}' inizia prima o contemporaneamente alla fine dell'evento precedente su questo canale. Fallback per l'inizio dell'annuncio.")
                                announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time())
                        else:
                            # Primo evento per questo canale in questa data
                            announcement_start_local = datetime.combine(event_datetime_local.date(), datetime.min.time()) # 00:00 ora italiana
    
                        # Assicura che l'inizio dell'annuncio sia prima della fine
                        if announcement_start_local < announcement_stop_local:
                            announcement_title = f'Inizia  alle {event_datetime_local.strftime("%H:%M")}.' # Orario italiano
                            
                            epg_content += f'  <programme start="{announcement_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{announcement_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                            epg_content += f'    <title lang="it">{announcement_title}</title>\n'
                            epg_content += f'    <desc lang="it">{event_name}.</desc>\n' 
                            epg_content += f'    <category lang="it">Annuncio</category>\n'
                            epg_content += f'  </programme>\n'
                        elif announcement_start_local == announcement_stop_local:
                            print(f"[INFO] Annuncio di durata zero saltato per l'evento '{event_name}' sul canale '{channel_id}'.")
                        else: # announcement_start_local > announcement_stop_local
                            print(f"[!] Attenzione: L'orario di inizio calcolato per l'annuncio Ã¨ successivo all'orario di fine per l'evento '{event_name}' sul canale '{channel_id}'. Annuncio saltato.")
    
                        # --- EVENTO PRINCIPALE ---
                        main_event_start_local = event_datetime_local 
                        main_event_stop_local = event_datetime_local + timedelta(hours=2) # Durata fissa 2 ore
                        
                        epg_content += f'  <programme start="{main_event_start_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" stop="{main_event_stop_local.strftime("%Y%m%d%H%M%S")} {italian_offset_str}" channel="{channel_id}">\n'
                        epg_content += f'    <title lang="it">{event_desc}</title>\n'
                        epg_content += f'    <desc lang="it">{event_name}</desc>\n'
                        epg_content += f'    <category lang="it">{clean_text(category_name)}</category>\n'
                        epg_content += f'  </programme>\n'
    
                        # Aggiorna l'orario di fine dell'ultimo evento per questo canale in questa data
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
    
    def main_epg_generator(json_file_path, output_file_path="eventi.xml"):
        """Funzione principale per generare l'EPG XML"""
        print(f"[INFO] Inizio generazione EPG XML da: {json_file_path}")
        
        # Carica e filtra i dati JSON
        json_data = load_json_for_epg(json_file_path)
        
        if not json_data:
            print("[!] Nessun dato valido trovato nel file JSON.")
            return False
        
        print(f"[INFO] Dati caricati per {len(json_data)} date")
        
        # Genera il contenuto XML EPG
        epg_content = generate_epg_xml(json_data)
        
        # Salva il file XML
        success = save_epg_xml(epg_content, output_file_path)
        
        if success:
            print(f"[✓] Generazione EPG XML completata con successo!")
            return True
        else:
            print(f"[!] Errore durante la generazione EPG XML.")
            return False
    
    # Esempio di utilizzo
    if __name__ == "__main__":
        # Percorso del file JSON di input
        input_json_path = "daddyliveSchedule.json"  # Modifica con il tuo percorso
        
        # Percorso del file XML di output
        output_xml_path = "eventi.xml"
        
        # Esegui la generazione EPG
        main_epg_generator(input_json_path, output_xml_path)
        
# Funzione per il sesto script (italy_channels.py)
def italy_channels():
    print("Eseguendo il italy_channels.py...")

    import requests
    import re
    import os
    import xml.etree.ElementTree as ET
    from dotenv import load_dotenv
    import urllib.parse # Aggiunto per urlencode e quote
    import json         # Aggiunto per json.JSONDecodeError
    from bs4 import BeautifulSoup # Aggiunto per il parsing HTML

    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    LINK_SS = os.getenv("LINK_SKYSTREAMING", "https://skystreaming.yoga").strip()
    LINK_DADDY = os.getenv("LINK_DADDY", "https://daddylive.dad").strip()
    MFP_IP = os.getenv("IPMFP", "").strip()
    MFP_PASSWORD = os.getenv("PASSMFP", "").strip()
    EPG_FILE = "epg.xml"
    LOGOS_FILE = "logos.txt"
    OUTPUT_FILE = "channels_italy.m3u8"
    DEFAULT_TVG_ICON = ""
    HTTP_TIMEOUT = 20  # Timeout per le richieste HTTP in secondi

    # Crea una sessione requests per riutilizzare connessioni e gestire cookies
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

    # --- Funzioni per risolvere gli stream Daddylive ---
    def get_stream_from_channel_id(channel_id):
        # LINK_DADDY è una variabile globale
        # italy_channels usa /embed/stream-{id}.php per i canali Daddylive dalla pagina HTML
        raw_php_url = f"{LINK_DADDY.rstrip('/')}/embed/stream-{channel_id}.php"
        
        if MFP_IP:
            encoded_php_url = urllib.parse.quote(raw_php_url, safe='')
            return f"{MFP_IP.rstrip('/')}/extractor/video?host=DLHD&api_password={MFP_PASSWORD}&redirect_stream=true&d={encoded_php_url}"
        else:
            print(f"[!] MFP_IP non impostato. Impossibile generare l'URL extractor per il canale Daddylive {channel_id}.")
            return None
    # --- Fine funzioni Daddylive ---

    def fetch_channels_from_daddylive_page(page_url, base_daddy_url):
        print(f"Tentativo di fetch dei canali da: {page_url}")
        channels = []
        seen_daddy_channel_ids = set() # Set per tracciare i channel_id già visti da Daddylive
        try:
            response = session.get(page_url, timeout=HTTP_TIMEOUT, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # --- INIZIO LOGICA DI PARSING E FILTRAGGIO SPECIFICA PER DADDYLIVE 24-7 CHANNELS ---

            # Marcatori che suggeriscono un canale NON italiano (per evitare falsi positivi)
            non_italian_markers = [
                " (de)", " (fr)", " (es)", " (uk)", " (us)", " (pt)", " (gr)", " (nl)", " (tr)", " (ru)",
                " deutsch", " france", " español", " arabic", " greek", " turkish", " russian", " albania",
                " portugal" # Aggiunto basandomi sull'esempio fornito
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
                
                # Estrai l'ID del canale dall'href, es. /stream/stream-717.php -> 717
                channel_id_match = re.search(r'/stream/stream-(\d+)\.php', href)

                if channel_id_match and channel_name_raw:
                    channel_id = channel_id_match.group(1)
                    lower_channel_name = channel_name_raw.lower()

                    if channel_id in seen_daddy_channel_ids:
                        print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché l'ID è già stato processato.")
                        continue # Passa al prossimo item

                    # Filtro primario: deve contenere "italy"
                    if "italy" in lower_channel_name:
                        is_confirmed_non_italian_by_marker = False
                        for marker in non_italian_markers:
                            if marker in lower_channel_name:
                                is_confirmed_non_italian_by_marker = True
                                print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché, pur contenendo 'italy', ha anche un marcatore non italiano: '{marker}'")
                                break
                        
                        if not is_confirmed_non_italian_by_marker:
                            seen_daddy_channel_ids.add(channel_id) # Aggiungi l'ID al set prima di tentare la risoluzione
                            print(f"Trovato canale potenzialmente ITALIANO (Daddylive HTML): {channel_name_raw}, ID: {channel_id}. Tentativo di risoluzione stream...")
                            stream_url = get_stream_from_channel_id(channel_id)
                            if stream_url:
                                channels.append((channel_name_raw, stream_url))
                                print(f"Risolto e aggiunto stream per {channel_name_raw}: {stream_url}")
                            else:
                                print(f"Impossibile risolvere lo stream per {channel_name_raw} (ID: {channel_id})")
                    # else:
                        # Questo blocco è commentato per non intasare i log con canali non italiani
                        # Non stampiamo nulla per i canali che non contengono "italy" per non intasare il log
                        # print(f"Skipping Daddylive channel '{channel_name_raw}' (ID: {channel_id}) perché non contiene 'italy' nel nome.")
            # --- FINE LOGICA DI PARSING E FILTRAGGIO ---

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
                    raw_channel_url = ch['url']
                    channel_name = ch['name']
                    tvg_name_cleaned = re.sub(r"\s*\(.*?\)", "", ch["name"])

                    # I canali Daddylive (marcati con "(D)") hanno già l'URL formattato da get_stream_from_channel_id
                    # Altri canali (Vavoo, manuali) necessitano del wrapper proxy/hls se MFP_IP è impostato
                    if MFP_IP and not channel_name.upper().endswith(" (D)"):
                        # Canale Vavoo o manuale, applica il formato proxy/hls
                        final_url_to_write = f"{MFP_IP.rstrip('/')}/proxy/hls/manifest.m3u8?api_password={MFP_PASSWORD}&d={raw_channel_url}"
                    else:
                        # Canale Daddylive (URL già formattato o None) o MFP_IP non impostato (usa URL grezzo)
                        final_url_to_write = raw_channel_url

                    if final_url_to_write: # Scrivi solo se l'URL è valido
                        f.write(f'#EXTINF:-1 tvg-id="{ch.get("tvg_id", "")}" tvg-name="{tvg_name_cleaned}" tvg-logo="{ch.get("logo", DEFAULT_TVG_ICON)}" group-title="{category}",{ch["name"]}\n')
                        f.write(f"{final_url_to_write}\n\n")
                    else:
                        print(f"Skipping channel {channel_name} due to missing stream URL after processing.")


    def main():
        epg_root = fetch_epg(EPG_FILE)
        if epg_root is None:
            print("Impossibile recuperare il file EPG, procedura interrotta.")
            return
        logos_dict = fetch_logos(LOGOS_FILE)
        channel_id_map = create_channel_id_map(epg_root)
        
        all_fetched_channels = [] # Conterrà tuple (nome_canale, url_stream)

        # 1. Canali da sorgenti JSON (Vavoo)
        print("\n--- Fetching canali da sorgenti Vavoo (JSON) ---")
        for base_vavoo_url in BASE_URLS:
            json_channels_data = fetch_channels(base_vavoo_url)
            all_fetched_channels.extend(filter_italian_channels(json_channels_data, base_vavoo_url))

        # 2. Canali dalla pagina HTML di Daddylive
        print("\n--- Fetching canali da Daddylive (HTML) ---")
        daddylive_247_page_url = f"{LINK_DADDY.rstrip('/')}/24-7-channels.php"
        scraped_daddylive_channels = fetch_channels_from_daddylive_page(daddylive_247_page_url, LINK_DADDY)

        processed_scraped_channels = []
        seen_scraped_names = {}
        # Rinominato seen_scraped_names a seen_daddy_transformed_base_names per chiarezza
        seen_daddy_transformed_base_names = {}
        for raw_name, stream_url in scraped_daddylive_channels:
            # 1. Pulizia iniziale generica del nome grezzo
            name_after_initial_clean = clean_channel_name(raw_name)

            # 2. Trasformazioni specifiche per Daddylive:
            #    - Rimuovi "italy" (case insensitive)
            #    - Converti in maiuscolo
            # Questo sarà il nome base per la gestione dei duplicati Daddylive
            base_daddy_name = re.sub(r'italy', '', name_after_initial_clean, flags=re.IGNORECASE).strip()
            base_daddy_name = re.sub(r'\s+', ' ', base_daddy_name).strip() # Rimuovi spazi doppi
            base_daddy_name = base_daddy_name.upper()
            
            # Rinominare i canali Sky Calcio e Sky Calcio 7 specifici di Daddylive
            # Questo avviene DOPO la pulizia iniziale e l'uppercase,
            # e PRIMA della gestione dei duplicati e dell'aggiunta di "(D)"
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


            # Gestione skip DAZN (usa il nome base trasformato per il check)
            # clean_channel_name potrebbe già aver trasformato "dazn 1" in "DAZN2"
            if base_daddy_name == "DAZN" or base_daddy_name == "DAZN2":
                print(f"Skipping canale Daddylive (HTML) a causa della regola DAZN: {raw_name} (base trasformato: {base_daddy_name})")
                continue
            
            # 3. Gestione duplicati basata sul nome base trasformato di Daddylive
            count = seen_daddy_transformed_base_names.get(base_daddy_name, 0) + 1
            seen_daddy_transformed_base_names[base_daddy_name] = count
            
            # 4. Costruzione del nome finale per Daddylive
            final_name = base_daddy_name
            if count > 1:
                final_name = f"{base_daddy_name} ({count})" # Es. NOME CANALE (2)
            final_name = f"{final_name} (D)" # Es. NOME CANALE (D) o NOME CANALE (2) (D)
            
            processed_scraped_channels.append((final_name, stream_url))

        all_fetched_channels.extend(processed_scraped_channels)

        # 3. Canali manuali
        manual_channels_data = get_manual_channels()

        # Organizzazione di tutti i canali raccolti
        print("\n--- Organizzazione canali ---")
        organized_channels = {category: [] for category in CATEGORY_KEYWORDS.keys()}

        # Processa canali da Vavoo e Daddylive HTML (formato: (nome, url))
        for name, url in all_fetched_channels:
            # 'name' è il nome finale che verrà visualizzato, 
            # es. "CANALE SPORT (D) (2)" o "CANALE NEWS (3)" (da Vavoo)
            category = classify_channel(name)

            # Crea un nome base per il lookup di EPG e Logo:
            name_for_lookup = name
            # Rimuovi il suffisso (D) specifico di Daddylive, se presente
            if name_for_lookup.upper().endswith(" (D)"): # Controllo case-insensitive per robustezza
                # Rimuove l'ultima occorrenza di " (D)" (case insensitive)
                match_d_suffix = re.search(r'\s*\([Dd]\)$', name_for_lookup)
                if match_d_suffix:
                    name_for_lookup = name_for_lookup[:match_d_suffix.start()]
            
            # Rimuovi suffissi numerici per duplicati, es. (2), (3)...
            name_for_lookup = re.sub(r'\s*\(\d+\)$', '', name_for_lookup).strip()
            # A questo punto, name_for_lookup dovrebbe essere il nome del canale "pulito" 
            # es. "CANALE SPORT" o "CANALE NEWS" (già in maiuscolo se da Daddylive)

            # Logica per assegnazione logo
            final_logo_url = DEFAULT_TVG_ICON # Inizializza con il logo di default
            sky_sport_daddy_logo = "https://raw.githubusercontent.com/tv-logo/tv-logos/refs/heads/main/countries/italy/hd/sky-sport-hd-it.png"

            # Controlla se il canale è uno dei canali Daddylive SKY SPORT 251-256
            # name_for_lookup è il nome base pulito (es. "SKY SPORT 251")
            # name è il nome completo con suffisso (es. "SKY SPORT 251 (D)")
            if name.upper().endswith(" (D)"): # Verifica se è un canale Daddylive
                if re.match(r"SKY SPORT (25[1-6])$", name_for_lookup.upper()):
                    # È un canale Daddylive SKY SPORT 251-256
                    final_logo_url = sky_sport_daddy_logo
                    print(f"Logo specifico '{final_logo_url}' assegnato a Daddylive channel '{name}' (lookup name: '{name_for_lookup}')")
                else:
                    # È un canale Daddylive, ma non uno dei SKY SPORT 251-256 target, usa il lookup normale
                    final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)
            else:
                # Non è un canale Daddylive (es. Vavoo), usa il lookup normale
                final_logo_url = logos_dict.get(name_for_lookup.lower(), DEFAULT_TVG_ICON)

            organized_channels.setdefault(category, []).append({
                "name": name, # Nome completo da visualizzare
                "url": url,
                "tvg_id": channel_id_map.get(normalize_channel_name(name_for_lookup), ""), # Usa il nome pulito per tvg-id
                "logo": final_logo_url # Usa il logo determinato dalla logica sopra
            })

        # Processa canali manuali (formato: dict)
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

# Funzione per il settimo script (world_channels_generator.py)
def world_channels_generator():
    # Codice del settimo script qui
    # Aggiungi il codice del tuo script "world_channels_generator.py" in questa funzione.
    print("Eseguendo il world_channels_generator.py...")
    # Il codice che avevi nello script "world_channels_generator.py" va qui, senza modifiche.
    import requests
    import re
    import os
    from collections import defaultdict
    from dotenv import load_dotenv
    
    # Carica le variabili d'ambiente dal file .env
    load_dotenv()

    MFP_IP = os.getenv("IPMFP", "").strip()
    MFP_PASSWORD = os.getenv("PASSMFP", "").strip()
    OUTPUT_FILE = "world.m3u8"
    BASE_URLS = [
        "https://vavoo.to"
    ]
    
    # Scarica la lista dei canali
    def fetch_channels(base_url):
        try:
            response = requests.get(f"{base_url}/channels", timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore durante il download da {base_url}: {e}")
            return []
    
    # Pulisce il nome del canale
    def clean_channel_name(name):
        return re.sub(r"\s*(\|E|\|H|\(6\)|\(7\)|\.c|\.s)", "", name).strip()
    
    # Salva il file M3U8 con i canali ordinati alfabeticamente per categoria
    def save_m3u8(channels):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
    
        # Raggruppa i canali per nazione (group-title)
        grouped_channels = defaultdict(list)
        for name, url, country in channels:
            grouped_channels[country].append((name, url))
    
        # Ordina le categorie alfabeticamente e i canali dentro ogni categoria
        sorted_categories = sorted(grouped_channels.keys())
    
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write('#EXTM3U\n\n')
    
            for country in sorted_categories:
                # Ordina i canali in ordine alfabetico dentro la categoria
                grouped_channels[country].sort(key=lambda x: x[0].lower())
    
                for name, url in grouped_channels[country]:
                    final_url_to_write = url
                    if MFP_IP:
                        final_url_to_write = f"{MFP_IP.rstrip('/')}/proxy/hls/manifest.m3u8?api_password={MFP_PASSWORD}&d={final_url}"
                    else:
                        # Se MFP_IP non è settato, usa l'URL originale
                        final_url_to_write = url
                    f.write(f'#EXTINF:-1 tvg-name="{name}" group-title="{country}", {name}\n')
                    f.write(f"{final_url_to_write}\n\n")
    
    # Funzione principale
    def main():
        all_channels = []
        for url in BASE_URLS:
            channels = fetch_channels(url)
            for ch in channels:
                clean_name = clean_channel_name(ch["name"])
                country = ch.get("country", "Unknown")  # Estrai la nazione del canale, default Ã¨ "Unknown"
                all_channels.append((clean_name, f"{url}/play/{ch['id']}/index.m3u8", country))
    
        save_m3u8(all_channels)
        print(f"File {OUTPUT_FILE} creato con successo!")
    
    if __name__ == "__main__":
        main()

def removerworld():
    import os
    
    # Lista dei file da eliminare
    files_to_delete = ["world.m3u8", "channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
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
    
    # Lista dei file da eliminare
    files_to_delete = ["channels_italy.m3u8", "eventi.m3u8", "eventi.xml"]
    
    for filename in files_to_delete:
        if os.path.exists(filename):
            try:
                os.remove(filename)
                print(f"File eliminato: {filename}")
            except Exception as e:
                print(f"Errore durante l'eliminazione di {filename}: {e}")
        else:
            print(f"File non trovato: {filename}")

# Funzione principale che esegue tutti gli script
def main():
    try:
        schedule_success = schedule_extractor()
    except Exception as e:
        print(f"Errore durante l'esecuzione di schedule_extractor: {e}")
        
    try:
        eventi_sps()
    except Exception as e:
        print(f"Errore durante l'esecuzione di eventi_sps: {e}")
        return


    eventi_en = os.getenv("EVENTI_EN", "no").strip().lower()
    world_flag = os.getenv("WORLD", "si").strip().lower()

    # EPG Eventi
    try:
        if eventi_en == "si":
            epg_eventi_generator_world()
        else:
            epg_eventi_generator()
    except Exception as e:
        print(f"Errore durante la generazione EPG eventi: {e}")
        return

    # Eventi M3U8
    try:
        if eventi_en == "si":
            eventi_m3u8_generator_world()
        else:
            eventi_m3u8_generator()
    except Exception as e:
        print(f"Errore durante la generazione eventi.m3u8: {e}")
        return

    # EPG Merger
    try:
        epg_merger()
    except Exception as e:
        print(f"Errore durante l'esecuzione di epg_merger: {e}")
        return

    # Canali Italia
    try:
        italy_channels()
    except Exception as e:
        print(f"Errore durante l'esecuzione di italy_channels: {e}")
        return

    # Canali World e Merge finale
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
