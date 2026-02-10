#!/bin/bash

set -euo pipefail

# Limpia líneas vacías
sed -i '/^ *$/d' epgs.txt
sed -i '/^ *$/d' canales.txt

rm -f EPG_temp*
: > EPG_temp1.xml   # channels finales
: > EPG_temp2.xml   # programmes finales

SEEN_FILE="seen_channels.txt"
: > "$SEEN_FILE"

while IFS= read -r epg
do
  [ -z "$epg" ] && continue

  extension="${epg##*.}"
  if [ "$extension" = "gz" ]; then
    echo "Descargando y descomprimiendo epg: $epg"
    wget -q -O EPG_temp00.xml.gz "$epg"
    gzip -d -f EPG_temp00.xml.gz
  else
    echo "Descargando epg: $epg"
    wget -q -O EPG_temp00.xml "$epg"
  fi

  while IFS=, read -r old new logo
  do
    [ -z "${old:-}" ] && continue
    [ -z "${new:-}" ] && new="$old"

    # Si ya lo capturamos en una EPG anterior, no duplicar
    if grep -Fxq "$old" "$SEEN_FILE"; then
      continue
    fi

    # Si en esta EPG no hay programmes para ese canal, saltar
    if ! grep -Fq "channel=\"${old}\"" EPG_temp00.xml; then
      continue
    fi

    echo "Usando 1ª coincidencia: $old -> $new"
    echo "$old" >> "$SEEN_FILE"

    # ---------- Construir <channel> final ----------
    # Extrae iconos del canal original (si existe el bloque <channel>)
    if grep -Fq "<channel id=\"${old}\">" EPG_temp00.xml; then
      sed -n "/<channel id=\"${old}\">/,/<\/channel>/p" EPG_temp00.xml > EPG_temp01.xml
      sed -i '/<icon src/!d' EPG_temp01.xml
    else
      : > EPG_temp01.xml
    fi

    if [ -n "${logo:-}" ]; then
      # Logo forzado desde canales.txt
      {
        echo "  <channel id=\"${new}\">"
        echo "    <display-name>${new}</display-name>"
        echo "    <icon src=\"${logo}\" />"
        echo "  </channel>"
      } >> EPG_temp1.xml
    else
      # Mantener el/los iconos encontrados en la EPG (si hay)
      {
        echo "  <channel id=\"${new}\">"
        echo "    <display-name>${new}</display-name>"
        cat EPG_temp01.xml
        echo "  </channel>"
      } >> EPG_temp1.xml
    fi

    # Quita duplicados exactos de líneas (por si repites canal/new en canales.txt)
    sed -i '$!N;/^\(.*\)\n\1$/!P;D' EPG_temp1.xml

    # ---------- Extraer programmes del canal (solo de esta EPG) ----------
    sed -n "/<programme[^>]*channel=\"${old}\"/,/<\/programme>/p" EPG_temp00.xml > EPG_temp02.xml
    sed -i '/<programme/s/">.*/"/g' EPG_temp02.xml
    sed -i "s# channel=\"${old}\"##g" EPG_temp02.xml
    sed -i "/<programme/a EPG_temp channel=\"${new}\">" EPG_temp02.xml
    sed -i ':a;N;$!ba;s/\nEPG_temp//g' EPG_temp02.xml

    cat EPG_temp02.xml >> EPG_temp2.xml

  done < canales.txt

done < epgs.txt

# ---------- Montar XML final ----------
date_stamp=$(date +"%d/%m/%Y %R")
{
  echo '<?xml version="1.0" encoding="UTF-8"?>'
  echo "<tv generator-info-name=\"miEPG $date_stamp\" generator-info-url=\"https://github.com/davidmuma/miEPG\">"
  cat EPG_temp1.xml
  cat EPG_temp2.xml
  echo '</tv>'
} > miEPG.xml

rm -f EPG_temp*
rm -f "$SEEN_FILE"
