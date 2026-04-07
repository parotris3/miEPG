#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import urllib.request
import gzip
import os
import re
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE FECHAS ---
now = datetime.now()
min_date = now - timedelta(days=7) # 7 días hacia atrás
max_date = now + timedelta(days=2) # 2 días hacia adelante

def parse_time(t_str):
    """Extrae la fecha del formato XMLTV (ej. 20240520143000 +0200)"""
    if not t_str: return now
    try:
        return datetime.strptime(t_str[:14], '%Y%m%d%H%M%S')
    except ValueError:
        return now

# --- 2. CARGAR HISTORIAL (miEPG.xml actual) ---
old_programmes = {}  # Diccionario: ID del canal -> Lista de programas
if os.path.exists('miEPG.xml'):
    print("Cargando historial de miEPG.xml existente...")
    try:
        tree = ET.parse('miEPG.xml')
        root = tree.getroot()
        for prog in root.findall('programme'):
            ch_id = prog.get('channel')
            start_t = parse_time(prog.get('start'))
            stop_t = parse_time(prog.get('stop'))
            
            # Conservar SOLO si entra en la ventana de tiempo [-7 días, +2 días]
            if stop_t >= min_date and start_t <= max_date:
                if ch_id not in old_programmes:
                    old_programmes[ch_id] = []
                old_programmes[ch_id].append(prog)
    except Exception as e:
        print(f"No se pudo cargar el historial (puede ser la primera ejecución): {e}")

# --- 3. CARGAR canales.txt ---
canales = []
with open('canales.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # Evitar líneas vacías
        if not line.strip(): continue
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 2:
            old_id, new_id = parts[0], parts[1]
            logo = parts[2] if len(parts) > 2 else None
            canales.append((old_id, new_id, logo))

# --- 4. DESCARGAR EPGs NUEVOS ---
epgs_urls = []
if os.path.exists('epgs.txt'):
    with open('epgs.txt', 'r', encoding='utf-8') as f:
        epgs_urls = [line.strip() for line in f if line.strip()]

new_trees = []
for url in epgs_urls:
    print(f"Descargando: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            if url.endswith('.gz'):
                data = gzip.decompress(response.read())
            else:
                data = response.read()
            # Parsear XML a memoria
            new_trees.append(ET.fromstring(data))
    except Exception as e:
        print(f"Error descargando {url}: {e}")

# --- 5. EXTRAER, FILTRAR Y FUSIONAR ---
final_channels = []
final_programmes = []
seen_old_ids = set()

for old_id, new_id, logo in canales:
    if old_id in seen_old_ids:
        continue
    
    # 5.1. Buscar el canal en los EPGs descargados (Búsqueda segura anti-comillas)
    channel_element = None
    source_root = None
    for root in new_trees:
        for ch in root.findall('channel'):
            if ch.get('id') == old_id:
                channel_element = ch
                source_root = root
                break
        if channel_element is not None:
            break
    
    # 5.2. Construir el bloque <channel>
    new_ch_element = ET.Element('channel', id=new_id)
    ET.SubElement(new_ch_element, 'display-name').text = new_id
    
    if logo:
        ET.SubElement(new_ch_element, 'icon', src=logo)
    elif channel_element is not None:
        icon = channel_element.find('icon')
        if icon is not None:
            new_ch_element.append(icon)
            
    final_channels.append(new_ch_element)
    seen_old_ids.add(old_id)

    # 5.3. Recopilar programas NUEVOS para este canal (Búsqueda segura)
    new_progs_for_channel = []
    if source_root is not None:
        for prog in source_root.findall('programme'):
            if prog.get('channel') == old_id:
                start_t = parse_time(prog.get('start'))
                stop_t = parse_time(prog.get('stop'))
                
                # Filtrar por fecha
                if stop_t >= min_date and start_t <= max_date:
                    prog.set('channel', new_id)
                    
                    # Limpiar descripción
                    desc = prog.find('desc')
                    if desc is not None and desc.text:
                        desc.text = re.sub(r'^\s*\([^)]*\)\s*', '', desc.text)
                    
                    new_progs_for_channel.append(prog)

    # 5.4. Lógica de Solapamientos (Nuevos vs Viejos)
    historical_progs = old_programmes.get(new_id, [])
    
    def is_overlap(p1, p2):
        s1, e1 = parse_time(p1.get('start')), parse_time(p1.get('stop'))
        s2, e2 = parse_time(p2.get('start')), parse_time(p2.get('stop'))
        return s1 < e2 and e1 > s2

    merged_progs = list(new_progs_for_channel)
    
    # Añadimos los programas del historial SOLO si no pisan a ningún programa nuevo
    for old_p in historical_progs:
        overlap = False
        for new_p in new_progs_for_channel:
            if is_overlap(old_p, new_p):
                overlap = True
                break
        if not overlap:
            merged_progs.append(old_p)
            
    final_programmes.extend(merged_progs)

# --- 6. GENERAR XML FINAL ---
print("Generando miEPG.xml final...")
date_stamp = datetime.now().strftime("%d/%m/%Y %H:%M")
tv = ET.Element('tv', {
    'generator-info-name': f"miEPG {date_stamp}",
    'generator-info-url': "https://github.com/davidmuma/miEPG"
})

for ch in final_channels:
    tv.append(ch)
for pr in final_programmes:
    tv.append(pr)

# Identar y guardar
tree = ET.ElementTree(tv)
ET.indent(tree, space="  ", level=0)
tree.write('miEPG.xml', encoding='UTF-8', xml_declaration=True)
print("¡Proceso completado con éxito!")
