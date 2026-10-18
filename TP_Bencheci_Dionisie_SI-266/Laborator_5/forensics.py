import re
import os
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    elif cap.startswith(b"\x89PNG"):
        return "png"
    elif cap.startswith(b"\xff\xd8"):
        return "jpeg"
    elif cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()

def extrage_strings(cale, lungime_min=4):
    with open(cale, "rb") as f:
        date = f.read()
    gasite = [m.decode("latin1") for m in re.findall(rb"[ -~]{" + str(lungime_min).encode() + rb",}", date)]
    return gasite

def dms_to_decimal(dms, ref):
    grade = float(dms[0])
    minute = float(dms[1])
    secunde = float(dms[2])
    zecimal = grade + (minute / 60.0) + (secunde / 3600.0)
    if ref in ["S", "W"]:
        zecimal = -zecimal
    return round(zecimal, 6)

def citeste_exif_gps(cale_poza):
    img = Image.open(cale_poza)
    exif = img._getexif() or {}
    
    print(f"\n[B3] Metadate EXIF pentru {cale_poza}:")
    gps_info = {}
    for id_tag, val in exif.items():
        nume_tag = TAGS.get(id_tag, id_tag)
        if nume_tag == "GPSInfo":
            for gps_id, gps_val in val.items():
                gps_info[GPSTAGS.get(gps_id, gps_id)] = gps_val
        else:
            print(f"  {nume_tag} = {val}")

    if gps_info:
        lat_dms = gps_info.get("GPSLatitude")
        lat_ref = gps_info.get("GPSLatitudeRef", "N")
        lon_dms = gps_info.get("GPSLongitude")
        lon_ref = gps_info.get("GPSLongitudeRef", "E")
        
        if lat_dms and lon_dms:
            lat = dms_to_decimal(lat_dms, lat_ref)
            lon = dms_to_decimal(lon_dms, lon_ref)
            print(f"  [GPS] Coordonate brute: Lat={lat_dms} {lat_ref}, Lon={lon_dms} {lon_ref}")
            print(f"  [GPS] Grade zecimale: {lat}, {lon}")

def carving_zip(cale_fisier, cale_iesire="gasit.zip"):
    with open(cale_fisier, "rb") as f:
        date = f.read()
    i = date.find(b"PK\x03\x04")
    if i != -1:
        with open(cale_iesire, "wb") as out:
            out.write(date[i:])
        print(f"\n[B4] Arhivă extrasă de la octetul {i} în '{cale_iesire}'")
        
        if zipfile.is_zipfile(cale_iesire):
            with zipfile.ZipFile(cale_iesire, "r") as z:
                print("  Fișiere în arhivă:", z.namelist())
                for nume in z.namelist():
                    continut = z.read(nume).decode("utf-8", errors="ignore")
                    print(f"  Conținut '{nume}': {continut.strip()}")
    else:
        print("\n[B4] Nu s-a găsit nicio semnătură ZIP.")

if __name__ == "__main__":
    for f in ["probe/foto.jpg", "probe/ascuns.png", "probe/xor.bin"]:
        if os.path.exists(f):
            print(f"[B1] Tip real pentru {f}: {tip_real(f)}")

    if os.path.exists("probe/ascuns.png"):
        siruri = extrage_strings("probe/ascuns.png")
        print(f"\n[B2] Ultimele șiruri citibile din probe/ascuns.png:")
        for s in siruri[-5:]:
            print(" ", s)

    if os.path.exists("probe/foto.jpg"):
        citeste_exif_gps("probe/foto.jpg")

    if os.path.exists("probe/ascuns.png"):
        carving_zip("probe/ascuns.png")