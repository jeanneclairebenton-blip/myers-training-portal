// confetti.js — Shared rainbow confetti for all onboarding modules
function checkConfetti() {
  var boxes = document.querySelectorAll('input[type="checkbox"]');
  var allChecked = Array.from(boxes).every(function(b) { return b.checked; });
  if (allChecked) launchConfetti();
}

function launchConfetti() {
  var canvas = document.getElementById('confetti-canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'confetti-canvas';
    canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;';
    document.body.appendChild(canvas);
  }
  var ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  var pieces = [];
  var colors = [
    '#FF0A54','#FF477E','#FF7096','#FF85A1',  // pinks/reds
    '#FF6B35','#FFA62B','#FFD166',              // oranges/yellows
    '#06D6A0','#1B9AAA','#06BA63',              // greens/teals
    '#118AB2','#073B4C','#7B68EE',              // blues/purples
    '#9B5DE5','#F15BB5','#FEE440',              // vibrant accents
    '#00BBF9','#00F5D4','#C9941F','#FBE8B7'     // cyan + myers gold
  ];
  var shapes = ['rect','rect','rect','circle','circle'];

  for (var i = 0; i < 400; i++) {
    pieces.push({
      x: Math.random() * canvas.width,
      y: -(Math.random() * canvas.height),
      w: Math.random() * 12 + 4,
      h: Math.random() * 8 + 3,
      color: colors[Math.floor(Math.random() * colors.length)],
      shape: shapes[Math.floor(Math.random() * shapes.length)],
      vx: (Math.random() - 0.5) * 3,
      vy: Math.random() * 4 + 2,
      gravity: 0.08 + Math.random() * 0.05,
      rot: Math.random() * 360,
      rv: (Math.random() - 0.5) * 12,
      opacity: 1,
      delay: Math.random() * 40
    });
  }

  var frame = 0;
  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var alive = false;
    pieces.forEach(function(p) {
      if (frame < p.delay) { alive = true; return; }
      p.vy += p.gravity;
      p.vx *= 0.99;
      p.x += p.vx;
      p.y += p.vy;
      p.rot += p.rv;
      if (frame > 160) p.opacity -= 0.008;
      if (p.opacity <= 0) return;
      alive = true;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rot * Math.PI / 180);
      ctx.globalAlpha = Math.max(0, p.opacity);
      ctx.fillStyle = p.color;
      if (p.shape === 'circle') {
        ctx.beginPath();
        ctx.arc(0, 0, p.w / 2, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h);
      }
      ctx.restore();
    });
    frame++;
    if (alive && frame < 350) requestAnimationFrame(draw);
    else ctx.clearRect(0, 0, canvas.width, canvas.height);
  }
  draw();
}
