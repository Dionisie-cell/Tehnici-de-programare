import re
import base64
import hashlib
import argparse
import json
import os
from urllib.parse import unquote

def ghici_strat(s):
    s = s.strip()
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if len(s) >= 2 and len(s) % 2 == 0 and re.fullmatch(r"[0-9a-fA-F]+", s):
        return "hex"
    if len(s) >= 4 and len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"

def desfa(s):
    s = s.strip()
    strat = ghici_strat(s)
    try:
        if strat == "base64":
            return strat, base64.b64decode(s)
        elif strat == "hex":
            return strat, bytes.fromhex(s)
        elif strat == "url":
            return strat, unquote(s).encode()
    except Exception:
        pass
    return "necunoscut", s.encode()

def citibil(b):
    return len(b) > 0 and all(32 <= c < 127 or c in (9, 10, 13) for c in b)

def decodeaza_straturi(val_initiala):
    val = val_initiala.strip()
    straturi_aplicate = []
    
    for _ in range(10):
        strat, b = desfa(val)
        if strat == "necunoscut":
            break
        straturi_aplicate.append(strat)
        try:
            text_urmator = b.decode("utf-8").strip()
            if ghici_strat(text_urmator) == "necunoscut" and citibil(b):
                return straturi_aplicate, text_urmator
            val = text_urmator
        except UnicodeDecodeError:
            break
            
    return straturi_aplicate, val

def sparge_xor(date_bytes):
    rezultate = []
    for k in range(256):
        clar = bytes(b ^ k for b in date_bytes)
        if citibil(clar):
            text = clar.decode("ascii", errors="ignore")
            rezultate.append((k, text))
    return rezultate

def sparge_hash(tinta, cale_wordlist="probe/wordlist.txt"):
    tinta = tinta.strip().lower()
    lungime = len(tinta)
    algoritmi = {32: "md5", 40: "sha1", 64: "sha256"}
    alg = algoritmi.get(lungime)
    if not alg or not os.path.exists(cale_wordlist):
        return alg, None

    with open(cale_wordlist, encoding="latin1") as f:
        for cuv in f:
            cuv = cuv.strip()
            h = hashlib.new(alg, cuv.encode()).hexdigest()
            if h == tinta:
                return alg, cuv
    return alg, None

def main():
    if os.path.exists("probe/mesaj.txt"):
        continut = open("probe/mesaj.txt", "r", encoding="utf-8").read().strip()
        straturi, rez_mesaj = decodeaza_straturi(continut)
        print(f"[A4] probe/mesaj.txt -> Straturi: {straturi} | Mesaj: {rez_mesaj}")
        
        os.makedirs("arsenal/forensics", exist_ok=True)
        with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
            json.dump({"strat": " -> ".join(straturi), "rezultat": rez_mesaj}, f, indent=4, ensure_ascii=False)

    if os.path.exists("probe/xor.bin"):
        date_xor = open("probe/xor.bin", "rb").read()
        for k, text in sparge_xor(date_xor):
            print(f"[A5] probe/xor.bin -> Cheie XOR: {k} | Text: {text}")

    if os.path.exists("probe/hashuri.txt"):
        with open("probe/hashuri.txt", "r") as f:
            for linie in f:
                h = linie.strip()
                if h:
                    alg, parola = sparge_hash(h)
                    print(f"[A6] Hash ({alg}): {h} -> Parolă găsită: {parola}")

if __name__ == "__main__":
    main()