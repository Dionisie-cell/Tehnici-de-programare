import os
import base64
import hashlib
import zipfile
import io
from urllib.parse import quote
from PIL import Image

os.makedirs("probe", exist_ok=True)

# 1. probe/mesaj.txt (șir codat în mai multe straturi: URL -> Hex -> Base64)
mesaj_secret = "FLAG{straturi_desfacute_cu_succes}"
s1 = quote(mesaj_secret)                      # Strat 1: URL encoding
s2 = s1.encode().hex()                        # Strat 2: Hex
s3 = base64.b64encode(s2.encode()).decode()   # Strat 3: Base64

with open("probe/mesaj.txt", "w", encoding="utf-8") as f:
    f.write(s3)

# 2. probe/xor.bin (text criptat cu XOR pe un octet, cheia = 42)
cheie_xor = 42
mesaj_xor = b"FLAG{xor_spart_prin_forta_bruta}"
xor_bytes = bytes(b ^ cheie_xor for b in mesaj_xor)
with open("probe/xor.bin", "wb") as f:
    f.write(xor_bytes)

# 3. probe/wordlist.txt și probe/hashuri.txt (hash MD5 de spart cu dicționarul)
parole = ["123456", "admin", "parola123", "utm2026", "securitate", "chisinau", "forensics"]
parola_tinta = "securitate"
with open("probe/wordlist.txt", "w", encoding="latin1") as f:
    f.write("\n".join(parole) + "\n")

hash_tinta = hashlib.md5(parola_tinta.encode()).hexdigest()
with open("probe/hashuri.txt", "w", encoding="utf-8") as f:
    f.write(hash_tinta + "\n")

# 4. probe/foto.jpg (poză JPEG cu metadate EXIF și coordonate GPS)
img_jpg = Image.new("RGB", (200, 200), color=(30, 90, 160))
exif = img_jpg.getexif()
exif[271] = "Camera_Forensics_UTM"   # Make
exif[272] = "Model_SI_266"           # Model
# Tag 34853 = GPSInfo (Coordonate: 47° 3' 36" N, 28° 52' 12" E -> Chișinău, UTM)
exif[34853] = {
    1: "N",
    2: (47.0, 3.0, 36.0),
    3: "E",
    4: (28.0, 52.0, 12.0)
}
img_jpg.save("probe/foto.jpg", "JPEG", exif=exif)

# 5. probe/ascuns.png (imagine PNG cu o arhivă ZIP lipită la coadă)
img_png = Image.new("RGB", (150, 150), color=(40, 140, 80))
png_buf = io.BytesIO()
img_png.save(png_buf, format="PNG")
png_bytes = png_buf.getvalue()

zip_buf = io.BytesIO()
with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("secret.txt", "FLAG{arhiva_extrasa_din_png_prin_carving}\n")
zip_bytes = zip_buf.getvalue()

indiciu = b"\n# INDICIU_STRINGS: Cauta semnatura PK pentru a extrage secret.txt!\n"
with open("probe/ascuns.png", "wb") as f:
    f.write(png_bytes + indiciu + zip_bytes)

print("Toate fișierele din 'probe/' au fost generate cu succes!")