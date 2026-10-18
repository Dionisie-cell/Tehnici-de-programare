from PIL import Image
import os

def ascunde_lsb(cale_intrare, mesaj_bytes, cale_iesire="stego.png"):
    img = Image.open(cale_intrare).convert("RGB")
    px = list(img.getdata())
    
    mesaj_complet = mesaj_bytes + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_complet)
    
    idx_bit = 0
    nr_biti = len(biti)
    px_nou = []

    for r, g, b in px:
        if idx_bit < nr_biti:
            r = (r & ~1) | int(biti[idx_bit])
            idx_bit += 1
        if idx_bit < nr_biti:
            g = (g & ~1) | int(biti[idx_bit])
            idx_bit += 1
        if idx_bit < nr_biti:
            b = (b & ~1) | int(biti[idx_bit])
            idx_bit += 1
        px_nou.append((r, g, b))

    img.putdata(px_nou)
    img.save(cale_iesire, "PNG")
    print(f"[B5] Mesaj ascuns cu succes în '{cale_iesire}'.")

def dezvaluie_lsb(cale_stego="stego.png"):
    px = list(Image.open(cale_stego).convert("RGB").getdata())
    biti = []
    
    for r, g, b in px:
        biti.append(str(r & 1))
        biti.append(str(g & 1))
        biti.append(str(b & 1))

    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        octet_str = "".join(biti[i:i+8])
        val = int(octet_str, 2)
        if val == 0:
            break
        octeti.append(val)

    mesaj_extras = octeti.decode("utf-8", errors="ignore")
    print(f"[B6] Mesaj dezvăluit din '{cale_stego}': {mesaj_extras}")
    return mesaj_extras

if __name__ == "__main__":
    if os.path.exists("probe/foto.jpg"):
        mesaj = b"FLAG{ascuns_in_pixeli}"
        ascunde_lsb("probe/foto.jpg", mesaj, "stego.png")
        dezvaluie_lsb("stego.png")