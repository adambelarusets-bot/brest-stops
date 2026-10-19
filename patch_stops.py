import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Добавляем новые поля в STOPS (если их нет)
# Ищем массив STOPS и добавляем поля после buses
if "state:" not in html:
    # Пример: добавляем поля после каждого buses: [...]
    html = re.sub(
        r'(buses: \[[^\]]*\])',
        r'\1,\n    state: "good",        // good | satisfactory | bad\n    surface: "asphalt",   // asphalt | tile | grass\n    has_square: false,    // сквер\n    has_shop: false       // магазин',
        html
    )
    print("✅ Поля state, surface, has_square, has_shop добавлены в STOPS")
else:
    print("ℹ️ Поля уже есть, пропускаем")

# 2. Заменяем addMarkers на новую версию с цветами по состоянию
new_addMarkers = '''
function addMarkers() {
  STOPS.forEach(stop => {
    const el = document.createElement('div');
    // Цвет по состоянию
    let color = '#30d158'; // good
    if (stop.state === 'satisfactory') color = '#ff9f0a';
    if (stop.state === 'bad') color = '#ff453a';

    el.style.cssText = `
      width: 28px;
      height: 28px;
      background: ${color};
      border: 3px solid #ffffff;
      border-radius: 50%;
      cursor: pointer;
      box-shadow: 0 4px 16px ${color}99, 0 0 0 4px ${color}33;
      transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s ease;
    `;

    el.addEventListener('mouseenter', () => {
      el.style.transform = 'scale(1.3)';
      el.style.boxShadow = `0 6px 24px ${color}cc, 0 0 0 8px ${color}44`;
    });
    el.addEventListener('mouseleave', () => {
      el.style.transform = 'scale(1)';
      el.style.boxShadow = `0 4px 16px ${color}99, 0 0 0 4px ${color}33`;
    });

    // Покрытие
    let surfaceText = 'Асфальт';
    if (stop.surface === 'tile') surfaceText = 'Плитка';
    if (stop.surface === 'grass') surfaceText = 'Трава';

    const popup = new maplibregl.Popup({ offset: 20, closeButton: true, maxWidth: '300px' })
      .setHTML(`
        <div class="popup-title">${stop.name}</div>
        <div class="popup-addr">📍 ${stop.address}</div>
        <div class="popup-buses">
          ${stop.buses.slice(0, 6).map(b => `<span class="bus-chip">${b}</span>`).join('')}
          ${stop.buses.length > 6 ? `<span class="bus-chip">+${stop.buses.length - 6}</span>` : ''}
        </div>
        <div class="popup-info" style="margin-top:8px; font-size:12px; color:#aaa;">
          <div>🟢 Состояние: ${stop.state === 'good' ? 'Хорошее' : stop.state === 'satisfactory' ? 'Удовлетворительное' : 'Требует внимания'}</div>
          <div>🛣 Покрытие: ${surfaceText}</div>
          <div>🌳 Сквер: ${stop.has_square ? 'Есть' : 'Нет'}</div>
          <div>🛒 Магазин: ${stop.has_shop ? 'Есть' : 'Нет'}</div>
        </div>
        <button class="popup-btn" onclick="openStopPage('${stop.id}')">Подробнее</button>
      `);

    markers[stop.id] = new maplibregl.Marker({ element: el })
      .setLngLat(stop.coords)
      .setPopup(popup)
      .addTo(map);
  });
}
'''

# Заменяем старую функцию addMarkers
html = re.sub(
    r'function addMarkers\(\) \{.*?\n\}',
    new_addMarkers,
    html,
    flags=re.DOTALL
)
print("✅ Функция addMarkers заменена (цвета по состоянию + новые поля)")

# 3. Добавляем кнопки в шапку (GPS, слои)
if 'id="btn-locate"' not in html:
    html = html.replace(
        '<button class="btn-icon" id="btn-style" title="Стиль карты">🗺</button>',
        '''<button class="btn-icon" id="btn-style" title="Стиль карты">🗺</button>
    <button class="btn-icon" id="btn-locate" title="Моё местоположение">📍</button>
    <button class="btn-icon" id="btn-layers" title="Слои">🎨</button>'''
    )
    print("✅ Кнопки GPS и Слои добавлены в шапку")

# 4. Добавляем GPS-трекинг
if 'navigator.geolocation' not in html:
    gps_code = '''
// GPS-трекинг
let userMarker = null;
document.getElementById('btn-locate')?.addEventListener('click', () => {
  if (!navigator.geolocation) {
    alert('Геолокация не поддерживается');
    return;
  }
  navigator.geolocation.watchPosition(
    (pos) => {
      const { latitude, longitude } = pos.coords;
      if (!userMarker) {
        const el = document.createElement('div');
        el.style.cssText = `
          width: 20px; height: 20px;
          background: #0a84ff;
          border: 3px solid #fff;
          border-radius: 50%;
          box-shadow: 0 0 0 8px rgba(10,132,255,0.3);
        `;
        userMarker = new maplibregl.Marker({ element: el })
          .setLngLat([longitude, latitude])
          .addTo(map);
      } else {
        userMarker.setLngLat([longitude, latitude]);
      }
      map.flyTo({ center: [longitude, latitude], zoom: 16 });
    },
    (err) => alert('Ошибка GPS: ' + err.message),
    { enableHighAccuracy: true, maximumAge: 10000, timeout: 5000 }
  );
});
'''
    html = html.replace('</script>', gps_code + '\n</script>')
    print("✅ GPS-трекинг добавлен")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Файл index.html обновлён")
