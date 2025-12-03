import requests
import csv  # Importa el módulo csv
import io   # Necesario para tratar el texto como un archivo

def obtener_datos_canal(cas_id, url="https://raw.githubusercontent.com/parotris3/Mfeed/refs/heads/main/difusion.csv"):
    """Obtiene el nombre y el logo de un canal a partir de su CasId desde un CSV en línea usando el módulo csv.

    Args:
        cas_id: El CasId del canal a buscar.
        url: La URL del archivo CSV.

    Returns:
        Una tupla con el nombre y la URL del logo, o (None, None) si no se encuentra el canal.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        try:
            decoded_text = response.content.decode('utf-8-sig')
        except UnicodeDecodeError:
            print("Advertencia: No se pudo decodificar como utf-8-sig, intentando con la detección automática.")
            decoded_text = response.text

        # Usa io.StringIO para que el módulo csv pueda leer el texto como si fuera un archivo
        csv_file = io.StringIO(decoded_text)

        # Crea un lector csv. Automáticamente maneja las comillas (quotechar='"')
        reader = csv.reader(csv_file, delimiter=',', quotechar='"')

        # Lee la cabecera
        try:
            header = next(reader) # Lee la primera fila (cabecera)
            print(f"DEBUG: Cabecera leída por csv.reader: {header}")
        except StopIteration:
            print("Error: Archivo CSV vacío.")
            return None, None

        # Encuentra los índices (los nombres en 'header' ya están limpios, sin comillas)
        try:
            casid_index = header.index('CasId')
            nombre_index = header.index('Nombre')
            logo_index = header.index('Logo')
        except ValueError as e:
            print(f"Error: Columna no encontrada en la cabecera. Cabecera={header}. Error: {e}")
            return None, None

        # Itera sobre las filas de datos restantes
        for row in reader:
            # 'row' es una lista de strings ya limpios (sin comillas)
            if len(row) > max(casid_index, nombre_index, logo_index):
                if row[casid_index] == str(cas_id): # Compara directamente
                    nombre = row[nombre_index]
                    logo = row[logo_index]
                    return nombre, logo
            else:
                print(f"Advertencia: Fila saltada por tener pocas columnas: {row}")

        return None, None  # No se encontró el CasId

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos desde la URL: {e}")
        return None, None
    except (ValueError, IndexError, csv.Error) as e: # Añade csv.Error a las excepciones
        print(f"Error al procesar el archivo CSV: {e}")
        return None, None
    except Exception as e:
        print(f"Error inesperado procesando el archivo CSV: {e}")
        return None, None



def crear_archivo_canales(nombre_archivo="canales.txt"):
    """Crea el archivo canales.txt con el contenido especificado,
       reemplazando los valores de los popups.
    """

    contenido_base = """La 1 HD,LA 1
