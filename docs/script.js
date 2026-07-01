/**
 * Twitch Browser Source — Starting Soon (Tenniel)
 * Вписывает кадр 1920×1080 целиком в окно (без обрезки).
 */

(function () {
  const screen = document.querySelector(".screen");
  const catHead = document.querySelector(".layer-cat-head");
  const alice = document.querySelector(".layer-alice");
  const channelAvatar = document.querySelector(".channel-avatar");
  const channelName = document.querySelector(".channel-name");
  const channelAnchor = document.querySelector(".channel-anchor");
  const titleSubtitle = document.querySelector(".title-subtitle");

  function readConfig() {
    const params = new URLSearchParams(window.location.search);
    const fileConfig = window.STREAM_CONFIG || {};

    return {
      channelName:
        params.get("name") ||
        params.get("channel") ||
        fileConfig.channelName ||
        "",
      channelAvatar:
        params.get("avatar") ||
        fileConfig.channelAvatar ||
        "assets/channel-avatar.png",
      titleSubtitle:
        params.has("subtitle")
          ? params.get("subtitle")
          : fileConfig.titleSubtitle ?? "",
    };
  }

  function applyChannelConfig() {
    if (!channelAnchor) return;

    const config = readConfig();
    const name = String(config.channelName).trim();
    const avatar = String(config.channelAvatar).trim();

    if (channelName) {
      channelName.textContent = name || "Название канала";
    }

    if (channelAvatar && avatar) {
      channelAvatar.src = avatar;
      channelAvatar.alt = name ? `Аватар канала ${name}` : "Аватар канала";
    }

    channelAnchor.hidden = !name && !avatar;
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
