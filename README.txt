Twitch Starting Soon — John Tenniel (живописный арт)
====================================================

Экран «Скоро начнём» для OBS Browser Source (1920×1080).
Иллюстрации в стиле Джона Тенниела — растровый арт, не вектор.

Слои (HTML + PNG):
  1. background.jpg   — лес (ваш фон, 1920×1080)
  2. alice-cutout.png — девочка, вырезанный силуэт (анимация покачивания)

Исходники генерации: assets/ в .cursor/projects (scene-reference, слои).
Подготовка слоёв: python prepare_assets.py

OBS:
  Browser Source → Local file → index.html
  1920 × 1080

Настройка канала (аватар + название + подпись):
  Откройте config.js:
    channelName, channelAvatar, titleSubtitle
  titleSubtitle — подпись под заголовком; "" = скрыта
  Или URL:
    index.html?name=МойКанал&avatar=assets/my-avatar.png&subtitle=Скоро%20будем

Файлы:
  index.html, style.css, script.js, config.js
  assets/*.jpg, assets/*.png
