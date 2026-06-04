from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components
from ui.components.html import html_block


def render_home_section() -> None:
    """Renders the HTML layout and styles for the Artificial Hero section in full screen."""
    theme = st.session_state.get("theme", "dark")
    is_dark = theme == "dark"
    next_theme = "light" if is_dark else "dark"
    theme_label = "Light theme" if is_dark else "Dark theme"
    
    # Theme-aware active color
    active_color = "#7ddcff" if is_dark else "#3D9DF3"
    
    html_block(f"""
    <div id="artificial-hero-container" style="
      position: relative;
      width: 100% !important;
      height: 180vh;
      background: #000;
      overflow: clip;
    ">
      <!-- Sticky Container -->
      <div style="
        position: sticky;
        top: 0;
        width: 100%;
        height: calc(100vh - 32px);
        overflow: hidden;
        z-index: 10;
      ">
        
        <!-- Canvases -->
        <canvas id="artificial-hero-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: #000;"></canvas>
        <canvas id="artificial-hero-grain-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; mix-blend-mode: overlay; opacity: 0.6;"></canvas>

        <!-- Premium Top Navigation replacing Sidebar on Home page -->
        <nav style="
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          z-index: 100;
          padding: 1.2rem 2.5rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          background: rgba(0, 0, 0, 0.45);
          backdrop-filter: blur(12px) saturate(120%);
          -webkit-backdrop-filter: blur(12px) saturate(120%);
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        ">
          <!-- Logo / Branding -->
          <div style="display: flex; align-items: center; gap: 10px;">
            <div style="
              width: 34px;
              height: 34px;
              border-radius: 8px;
              display: grid;
              place-items: center;
              color: #080a0d;
              background: linear-gradient(135deg, #7ddcff, #6ea8ff);
              font-family: Arial, sans-serif;
              font-size: 11px;
              font-weight: 800;
              box-shadow: 0 0 16px rgba(125, 220, 255, 0.35);
            ">PR</div>
            <div style="font-family: Arial, sans-serif; line-height: 1.2;">
              <strong style="color: white; font-size: 13.5px; display: block; font-weight: 750; letter-spacing: 0.2px;">PR.dev</strong>
              <span style="color: rgba(255,255,255,0.48); font-size: 9px; display: block; font-family: monospace;">Optical analytics</span>
            </div>
          </div>
          
          <!-- Navigation Links -->
          <div style="
            display: flex;
            gap: 2.2rem;
            font-family: Arial, sans-serif;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
          ">
            <a href="?page=home&theme={theme}" target="_self" class="nav-link" style="color: {active_color}; text-decoration: none; font-weight: 750; border-bottom: 2px solid {active_color}; padding-bottom: 4px;">
              Home
            </a>
            <a href="?page=simulation&theme={theme}" target="_self" class="nav-link" style="color: white; text-decoration: none; opacity: 0.85;">
              Simulation
            </a>
            <a href="?page=theory&theme={theme}" target="_self" class="nav-link" style="color: white; text-decoration: none; opacity: 0.85;">
              Theory
            </a>
            <a href="?page=architecture&theme={theme}" target="_self" class="nav-link" style="color: white; text-decoration: none; opacity: 0.85;">
              Architecture
            </a>
            <a href="?page=publisher&theme={theme}" target="_self" class="nav-link" style="color: white; text-decoration: none; opacity: 0.85;">
              Publisher
            </a>
          </div>
          
          <!-- Theme Switcher -->
          <div style="
            display: flex;
            align-items: center;
            gap: 1rem;
          ">
            <a href="?page=home&theme={next_theme}" target="_self" class="nav-link" style="
              color: {active_color};
              text-decoration: none;
              border: 1px solid rgba(125, 220, 255, 0.3);
              background: rgba(125, 220, 255, 0.08);
              padding: 6px 14px;
              border-radius: 999px;
              font-family: Arial, sans-serif;
              font-size: 10px;
              font-weight: 600;
              letter-spacing: 0.5px;
              text-transform: uppercase;
            ">
              {theme_label}
            </a>
          </div>
        </nav>

        <!-- Large text -->
        <div id="artificial-hero-large-text" style="
          position: absolute;
          bottom: 15%;
          left: 0;
          right: 0;
          z-index: 50;
          pointer-events: none;
          transition: transform 0.1s ease-out;
        ">
          <div style="
            font-family: 'Arial Black', Arial, sans-serif;
            font-size: clamp(4rem, 10vw, 10rem);
            font-weight: 900;
            color: white;
            text-align: center;
            line-height: 0.8;
            letter-spacing: -0.02em;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
            filter: contrast(1.2);
          ">
            ARTIFICIAL
          </div>
        </div>

        <!-- Left side text -->
        <div id="artificial-hero-left-text" style="
          position: absolute;
          left: 2rem;
          top: 40%;
          z-index: 50;
          transition: transform 0.1s ease-out;
        ">
          <div style="
            font-family: Arial, sans-serif;
            font-size: 11px;
            color: white;
            line-height: 1.4;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.8;
            max-width: 150px;
          ">
            In the dark<br />
            is where<br />
            light takes form<br />
            <br />
          </div>
        </div>

        <!-- Right side text -->
        <div id="artificial-hero-right-text" style="
          position: absolute;
          right: 2rem;
          top: 40%;
          z-index: 50;
          transition: transform 0.1s ease-out;
        ">
          <div style="
            font-family: Arial, sans-serif;
            font-size: 11px;
            color: white;
            line-height: 1.4;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            opacity: 0.8;
            max-width: 150px;
            text-align: right;
          ">
            In emptiness<br/>
            we find<br/>
            true happiness
          </div>
        </div>

        <!-- Bottom text -->
        <div id="artificial-hero-bottom-text" style="
          position: absolute;
          bottom: 8%;
          left: 2rem;
          z-index: 50;
          transition: transform 0.1s ease-out;
        ">
          <div style="
            font-family: Arial, sans-serif;
            font-size: 10px;
            color: white;
            letter-spacing: 1px;
            text-transform: uppercase;
            opacity: 0.7;
          ">
            Art & Design by @scottclayton
          </div>
        </div>

      </div>

      <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&display=swap');
        
        .nav-link {{
          transition: opacity 0.2s ease;
        }}
        .nav-link:hover {{
          opacity: 1 !important;
        }}

        /* Full-Screen Styling Overrides for Home Page */
        html.swdm-home-active .swdm-sidebar {{
          display: none !important;
        }}
        html.swdm-home-active .st-key-dashboard_shell {{
          left: 16px !important;
          width: calc(100vw - 32px) !important;
          max-height: calc(100vh - 32px) !important;
          top: 16px !important;
          bottom: 16px !important;
          padding: 0 !important;
        }}
      </style>
    </div>
    """)


