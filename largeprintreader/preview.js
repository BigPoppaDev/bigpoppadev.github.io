// Live preview of the reading view. The values are the extension's own settings (version 0.2.0).
(function () {
  var root = document.querySelector('[data-pv]');
  if (!root) return;
  var THEMES = {
    cream: { label: 'Cream', bg: '#FBF5E6', fg: '#1A1A1A', bar: '#EFE6D0', accent: '#7A4A00' },
    white: { label: 'White', bg: '#FFFFFF', fg: '#000000', bar: '#EDEDED', accent: '#0645AD' },
    dark: { label: 'Dark', bg: '#1C1C1C', fg: '#F2F2F2', bar: '#2C2C2C', accent: '#8AB4F8' },
    contrast: { label: 'High contrast', bg: '#000000', fg: '#FFFF00', bar: '#000000', accent: '#FFFFFF' }
  };
  var SPACINGS = { normal: { label: 'Normal', value: 1.5 }, roomy: { label: 'Roomy', value: 1.8 }, extra: { label: 'Extra', value: 2.2 } };
  var LETTERS = {
    sans: { label: 'Plain', stack: 'Verdana, Tahoma, "Segoe UI", Arial, sans-serif' },
    serif: { label: 'Classic', stack: 'Georgia, "Times New Roman", serif' }
  };
  var ORDER = { theme: ['cream', 'white', 'dark', 'contrast'], spacing: ['normal', 'roomy', 'extra'], letters: ['sans', 'serif'] };
  var MIN = 18, MAX = 64, STEP = 4;
  var state = { size: 28, theme: 'cream', spacing: 'roomy', letters: 'sans' };

  function next(list, current) { return list[(list.indexOf(current) + 1) % list.length]; }
  function show(name, text) { var el = root.querySelector('[data-show="' + name + '"]'); if (el) el.textContent = text; }
  function apply() {
    var t = THEMES[state.theme];
    root.style.setProperty('--pv-bg', t.bg);
    root.style.setProperty('--pv-fg', t.fg);
    root.style.setProperty('--pv-bar', t.bar);
    root.style.setProperty('--pv-accent', t.accent);
    root.style.setProperty('--pv-size', state.size + 'px');
    root.style.setProperty('--pv-line', String(SPACINGS[state.spacing].value));
    root.style.setProperty('--pv-font', LETTERS[state.letters].stack);
    show('theme', t.label);
    show('spacing', SPACINGS[state.spacing].label);
    show('letters', LETTERS[state.letters].label);
    root.querySelector('[data-act="smaller"]').disabled = state.size <= MIN;
    root.querySelector('[data-act="bigger"]').disabled = state.size >= MAX;
  }
  root.addEventListener('click', function (e) {
    var btn = e.target.closest('button[data-act]');
    if (!btn) return;
    var act = btn.getAttribute('data-act');
    if (act === 'smaller') state.size = Math.max(MIN, state.size - STEP);
    else if (act === 'bigger') state.size = Math.min(MAX, state.size + STEP);
    else if (ORDER[act]) state[act] = next(ORDER[act], state[act]);
    apply();
  });
  apply();
})();
