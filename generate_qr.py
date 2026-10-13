#!/usr/bin/env python3
import os
import qrcode

SITE_URL = "https://adambelarusets-bot.github.io/brest-stops/index.html"
OUTPUT_DIR = os.path.expanduser("~/Desktop/brest_stops/qr_codes")
os.makedirs(OUTPUT_DIR, exist_ok=True)

STOPS = [
    ("rechickaya",    "Речицкая"),
    ("hlebprom",      "Хлебпром"),
    ("shkola",        "Школа"),
    ("agrotrans",     "Агротранс"),
    ("rybtorg",       "База Рыбторг"),
    ("myasokombinat", "Мясокомбинат"),
]

print("📱 Генератор QR-кодов\n")

for stop_id, stop_name in STOPS:
    url = f"{SITE_URL}#stop={stop_id}"
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=12, border=3)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(OUTPUT_DIR, f"{stop_id}.png"))
    print(f"✅ {stop_name}: {stop_id}.png")

print(f"\n✅ Готово: {len(STOPS)} QR в {OUTPUT_DIR}")