def inject_hero_scripts() -> None:
    """Uses st.components.v1.html to execute the script in a same-origin iframe.

    The script targets the parent page (`window.parent.document`) to run the
    canvas drawing loop and ScrollTrigger, managing the HTML class lifecycle.
    """
    components.html("""
    <script id="swdm-hero-js">
    (function() {
      try {
        var doc = (window.parent && window.parent.document) ? window.parent.document : document;
        var win = (window.parent && window.parent.document) ? window.parent : window;

        if (doc.__swdmHeroInit) return;
        doc.__swdmHeroInit = true;

        // Visual error handler in case anything breaks
        win.onerror = function(message, source, lineno, colno, error) {
          var errDiv = doc.getElementById('swdm-hero-error-box');
          if (!errDiv) {
            errDiv = doc.createElement('div');
            errDiv.id = 'swdm-hero-error-box';
            errDiv.style.position = 'fixed';
            errDiv.style.bottom = '10px';
            errDiv.style.right = '10px';
            errDiv.style.background = 'rgba(255, 0, 0, 0.95)';
            errDiv.style.color = 'white';
            errDiv.style.zIndex = '999999';
            errDiv.style.padding = '15px';
            errDiv.style.fontFamily = 'monospace';
            errDiv.style.fontSize = '11px';
            errDiv.style.whiteSpace = 'pre-wrap';
            errDiv.style.maxWidth = '450px';
            errDiv.style.borderRadius = '5px';
            errDiv.style.boxShadow = '0 4px 15px rgba(0,0,0,0.5)';
            doc.body.appendChild(errDiv);
          }
          errDiv.textContent = 'Error: ' + message + ' (Line: ' + lineno + ')';
          return false;
        };

        function loadScript(src, cb) {
          var s = doc.createElement('script');
          s.src = src;
          s.onload = cb;
          s.onerror = function() {
            if (win.onerror) win.onerror('Failed to load script: ' + src, '', 0, 0, null);
          };
          doc.head.appendChild(s);
        }

        function initHero(container) {
          var canvas = doc.getElementById('artificial-hero-canvas');
          var grainCanvas = doc.getElementById('artificial-hero-grain-canvas');
          if (!canvas || !grainCanvas) return;

          var ctx = canvas.getContext('2d');
          var grainCtx = grainCanvas.getContext('2d');
          if (!ctx || !grainCtx) return;

          // Set full-screen HTML active class on mount
          var htmlEl = doc.documentElement;
          htmlEl.classList.add('swdm-home-active');

          var density = ' .:-=+*#%@';
          var params = {
            rotation: 0,
            atmosphereShift: 0,
            glitchIntensity: 0,
            glitchFrequency: 0
          };

          // GSAP Animations
          win.gsap.to(params, {
            rotation: Math.PI * 2,
            duration: 20,
            repeat: -1,
            ease: "none"
          });

          win.gsap.to(params, {
            atmosphereShift: 1,
            duration: 6,
            repeat: -1,
            yoyo: true,
            ease: "sine.inOut"
          });

          win.gsap.to(params, {
            glitchIntensity: 1,
            duration: 0.1,
            repeat: -1,
            yoyo: true,
            ease: "power2.inOut",
            repeatDelay: Math.random() * 3 + 1
          });

          win.gsap.to(params, {
            glitchFrequency: 1,
            duration: 0.05,
            repeat: -1,
            yoyo: true,
            ease: "none"
          });

          // ScrollTrigger setup
          var scrollProgress = 0;
          var largeText = doc.getElementById('artificial-hero-large-text');
          var leftText = doc.getElementById('artificial-hero-left-text');
          var rightText = doc.getElementById('artificial-hero-right-text');
          var bottomText = doc.getElementById('artificial-hero-bottom-text');

          var scrollerElement = doc.querySelector('.st-key-dashboard_shell') || doc.querySelector('.main') || win;

          var trigger = win.ScrollTrigger.create({
            trigger: container,
            scroller: scrollerElement,
            start: "top top",
            end: "bottom top",
            scrub: 1,
            onUpdate: function(self) {
              scrollProgress = self.progress;
              
              if (largeText) {
                largeText.style.transform = 'translateY(' + (scrollProgress * 100) + 'px)';
                largeText.style.opacity = Math.max(0, 1 - scrollProgress * 1.5);
              }
              if (leftText) {
                leftText.style.transform = 'translateX(' + (-scrollProgress * 200) + 'px)';
                leftText.style.opacity = Math.max(0, 1 - scrollProgress * 2);
              }
              if (rightText) {
                rightText.style.transform = 'translateX(' + (scrollProgress * 200) + 'px)';
                rightText.style.opacity = Math.max(0, 1 - scrollProgress * 2);
              }
              if (bottomText) {
                bottomText.style.transform = 'translateY(' + (scrollProgress * 50) + 'px)';
                bottomText.style.opacity = Math.max(0, 1 - scrollProgress * 1.5);
              }
            }
          });

          var generateFilmGrain = function(width, height, intensity) {
            if (intensity === undefined) intensity = 0.15;
            var imageData = grainCtx.createImageData(width, height);
            var data = imageData.data;
            for (var i = 0; i < data.length; i += 4) {
              var grain = (Math.random() - 0.5) * intensity * 255;
              data[i] = Math.max(0, Math.min(255, 128 + grain));
              data[i + 1] = Math.max(0, Math.min(255, 128 + grain));
              data[i + 2] = Math.max(0, Math.min(255, 128 + grain));
              data[i + 3] = Math.abs(grain) * 3;
            }
            return imageData;
          };

          var drawGlitchedOrb = function(centerX, centerY, radius, hue, time, glitchIntensity) {
            ctx.save();
            var shouldGlitch = Math.random() < 0.1 && glitchIntensity > 0.5;
            var glitchOffset = shouldGlitch ? (Math.random() - 0.5) * 20 * glitchIntensity : 0;
            var glitchScale = shouldGlitch ? 1 + (Math.random() - 0.5) * 0.3 * glitchIntensity : 1;
            if (shouldGlitch) {
              ctx.translate(glitchOffset, glitchOffset * 0.8);
              ctx.scale(glitchScale, 1 / glitchScale);
            }
            
            var orbGradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius * 1.5);
            orbGradient.addColorStop(0, 'hsla(' + (hue + 10) + ', 100%, 95%, 0.9)');
            orbGradient.addColorStop(0.2, 'hsla(' + (hue + 20) + ', 90%, 80%, 0.7)');
            orbGradient.addColorStop(0.5, 'hsla(' + hue + ', 70%, 50%, 0.4)');
            orbGradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
            
            ctx.fillStyle = orbGradient;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            var centerRadius = radius * 0.3;
            ctx.fillStyle = 'hsla(' + (hue + 20) + ', 100%, 95%, 0.8)';
            ctx.beginPath();
            ctx.arc(centerX, centerY, centerRadius, 0, Math.PI * 2);
            ctx.fill();
            
            if (shouldGlitch) {
              ctx.globalCompositeOperation = 'screen';
              ctx.fillStyle = 'hsla(100, 100%, 50%, ' + (0.6 * glitchIntensity) + ')';
              ctx.beginPath();
              ctx.arc(centerX + glitchOffset * 0.5, centerY, centerRadius, 0, Math.PI * 2);
              ctx.fill();
              ctx.fillStyle = 'hsla(240, 100%, 50%, ' + (0.5 * glitchIntensity) + ')';
              ctx.beginPath();
              ctx.arc(centerX - glitchOffset * 0.5, centerY, centerRadius, 0, Math.PI * 2);
              ctx.fill();
              ctx.globalCompositeOperation = 'source-over';
              
              ctx.strokeStyle = 'rgba(255, 255, 255, ' + (0.6 * glitchIntensity) + ')';
              ctx.lineWidth = 1;
              for (var i = 0; i < 5; i++) {
                var y = centerY - radius + (Math.random() * radius * 2);
                var startX = centerX - radius + Math.random() * 20;
                var endX = centerX + radius - Math.random() * 20;
                ctx.beginPath();
                ctx.moveTo(startX, y);
                ctx.lineTo(endX, y);
                ctx.stroke();
              }
              
              ctx.fillStyle = 'rgba(255, 0, 255, ' + (0.4 * glitchIntensity) + ')';
              for (var i = 0; i < 3; i++) {
                var blockX = centerX - radius + Math.random() * radius * 2;
                var blockY = centerY - radius + Math.random() * radius * 2;
                var blockSize = Math.random() * 10 + 2;
                ctx.fillRect(blockX, blockY, blockSize, blockSize);
              }
            }
            
            ctx.strokeStyle = 'hsla(' + (hue + 20) + ', 80%, 70%, 0.6)';
            ctx.lineWidth = 2;
            if (shouldGlitch) {
              var segments = 8;
              for (var i = 0; i < segments; i++) {
                var startAngle = (i / segments) * Math.PI * 2;
                var endAngle = ((i + 1) / segments) * Math.PI * 2;
                var ringRadius = radius * 1.2 + (Math.random() - 0.5) * 10 * glitchIntensity;
                ctx.beginPath();
                ctx.arc(centerX, centerY, ringRadius, startAngle, endAngle);
                ctx.stroke();
              }
            } else {
              ctx.beginPath();
              ctx.arc(centerX, centerY, radius * 1.2, 0, Math.PI * 2);
              ctx.stroke();
            }
            
            if (shouldGlitch && Math.random() < 0.3) {
              ctx.globalCompositeOperation = 'difference';
              ctx.fillStyle = 'rgba(255, 255, 255, ' + (0.8 * glitchIntensity) + ')';
              for (var i = 0; i < 3; i++) {
                var barY = centerY - radius + Math.random() * radius * 2;
                var barHeight = Math.random() * 5 + 1;
                ctx.fillRect(centerX - radius, barY, radius * 2, barHeight);
              }
              ctx.globalCompositeOperation = 'source-over';
            }
            ctx.restore();
          };

          var time = 0;
          var frameId = 0;

          function render() {
            // Self-cleanup loop
            if (!doc.getElementById('artificial-hero-container')) {
              cancelAnimationFrame(frameId);
              trigger.kill();
              htmlEl.classList.remove('swdm-home-active');
              return;
            }

            time += 0.016;
            var width = canvas.offsetWidth;
            var height = canvas.offsetHeight;
            if (width <= 0 || height <= 0) {
              width = win.innerWidth;
              height = win.innerHeight;
            }
            if (width <= 0) width = 800;
            if (height <= 0) height = 600;

            canvas.width = grainCanvas.width = width;
            canvas.height = grainCanvas.height = height;

            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, width, height);

            var centerX = width / 2;
            var centerY = height / 2;
            var radius = Math.min(width, height) * 0.2;

            // Atmospheric background
            var bgGradient = ctx.createRadialGradient(centerX, centerY - 50, 0, centerX, centerY, Math.max(width, height) * 0.8);
            var hue = 180 + params.atmosphereShift * 60;
            bgGradient.addColorStop(0, 'hsla(' + (hue + 40) + ', 80%, 60%, 0.4)');
            bgGradient.addColorStop(0.3, 'hsla(' + hue + ', 60%, 40%, 0.3)');
            bgGradient.addColorStop(0.6, 'hsla(' + (hue - 20) + ', 40%, 20%, 0.2)');
            bgGradient.addColorStop(1, 'rgba(0, 0, 0, 0.9)');
            ctx.fillStyle = bgGradient;
            ctx.fillRect(0, 0, width, height);

            drawGlitchedOrb(centerX, centerY, radius, hue, time, params.glitchIntensity);

            // ASCII sphere particles
            ctx.font = '10px "JetBrains Mono", monospace';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';

            var spacing = 9;
            var cols = Math.floor(width / spacing);
            var rows = Math.floor(height / spacing);

            for (var i = 0; i < cols && i < 150; i++) {
              for (var j = 0; j < rows && j < 100; j++) {
                var x = (i - cols / 2) * spacing + centerX;
                var y = (j - rows / 2) * spacing + centerY;
                var dx = x - centerX;
                var dy = y - centerY;
                var dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < radius && Math.random() > 0.4) {
                  var z = Math.sqrt(Math.max(0, radius * radius - dx * dx - dy * dy));
                  var angle = params.rotation;
                  var rotZ = dx * Math.sin(angle) + z * Math.cos(angle);
                  var brightness = (rotZ + radius) / (radius * 2);

                  if (rotZ > -radius * 0.3) {
                    var charIndex = Math.floor(brightness * (density.length - 1));
                    var char = density[charIndex];

                    if (dist < radius * 0.8 && params.glitchIntensity > 0.8 && Math.random() < 0.3) {
                      var glitchChars = ['█', '▓', '▒', '░', '▄', '▀', '■', '□'];
                      char = glitchChars[Math.floor(Math.random() * glitchChars.length)];
                    }

                    var alpha = Math.max(0.2, brightness);
                    ctx.fillStyle = 'rgba(255, 255, 255, ' + alpha + ')';
                    ctx.fillText(char, x, y);
                  }
                }
              }
            }

            // Film grain rendering
            grainCtx.clearRect(0, 0, width, height);
            var grainIntensity = 0.22 + Math.sin(time * 10) * 0.03;
            var grainImageData = generateFilmGrain(width, height, grainIntensity);
            grainCtx.putImageData(grainImageData, 0, 0);

            if (params.glitchIntensity > 0.5) {
              grainCtx.globalCompositeOperation = 'screen';
              for (var gi = 0; gi < 200; gi++) {
                var gx = Math.random() * width;
                var gy = Math.random() * height;
                var gsize = Math.random() * 3 + 0.5;
                var gopacity = Math.random() * 0.5 * params.glitchIntensity;
                grainCtx.fillStyle = 'rgba(255, 255, 255, ' + gopacity + ')';
                grainCtx.beginPath();
                grainCtx.arc(gx, gy, gsize, 0, Math.PI * 2);
                grainCtx.fill();
              }
            }

            grainCtx.globalCompositeOperation = 'screen';
            for (var gi2 = 0; gi2 < 100; gi2++) {
              var gx2 = Math.random() * width;
              var gy2 = Math.random() * height;
              var gsize2 = Math.random() * 2 + 0.5;
              var gopacity2 = Math.random() * 0.3;
              grainCtx.fillStyle = 'rgba(255, 255, 255, ' + gopacity2 + ')';
              grainCtx.beginPath();
              grainCtx.arc(gx2, gy2, gsize2, 0, Math.PI * 2);
              grainCtx.fill();
            }

            grainCtx.globalCompositeOperation = 'multiply';
            for (var gi3 = 0; gi3 < 50; gi3++) {
              var gx3 = Math.random() * width;
              var gy3 = Math.random() * height;
              var gsize3 = Math.random() * 1.5 + 0.5;
              var gopacity3 = Math.random() * 0.5 + 0.5;
              grainCtx.fillStyle = 'rgba(0, 0, 0, ' + gopacity3 + ')';
              grainCtx.beginPath();
              grainCtx.arc(gx3, gy3, gsize3, 0, Math.PI * 2);
              grainCtx.fill();
            }

            frameId = requestAnimationFrame(render);
          }

          render();
        }

        function setupLoader() {
          if (win.gsap && win.ScrollTrigger) {
            var observeHero = function() {
              var container = doc.getElementById('artificial-hero-container');
              if (container && !container.dataset.swdmHeroActive) {
                container.dataset.swdmHeroActive = '1';
                initHero(container);
              }
            };

            var observer = new MutationObserver(observeHero);
            observer.observe(doc.body, { childList: true, subtree: true });
            observeHero();
          } else {
            loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js', function() {
              loadScript('https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/ScrollTrigger.min.js', function() {
                win.gsap.registerPlugin(win.ScrollTrigger);
                setupLoader();
              });
            });
          }
        }

        setupLoader();

      } catch (err) {
        if (win.onerror) win.onerror(err.message, '', 0, 0, err);
      }
    })();
    </script>
    """, height=0, width=0)
