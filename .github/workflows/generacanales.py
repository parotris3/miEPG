import requests

def obtener_datos_canal(cas_id, url="https://raw.githubusercontent.com/parotris3/Mfeed/refs/heads/main/ott.csv"):
    """Obtiene el nombre y el logo de un canal a partir de su CasId desde un CSV en línea.

    Args:
        cas_id: El CasId del canal a buscar.
        url: La URL del archivo CSV.

    Returns:
        Una tupla con el nombre y la URL del logo, o (None, None) si no se encuentra el canal.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza una excepción si hay un error HTTP

        lines = response.text.strip().split('\n')
        header = lines[0].split(',')
        
        # Encuentra los índices de las columnas relevantes (maneja posibles espacios extra)
        casid_index = header.index('CasId')
        nombre_index = header.index('Nombre')
        logo_index = header.index('Logo')


        for line in lines[1:]:
            values = line.split(',')
            if len(values) > casid_index and values[casid_index].strip() == str(cas_id):
                nombre = values[nombre_index].strip()
                logo = values[logo_index].strip()
                return nombre, logo
        return None, None  # No se encontró el CasId

    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos desde la URL: {e}")
        return None, None
    except (ValueError, IndexError) as e:
        print(f"Error al procesar el archivo CSV: {e}")
        return None, None




def crear_archivo_canales(nombre_archivo="canales.txt"):
    """Crea el archivo canales.txt con el contenido especificado,
       reemplazando los valores de los popups.
    """

    contenido_base = """La 1 HD,La 1 HD
La 2,La 2
Antena 3 HD,Antena 3
Cuatro HD,Cuatro
Telecinco HD,Telecinco
La Sexta HD,La Sexta
TVG,TVG
TVG2,TVG 2
TPA7 Asturias,TPA7 Asturias
TPA8 Asturias,TPA8 Asturias
M+ Vamos HD,M+ Vamos
M+ Ellas Vamos HD,M+ Ellas Vamos
Movistar Plus+ HD,Movistar Plus+
Movistar Plus+ 2 HD,Movistar Plus+ 2
M+ Originales HD,M+ Originales
M+ Documentales HD,M+ Documentales
M+ Estrenos HD,M+ Estrenos HD
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
Love TV Trailers,Trailers
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
acontra+,acontra+
Clásicos atresplayer,Clásicos atresplayer
Multicine atresplayer,Multicine atresplayer
Comedia atresplayer,Comedia atresplayer
Inquietos atresplayer,Inquietos atresplayer
ATRESplayer PREMIUM,ATRESplayer PREMIUM
TCM HD,TCM
Canal Hollywood HD,Canal Hollywood
M+ Hits HD,M+ Hits HD
STAR Channel HD,STAR Channel
Max Avances,Max Avances
AXN HD,AXN
AXN Movies HD,AXN Movies
Warner TV HD,Warner TV
SkyShowtime,SkyShowtime
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
MTV España,MTV España
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
NOW 80s,NOW 80s
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
Clan,Clan
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
GOL PLAY,GOL PLAY
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
M+ LaLiga TV HD,M+ LALIGA TV
M+ LaLiga TV UHD,M+ LALIGA TV UHD
M+ LaLiga TV 2 HD,M+ LALIGA TV 2
M+ LaLiga TV 3 HD,M+ LALIGA TV 3
M+ Copa del Rey,M+ Copa del Rey
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
M+ Liga de Campeones 2 HDR,M+ Liga de Campeones 2 HDR
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
