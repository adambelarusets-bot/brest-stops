#!/bin/bash
cd ~/Desktop/brest_stops

echo "═══ 1. Обновляем SITE_URL ═══"
python3 << 'PYEOF'
import re

SITE_URL = "https://adambelarusets-bot.github.io/brest-stops/index.html"

with open("generate_qr.py", "r", encoding="utf-8") as f:
    code = f.read()

code = re.sub(
    r'SITE_URL = "[^"]*"',
    f'SITE_URL = "{SITE_URL}"',
    code
)

with open("generate_qr.py", "w", encoding="utf-8") as f:
    f.write(code)

print(f"✅ SITE_URL: {SITE_URL}")
PYEOF

echo ""
echo "═══ 2. Генерируем QR ═══"
python3 generate_qr.py

echo ""
echo "═══ 3. Проверка ═══"
ls -la qr_codes/

echo ""
echo "═══ 4. Git status ═══"
git status

echo ""
echo "═══ 5. Коммит и пуш ═══"
git add generate_qr.py
git add qr_codes/
git commit -m "Final: QR коды для публичного сайта"
git push

echo ""
echo "✅ Готово!"
