// particles.js
(function () {
  const canvas = document.getElementById("particles-canvas");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let particles = [];
  let animationId;
  let mouse = { x: null, y: null, prevX: null, prevY: null, speed: 0 };

  // Theme color definitions
  const themeColors = {
    nord: {
      particles: ["#8fbcbb", "#88c0d0", "#81a1c1", "#5e81ac"],
      mouseConnection: "136, 192, 208",
      particleConnection: "180, 142, 173",
    },
    tokyo: {
      particles: ["#7aa2f7", "#bb9af7", "#5d7cbf", "#89b4fa"],
      mouseConnection: "122, 162, 247",
      particleConnection: "187, 154, 247",
    },
    catppuccin: {
      particles: ["#cba6f7", "#89b4fa", "#94e2d5", "#f5c2e7"],
      mouseConnection: "203, 166, 247",
      particleConnection: "245, 194, 231",
    },
    gruvbox: {
      particles: ["#fe8019", "#fabd2f", "#b8bb26", "#83a598"],
      mouseConnection: "254, 128, 25",
      particleConnection: "211, 134, 155",
    },
    material: {
      particles: ["#82aaff", "#c792ea", "#89ddff", "#c3e88d"],
      mouseConnection: "130, 170, 255",
      particleConnection: "199, 146, 234",
    },
  };

  // Get current theme colors
  function getThemeColors() {
    const theme =
      document.documentElement.getAttribute("data-theme") || "tokyo";
    return themeColors[theme] || themeColors.tokyo;
  }

  // config
  const config = {
    particleCount: 100,
    particleMinSize: 1,
    particleMaxSize: 4,
    baseSpeed: 0.15,
    mouseRadius: 250,
    mouseConnectionRadius: 200,
    attractionStrength: 0.08,
    orbitStrength: 0.03,
    get colors() {
      return getThemeColors().particles;
    },
  };

  // resize
  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  // particle
  class Particle {
    constructor() {
      this.reset();
    }

    reset() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.size =
        Math.random() * (config.particleMaxSize - config.particleMinSize) +
        config.particleMinSize;
      this.baseSize = this.size;
      this.vx = (Math.random() - 0.5) * config.baseSpeed;
      this.vy = (Math.random() - 0.5) * config.baseSpeed;
      this.color =
        config.colors[Math.floor(Math.random() * config.colors.length)];
      this.opacity = Math.random() * 0.3 + 0.35;
      this.baseOpacity = this.opacity;
    }

    update() {
      if (mouse.x !== null && mouse.y !== null) {
        const dx = mouse.x - this.x;
        const dy = mouse.y - this.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < config.mouseRadius) {
          const force = (config.mouseRadius - distance) / config.mouseRadius;
          const angle = Math.atan2(dy, dx);

          // attract but keep orbit distance
          const orbitDistance = 70;
          if (distance > orbitDistance) {
            this.vx += Math.cos(angle) * force * config.attractionStrength;
            this.vy += Math.sin(angle) * force * config.attractionStrength;
          } else {
            // repel if too close
            const repelForce = (orbitDistance - distance) / orbitDistance;
            this.vx -= Math.cos(angle) * repelForce * 0.2;
            this.vy -= Math.sin(angle) * repelForce * 0.2;
          }

          // swirl
          const perpAngle = angle + Math.PI / 2;
          this.vx += Math.cos(perpAngle) * force * config.orbitStrength;
          this.vy += Math.sin(perpAngle) * force * config.orbitStrength;

          // mouse speed effect
          const mouseInfluence = Math.min(mouse.speed * 0.01, 1);
          this.vx += (Math.random() - 0.5) * mouseInfluence * 0.5;
          this.vy += (Math.random() - 0.5) * mouseInfluence * 0.5;

          // grow near mouse
          this.size = this.baseSize + force * 3;
          this.opacity = Math.min(this.baseOpacity + force * 0.7, 1);
        } else {
          // reset
          this.size += (this.baseSize - this.size) * 0.05;
          this.opacity += (this.baseOpacity - this.opacity) * 0.05;
        }

        // damping
        this.vx *= 0.98;
        this.vy *= 0.98;
      } else {
        // idle drift
        this.vx += (Math.random() - 0.5) * 0.01;
        this.vy += (Math.random() - 0.5) * 0.01;
        this.vx *= 0.99;
        this.vy *= 0.99;
        this.size += (this.baseSize - this.size) * 0.05;
        this.opacity += (this.baseOpacity - this.opacity) * 0.05;
      }

      // move
      this.x += this.vx;
      this.y += this.vy;

      // wrap edges
      const margin = 50;
      if (this.x < -margin) this.x = canvas.width + margin;
      if (this.x > canvas.width + margin) this.x = -margin;
      if (this.y < -margin) this.y = canvas.height + margin;
      if (this.y > canvas.height + margin) this.y = -margin;
    }

    draw() {
      const isGruvbox =
        document.documentElement.getAttribute("data-theme") === "gruvbox";

      // glow (skip for gruvbox)
      if (!isGruvbox && this.opacity > this.baseOpacity + 0.2) {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size * 2, 0, Math.PI * 2);
        const gradient = ctx.createRadialGradient(
          this.x,
          this.y,
          0,
          this.x,
          this.y,
          this.size * 2,
        );
        gradient.addColorStop(0, this.color + "40");
        gradient.addColorStop(1, "transparent");
        ctx.fillStyle = gradient;
        ctx.fill();
      }

      ctx.fillStyle = this.color;
      ctx.globalAlpha = this.opacity;

      if (isGruvbox) {
        // Draw squares for gruvbox
        const squareSize = this.size * 2;
        ctx.fillRect(
          this.x - squareSize / 2,
          this.y - squareSize / 2,
          squareSize,
          squareSize,
        );
      } else {
        // Draw circles for other themes
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.globalAlpha = 1;
    }
  }

  // mouse connections
  function drawMouseConnections() {
    if (mouse.x === null || mouse.y === null) return;

    particles.forEach((particle) => {
      const dx = particle.x - mouse.x;
      const dy = particle.y - mouse.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < config.mouseConnectionRadius) {
        const opacity = (1 - distance / config.mouseConnectionRadius) * 0.4;
        ctx.beginPath();
        ctx.moveTo(particle.x, particle.y);
        ctx.lineTo(mouse.x, mouse.y);
        ctx.strokeStyle = `rgba(${getThemeColors().mouseConnection}, ${opacity})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    });
  }

  // particle connections
  function drawParticleConnections() {
    if (mouse.x === null || mouse.y === null) return;

    for (let i = 0; i < particles.length; i++) {
      const p1 = particles[i];
      const distToMouse1 = Math.sqrt(
        (p1.x - mouse.x) ** 2 + (p1.y - mouse.y) ** 2,
      );
      if (distToMouse1 > config.mouseRadius) continue;

      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const distToMouse2 = Math.sqrt(
          (p2.x - mouse.x) ** 2 + (p2.y - mouse.y) ** 2,
        );
        if (distToMouse2 > config.mouseRadius) continue;

        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
          const opacity = (1 - distance / 100) * 0.2;
          ctx.beginPath();
          ctx.moveTo(p1.x, p1.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.strokeStyle = `rgba(${getThemeColors().particleConnection}, ${opacity})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      }
    }
  }

  // mouse glow
  function drawMouseGlow() {
    if (mouse.x === null || mouse.y === null) return;

    const gradient = ctx.createRadialGradient(
      mouse.x,
      mouse.y,
      0,
      mouse.x,
      mouse.y,
      config.mouseRadius * 0.6,
    );
    const colors = getThemeColors();
    gradient.addColorStop(0, `rgba(${colors.mouseConnection}, 0.08)`);
    gradient.addColorStop(0.5, `rgba(${colors.particleConnection}, 0.03)`);
    gradient.addColorStop(1, "transparent");

    ctx.beginPath();
    ctx.arc(mouse.x, mouse.y, config.mouseRadius * 0.6, 0, Math.PI * 2);
    ctx.fillStyle = gradient;
    ctx.fill();
  }

  // repel particles
  function repelParticles() {
    const repelDistance = 30;
    const repelStrength = 0.15;

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < repelDistance && distance > 0) {
          const force =
            ((repelDistance - distance) / repelDistance) * repelStrength;
          const angle = Math.atan2(dy, dx);

          particles[i].vx += Math.cos(angle) * force;
          particles[i].vy += Math.sin(angle) * force;
          particles[j].vx -= Math.cos(angle) * force;
          particles[j].vy -= Math.sin(angle) * force;
        }
      }
    }
  }

  // loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    drawMouseGlow();

    drawMouseConnections();
    drawParticleConnections();
    repelParticles();

    particles.forEach((particle) => {
      particle.update();
      particle.draw();
    });

    animationId = requestAnimationFrame(animate);
  }

  // init
  function init() {
    resize();
    particles = [];

    const screenArea = canvas.width * canvas.height;
    const baseArea = 1920 * 1080;
    const adjustedCount = Math.floor(
      config.particleCount * (screenArea / baseArea),
    );
    const count = Math.max(40, Math.min(adjustedCount, 180));

    for (let i = 0; i < count; i++) {
      particles.push(new Particle());
    }

    animate();
  }

  // events
  window.addEventListener("resize", () => {
    cancelAnimationFrame(animationId);
    init();
  });

  document.addEventListener("mousemove", (e) => {
    mouse.prevX = mouse.x;
    mouse.prevY = mouse.y;
    mouse.x = e.clientX;
    mouse.y = e.clientY;

    if (mouse.prevX !== null && mouse.prevY !== null) {
      const dx = mouse.x - mouse.prevX;
      const dy = mouse.y - mouse.prevY;
      mouse.speed = Math.sqrt(dx * dx + dy * dy);
    }
  });

  document.addEventListener("mouseleave", () => {
    mouse.x = null;
    mouse.y = null;
    mouse.speed = 0;
  });

  // reduced motion
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    canvas.style.display = "none";
    return;
  }

  // Listen for theme changes
  window.addEventListener("themechange", () => {
    // Update existing particle colors
    particles.forEach((particle) => {
      particle.color =
        config.colors[Math.floor(Math.random() * config.colors.length)];
    });
  });

  init();
})();
