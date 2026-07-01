/**
 * Starting Soon (Tenniel) — OBS / Browser Source, 1920×1080
 *
 * Настройки (ниже): channelName, channelAvatar, titleSubtitle
 * Или URL: ?name=Канал&avatar=assets/my.png&subtitle=Текст
 */
(function () {
  const STREAM_CONFIG = {
    channelName: "",
    channelAvatar: "",
    titleSubtitle: "",
  };

  const screen = document.querySelector(".screen");
  const catHead = document.querySelector(".layer-cat-head");
  const alice = document.querySelector(".layer-alice");
  const channelAvatar = document.querySelector(".channel-avatar");
  const channelName = document.querySelector(".channel-name");
  const channelAnchor = document.querySelector(".channel-anchor");
  const titleSubtitle = document.querySelector(".title-subtitle");

  function readConfig() {
    const params = new URLSearchParams(window.location.search);

    return {
      channelName:
        params.get("name") ||
        params.get("channel") ||
        STREAM_CONFIG.channelName ||
        "",
      channelAvatar:
        params.get("avatar") ||
        STREAM_CONFIG.channelAvatar ||
        "",
      titleSubtitle:
        params.has("subtitle")
          ? params.get("subtitle")
          : STREAM_CONFIG.titleSubtitle ?? "",
    };
  }

  function isValidAvatarUrl(url) {
    const value = String(url || "").trim();
    return Boolean(value) && !value.includes("{{");
  }

  function applyChannelConfig() {
    if (!channelAnchor) return;

    const config = readConfig();
    const name = String(config.channelName).trim();
    const avatar = isValidAvatarUrl(config.channelAvatar)
      ? String(config.channelAvatar).trim()
      : "";

    if (channelName) {
      channelName.textContent = name;
      channelName.hidden = !name;
    }

    if (channelAvatar) {
      if (avatar) {
        channelAvatar.src = avatar;
        channelAvatar.alt = name ? `Аватар канала ${name}` : "Аватар канала";
        channelAvatar.hidden = false;
      } else {
        channelAvatar.removeAttribute("src");
        channelAvatar.alt = "";
        channelAvatar.hidden = true;
      }
    }

    channelAnchor.classList.toggle("is-hidden", !name && !avatar);
  }

  function applyTitleSubtitle() {
    if (!titleSubtitle) return;

    const text = String(readConfig().titleSubtitle ?? "").trim();
    titleSubtitle.textContent = text;
    titleSubtitle.hidden = !text;
  }

  if (catHead) {
    catHead.style.animationDuration = `${4.8 + Math.random() * 0.6}s`;
  }
  if (alice) {
    alice.style.animationDuration = `${5.2 + Math.random() * 0.6}s`;
    alice.style.animationDelay = `${0.2 + Math.random() * 0.4}s`;
  }

  function fitScreen() {
    if (!screen) return;
    const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    screen.style.transform = `scale(${scale})`;
  }

  applyChannelConfig();
  applyTitleSubtitle();
  window.addEventListener("resize", fitScreen);
  fitScreen();
})();
