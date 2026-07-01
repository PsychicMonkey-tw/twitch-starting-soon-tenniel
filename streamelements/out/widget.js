(function () {
  const screen = document.querySelector(".screen");
  const catHead = document.querySelector(".layer-cat-head");
  const alice = document.querySelector(".layer-alice");
  const channelAvatar = document.querySelector(".channel-avatar");
  const channelName = document.querySelector(".channel-name");
  const channelAnchor = document.querySelector(".channel-anchor");
  const titleSubtitle = document.querySelector(".title-subtitle");

  function applyConfig(fieldData) {
    const data = fieldData || {};
    const name = String(data.channelName || "").trim();
    const avatar = String(data.channelAvatar || "").trim();
    const subtitle = String(data.titleSubtitle || "").trim();

    if (channelName) {
      channelName.textContent = name;
    }

    if (channelAvatar) {
      channelAvatar.src = avatar;
      channelAvatar.alt = name ? `Аватар канала ${name}` : "Аватар канала";
    }

    if (channelAnchor) {
      channelAnchor.classList.toggle("is-hidden", !name && !avatar);
    }

    if (titleSubtitle) {
      titleSubtitle.textContent = subtitle;
    }
  }

  function fitScreen() {
    if (!screen) return;
    const scale = Math.min(window.innerWidth / 1920, window.innerHeight / 1080);
    screen.style.transform = `scale(${scale})`;
  }

  if (catHead) {
    catHead.style.animationDuration = `${4.8 + Math.random() * 0.6}s`;
  }
  if (alice) {
    alice.style.animationDuration = `${5.2 + Math.random() * 0.6}s`;
    alice.style.animationDelay = `${0.2 + Math.random() * 0.4}s`;
  }

  window.addEventListener("onWidgetLoad", (obj) => {
    applyConfig(obj.detail.fieldData);
    fitScreen();
  });

  window.addEventListener("resize", fitScreen);
  fitScreen();
})();