La 2,LA 2
Antena 3 HD,Antena 3
Cuatro HD,Cuatro
Telecinco HD,Telecinco
La Sexta HD,La Sexta
TVG,TVG
TVG2,TVG 2
TPA7 Asturias,TPA7
TPA8 Asturias,TPA8
M+ Vamos HD,M+ Vamos
M+ Ellas Vamos HD,M+ Ellas V
Movistar Plus+ HD,Movistar Plus+
M+ Originales HD,M+ Originales
M+ Documentales HD,M+ Documentales
M+ Estrenos HD,M+ Estrenos
M+ Comedia HD,M+ Comedia
M+ Drama HD,M+ Drama
M+ Acción HD,M+ Acción
NOMBREPOPUP,NOMBREPOPUP,URLLOGOPOPUP
NOMBREPOP2,NOMBREPOP2,URLLOGOPOP2
M+ PopUp,M+ PopUp,URLLOGOPOPUP
M+ PopUp 2,M+ PopUp 2,URLLOGOPOP2
M+ Clásicos HD,M+ Clásicos
M+ Cine Español,M+ Cine Español
M+ Indie HD,M+ Indie
Love TV Trailers,Love TV Trailers
5f1ac8099c49f600076579b2,Pluto TV Cine Comedia
655b5d865812e80008843bd1,Pluto TV Cine Comedias Románticas
5f1ac9a2d3611d0007a844bb,Pluto TV Cine Romántico
5f1ac947dcd00d0007937c08,Pluto TV Cine Drama
61373bb45168fe000773eecd,Pluto TV Cine Clásico
5f1ac1f1b66c76000790ef27,Pluto TV Cine Estelar
5f1ac2591dd8880007bb7d6d,Pluto TV Cine Acción
6385e82900ab2e000768a058,Pluto TV Western
6304f530440dc90007f514d3,Poirot y Miss Marple
BOM Cine,Bom Cine
Somos,Somos
Cines Verdi TV,Cines Verdi TV
Cine Feel Good,Cine Feel Good
Acontra+,acontra+
Clásicos atresplayer,Clásicos atresplayer
Multicine atresplayer,Multicine atresplayer
Comedia atresplayer,Comedia atresplayer
Inquietos atresplayer,Inquietos atresplayer
ATRESplayer PREMIUM,ATRESplayer PREMIUM
TCM HD,TCM
Canal Hollywood HD,Canal Hollywood
M+ Hits HD,M+ Hits
STAR Channel HD,STAR Channel
HBO Max Avances,HBO Max Avances
AXN HD,AXN
AXN Movies HD,AXN Movies
Warner TV HD,Warner TV
SkyShowtime,SkyShowtime 1
AMC HD,AMC
AMC Break,AMC Break
AMC Crime,AMC Crime
SELEKT,SELEKT
Calle 13 HD,Calle 13
DARK,DARK
SyFy HD,SYFY
XTRM,XTRM
Cosmo HD,COSMO
Comedy Central HD,Comedy Central
La Resistencia 24H,La Resistencia 24H
Flooxer,Flooxer
Paramount Network,Paramount Network
Sundance TV,Sundance TV
DKISS,DKISS
MTV España,MTV
Ten,Ten
Be Mad,BE MAD
Atreseries,Atreseries
Neox,Neox
Nova,Nova
Energy,Energy
TRECE,TRECE
Divinity,Divinity
Factoría de Ficción,Factoría de Ficción
Mega,Mega
MTV 00s,MTV 00s
MTV Hits HD,MTV Hits
Sol Música,Sol Música
HIT TV,HIT TV
6076cd1df8576d0007c82193,VH1 Classics
Qello Concerts,Qello Concerts
61ea759737679900078ff559,MTV Party Music
60a26a056d55b30007918d5a,MTV Music Made in Spain
NOW 70s,NOW 70s
NOW 80's,NOW 80s
NOW Rock,NOW Rock
Mezzo,Mezzo
Mezzo Live HD,Mezzo Live
Classica HD,Classica
National Geographic HD,National Geographic
Nat Geo Wild HD,Nat Geo Wild
NatureTime,NatureTime
600ae6a78d801e0007117d21,Pluto TV Animales
64db2e0835425100080f2f5a,Pluto TV Diseño
ESBA330004121,Wild Earth
Odisea,Odisea
Historia,Historia
61cd7b49543066000713b620,Pluto TV Historia
Escapa TV,Escapa TV
BuenViaje,BuenViaje
De Viajes,RTVE De Viajes
60c343ad476ec00007c2ec1a,Pluto TV Viajes
622f42b831233300078658cc,Ciudadanos por el mundo
Viajes y Sabores,Viajes y Sabores,https://www.tivify.es/wp-content/uploads/2025/02/Viajes-y-Sabores-Logo-Web-300x300.png
Canal Cocina,Canal Cocina
5f1acdaa8ba90f0007d5e760,Pluto TV Cocina
Decasa,Decasa
DMAX,DMAX
60d356a534f63f000850cdd7,Top Gear
Discovery,Discovery
Caza y Pesca HD,Caza y Pesca
Iberalia TV,Iberalia TV
Clan,Clan TVE,https://raw.githubusercontent.com/davidmuma/picons_dobleM/master/icon/Clan.png
Boing,Boing
Baby TV,Baby TV
Squirrel TV,Squirrel TV
Disney Junior,Disney Junior
Enfamilia,Enfamilia
Nickelodeon HD,Nickelodeon
Nick JR,NICK JR
Dreamworks HD,Dreamworks
24 Horas,24 Horas
EuroNews,Euronews
Teledeporte,Teledeporte
GOL,GOL
Real Madrid TV,Real Madrid TV
Eurosport 1 HD,Eurosport 1
Eurosport 2,Eurosport 2
DAZN 1 HD,DAZN 1
DAZN 2 HD,DAZN 2
DAZN 3 HD,DAZN 3
DAZN 4 HD,DAZN 4
DAZN F1 HD,DAZN F1
DAZN LaLiga HD,DAZN LaLiga
DAZN LaLiga 2 HD,DAZN LaLiga 2
M+ LaLiga HD,M+ LALIGA
M+ LaLiga TV UHD,M+ LALIGA TV UHD
M+ LaLiga 2 HD,M+ LALIGA 2
M+ LaLiga 3 HD,M+ LALIGA 3
Primera Federación, Primera Federación
LaLiga TV Hypermotion HD,LALIGA TV HYPERMOTION
LaLiga TV Hypermotion 2,LALIGA TV HYPERMOTION 2
LaLiga TV Hypermotion 3,LALIGA TV HYPERMOTION 3
M+ Liga de Campeones HD,M+ Liga de Campeones
M+ Liga de Campeones 2 HD,M+ Liga de Campeones 2
M+ Liga de Campeones 3 HD,M+ Liga de Campeones 3
M+ Liga de Campeones 4,M+ Liga de Campeones 4
M+ Liga de Campeones 5,M+ Liga de Campeones 5
M+ Liga de Campeones 6,M+ Liga de Campeones 6
M+ Liga de Campeones 7,M+ Liga de Campeones 7
M+ Liga de Campeones 8,M+ Liga de Campeones 8
M+ Liga de Campeones 9,M+ Liga de Campeones 9
M+ Liga de Campeones 10,M+ Liga de Campeones 10
M+ Liga de Campeones 11,M+ Liga de Campeones 11
M+ Liga de Campeones 12,M+ Liga de Campeones 12
M+ Liga de Campeones 13,M+ Liga de Campeones 13
M+ Deportes HD,M+ Deportes
M+ Deportes 2 HD,M+ Deportes 2
M+ Deportes 3,M+ Deportes 3
M+ Deportes 4,M+ Deportes 4
M+ Deportes 5,M+ Deportes 5
M+ Deportes 6,M+ Deportes 6
M+ Deportes 7,M+ Deportes 7
M+ Deportes 8,M+ Deportes 8
M+ Golf HD,M+ Golf
M+ Golf 2 HD,M+ Golf 2
PT | DAZN 1,DAZN 1 Portugal
PT | DAZN 2,DAZN 2 Portugal
PT | DAZN 3,DAZN 3 Portugal
PT | DAZN 4,DAZN 4 Portugal
PT | DAZN 5,DAZN 5 Portugal
PT | DAZN 6,DAZN 6 Portugal
65786abdb3801200084c593a,Homeful
65786d29dfed030008ce2fa7,MTV Rock
668677f7fd9eb200087b673a,MTV Biggest Pop
BBC Drama,BBC Drama
BBC Food,BBC Food
BBC History,BBC History
BBC Top Gear,BBC Top Gear
Runtime Familia,Runtime Familia,https://img.static-ottera.com/prod/run/linear_channel/logo/runtime_familia_16x9_1.jpg
Runtime Comedia,Runtime Comedia,https://img.static-ottera.com/prod/run/linear_channel/logo/runtime_comedia_16x9.jpg
Runtime Romance,Runtime Romance,https://img.static-ottera.com/prod/run/linear_channel/logo/runtime_romance_16x9.jpg
MTV Live,MTV Live
M+ Liga de Campeones HDR,M+ Liga de Campeones HDR
M+ Liga de Campeones 2 HDR,M+ Liga de Campeones2 HDR
Garage TV,El Garage TV
Veo7,Veo7
VinTV,VinTV
El Toro TV,El Toro TV
M+ LaLiga HDR,M+ LALIGA HDR
AMC+ Connect,AMC+ Connect
BBC Earth,BBC Earth
BBC Lifestyle,BBC Lifestyle
BBC Series,BBC Series
M+ Vamos 2,M+ Vamos 2
Anime Visión,Anime Visión
Anime Visión Classics,Anime Visión Classics
100% Navidad (Rakuten TV),100% Navidad
Canal FlixOlé 1, Canal FlixOlé 1
Canal FlixOlé 2, Canal FlixOlé 2
"""

    nombre_popup1, logo_popup1 = obtener_datos_canal(4955)
    nombre_popup2, logo_popup2 = obtener_datos_canal(5252)

    if nombre_popup1 and logo_popup1:
        contenido_base = contenido_base.replace("NOMBREPOPUP", nombre_popup1)
        contenido_base = contenido_base.replace("URLLOGOPOPUP", logo_popup1)
    else:
        print("No se pudieron obtener los datos para el primer popup.")
        return  # Sale de la función si no se pueden obtener los datos

    if nombre_popup2 and logo_popup2:
        contenido_base = contenido_base.replace("NOMBREPOP2", nombre_popup2)
        contenido_base = contenido_base.replace("URLLOGOPOP2", logo_popup2)
    else:
        print("No se pudieron obtener los datos para el segundo popup.")
        return


    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido_base)
        print(f"Archivo '{nombre_archivo}' creado exitosamente.")
    except IOError as e:
        print(f"Error al escribir en el archivo: {e}")


if __name__ == "__main__":
    crear_archivo_canales()














