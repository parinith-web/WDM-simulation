from __future__ import annotations

from ui.components.html import html_block


def render_home_section() -> None:
    html_block("""
    <style>
        .swdm-page-wrap {
            animation: swdm-enter 500ms cubic-bezier(.22,1,.36,1) both;
        }
        @keyframes swdm-enter {
            from { opacity: 0; transform: translateY(24px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .hero-3d-wrap {
            position: relative;
            width: 100%;
            min-height: 82vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        #threejs-canvas-container {
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
        }
        .hero-content {
            position: relative;
            z-index: 10;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 18px;
            padding: 0 24px;
            pointer-events: none;
        }
        .hero-badge {
            display: inline-block;
            border: 1px solid rgba(125, 220, 255, 0.35);
            border-radius: 999px;
            background: rgba(125, 220, 255, 0.08);
            color: #7ddcff;
            font-family: var(--font-mono, monospace);
            font-size: 10px;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            padding: 5px 16px;
            backdrop-filter: blur(12px);
        }
        .hero-h1 {
            font-family: var(--font-display, sans-serif) !important;
            font-size: clamp(32px, 5vw, 58px) !important;
            font-weight: 800 !important;
            line-height: 1.08 !important;
            color: #f4f7fb !important;
            margin: 0 !important;
            text-shadow: 0 0 60px rgba(125,220,255,0.22);
        }
        .hero-h1 span {
            background: linear-gradient(135deg, #7ddcff 0%, #6ea8ff 55%, #a8d8ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .hero-sub {
            color: rgba(169, 180, 194, 0.92);
            font-size: clamp(14px, 1.6vw, 17px);
            line-height: 1.65;
            max-width: 560px;
            margin: 0;
        }
        .hero-actions {
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            justify-content: center;
            pointer-events: all;
        }
        .cta-primary-3d {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 0;
            border-radius: var(--radius-sm, 8px);
            background: linear-gradient(135deg, #7ddcff, #6ea8ff);
            color: #080a0d !important;
            text-decoration: none !important;
            font-size: 13px;
            font-weight: 750;
            padding: 10px 24px;
            cursor: pointer;
            box-shadow: 0 8px 32px rgba(125,220,255,0.28);
            transition: transform 140ms ease, box-shadow 140ms ease;
        }
        .cta-primary-3d:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 40px rgba(125,220,255,0.38);
        }
        .cta-secondary-3d {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border: 1px solid rgba(125,220,255,0.3);
            border-radius: var(--radius-sm, 8px);
            background: rgba(125,220,255,0.07);
            color: #7ddcff !important;
            text-decoration: none !important;
            font-size: 13px;
            font-weight: 650;
            padding: 10px 24px;
            cursor: pointer;
            backdrop-filter: blur(12px);
            transition: transform 140ms ease, background 140ms ease, border-color 140ms ease;
        }
        .cta-secondary-3d:hover {
            transform: translateY(-2px);
            background: rgba(125,220,255,0.12);
            border-color: rgba(125,220,255,0.5);
        }
        .hero-stats {
            display: flex;
            gap: 32px;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 8px;
        }
        .hero-stat {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2px;
        }
        .hero-stat strong {
            color: #7ddcff;
            font-family: var(--font-display, sans-serif);
            font-size: 22px;
            font-weight: 800;
        }
        .hero-stat small {
            color: rgba(169,180,194,0.7);
            font-family: var(--font-mono, monospace);
            font-size: 9px;
            font-weight: 700;
            letter-spacing: .1em;
            text-transform: uppercase;
        }
        .drag-hint {
            position: absolute;
            bottom: 20px;
            right: 20px;
            z-index: 20;
            background: rgba(0,0,0,0.3);
            color: rgba(255,255,255,0.6);
            font-size: 11px;
            padding: 4px 12px;
            border-radius: 999px;
            backdrop-filter: blur(8px);
            transition: opacity 1s ease;
        }
    </style>

    <div class="swdm-page-wrap">
    <section class="hero-3d-wrap">
        <div id="threejs-canvas-container"></div>

        <div class="hero-content">
            <div class="hero-badge">Research-grade WDM security platform</div>
            <h1 class="hero-h1">Secure WDM<br><span>Optical Simulator</span></h1>
            <p class="hero-sub">
                Interactive simulation of RC4-secured WDM optical communication.
                Analyze fiber dispersion, amplification, encryption penalties,
                and signal quality metrics in real-time.
            </p>
            <div class="hero-actions">
                <a href="?page=simulation" target="_self" class="cta-primary-3d">&#9655; Run Simulation</a>
                <a href="?page=theory" target="_self" class="cta-secondary-3d">&#9670; View Theory</a>
            </div>
            <div class="hero-stats">
                <div class="hero-stat"><strong>80</strong><small>Gbps total</small></div>
                <div class="hero-stat"><strong>8</strong><small>WDM channels</small></div>
                <div class="hero-stat"><strong>1e-9</strong><small>BER target</small></div>
                <div class="hero-stat"><strong>100+</strong><small>km reach</small></div>
            </div>
        </div>

        <div class="drag-hint" id="drag-hint">Drag to explore</div>
    </section>
    </div>

    <script>
    (function() {
        // Wait for THREE.js to be ready - we'll load it dynamically
        function loadScript(src, cb) {
            var s = document.createElement('script');
            s.src = src;
            s.onload = cb;
            document.head.appendChild(s);
        }

        function initScene() {
            var THREE = window.THREE;
            var container = document.getElementById('threejs-canvas-container');
            if (!container || !THREE) return;

            var W = container.offsetWidth || window.innerWidth;
            var H = container.offsetHeight || window.innerHeight;

            // Scene
            var scene = new THREE.Scene();
            var camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 2000);
            camera.position.set(0, 0, 22);

            var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
            renderer.setSize(W, H);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.setClearColor(0x000000, 0);
            container.appendChild(renderer.domElement);

            // Stars
            var starsGeo = new THREE.BufferGeometry();
            var starCount = 6000;
            var starPos = new Float32Array(starCount * 3);
            for (var i = 0; i < starCount; i++) {
                starPos[i*3]   = (Math.random()-0.5)*1200;
                starPos[i*3+1] = (Math.random()-0.5)*1200;
                starPos[i*3+2] = (Math.random()-0.5)*1200;
            }
            starsGeo.setAttribute('position', new THREE.BufferAttribute(starPos, 3));
            var starsMat = new THREE.PointsMaterial({ color: 0xaaccff, size: 0.5, sizeAttenuation: true, transparent: true, opacity: 0.6 });
            scene.add(new THREE.Points(starsGeo, starsMat));

            // Helper: create a globe node
            function makeGlobe(radius, pos, wireColor, glowColor, opacity) {
                var g = new THREE.Group();
                g.position.set(pos[0], pos[1], pos[2]);

                // Core sphere
                var coreGeo = new THREE.SphereGeometry(radius * 0.88, 48, 48);
                var coreMat = new THREE.MeshPhongMaterial({
                    color: new THREE.Color(wireColor).multiplyScalar(0.18),
                    transparent: true, opacity: 0.85,
                    shininess: 60
                });
                g.add(new THREE.Mesh(coreGeo, coreMat));

                // Wireframe overlay
                var wfGeo = new THREE.SphereGeometry(radius, 28, 28);
                var wfMat = new THREE.MeshBasicMaterial({
                    color: wireColor, wireframe: true, transparent: true, opacity: opacity
                });
                g.add(new THREE.Mesh(wfGeo, wfMat));

                // Glow ring (torus)
                var ringGeo = new THREE.TorusGeometry(radius * 1.15, radius * 0.04, 16, 80);
                var ringMat = new THREE.MeshBasicMaterial({ color: glowColor, transparent: true, opacity: 0.45 });
                var ring = new THREE.Mesh(ringGeo, ringMat);
                ring.rotation.x = Math.PI / 2;
                g.add(ring);

                // Atmosphere shader
                var atmGeo = new THREE.SphereGeometry(radius * 1.18, 32, 32);
                var atmMat = new THREE.ShaderMaterial({
                    vertexShader: `
                        varying vec3 vNormal;
                        void main() {
                            vNormal = normalize(normalMatrix * normal);
                            gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
                        }
                    `,
                    fragmentShader: `
                        uniform vec3 glowColor;
                        varying vec3 vNormal;
                        void main() {
                            float i = pow(0.65 - dot(vNormal, vec3(0,0,1)), 2.5);
                            gl_FragColor = vec4(glowColor, 1.0) * i;
                        }
                    `,
                    uniforms: { glowColor: { value: new THREE.Color(glowColor) } },
                    blending: THREE.AdditiveBlending,
                    side: THREE.BackSide,
                    transparent: true
                });
                g.add(new THREE.Mesh(atmGeo, atmMat));

                return g;
            }

            // Main central globe (large)
            var mainGlobe = makeGlobe(5.5, [0, 0, 0], 0x3a86ff, 0x3a86ff, 0.35);
            scene.add(mainGlobe);

            // Satellite globes (smaller, positioned around main)
            var satellites = [
                makeGlobe(2.2, [-11, 4, -4], 0x6ea8ff, 0x6ea8ff, 0.4),
                makeGlobe(1.8, [10, -3, -2], 0x7ddcff, 0x7ddcff, 0.45),
                makeGlobe(1.4, [-7, -6, 2], 0x2f6fed, 0x3a86ff, 0.38),
                makeGlobe(1.2, [8, 7, -5], 0x5bb8ff, 0x5bb8ff, 0.42),
            ];
            satellites.forEach(function(s) { scene.add(s); });

            // Light beams between globes
            function makeBeam(from, to, color) {
                var dir = new THREE.Vector3(to[0]-from[0], to[1]-from[1], to[2]-from[2]);
                var len = dir.length();
                var mid = [(from[0]+to[0])/2, (from[1]+to[1])/2, (from[2]+to[2])/2];
                var geo = new THREE.CylinderGeometry(0.025, 0.025, len, 8);
                var mat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.25 });
                var mesh = new THREE.Mesh(geo, mat);
                mesh.position.set(mid[0], mid[1], mid[2]);
                var axis = new THREE.Vector3(0, 1, 0);
                var dirN = dir.clone().normalize();
                mesh.quaternion.setFromUnitVectors(axis, dirN);
                return mesh;
            }

            var beamPositions = [
                [[0,0,0], [-11,4,-4], 0x6ea8ff],
                [[0,0,0], [10,-3,-2], 0x7ddcff],
                [[0,0,0], [-7,-6,2],  0x3a86ff],
                [[0,0,0], [8,7,-5],   0x5bb8ff],
            ];
            var beams = beamPositions.map(function(b) {
                var beam = makeBeam(b[0], b[1], b[2]);
                scene.add(beam);
                return beam;
            });

            // Photon particles traveling along beams
            var photons = [];
            var photonGeo = new THREE.SphereGeometry(0.12, 8, 8);

            function makePhoton(from, to, color, speed) {
                var mat = new THREE.MeshBasicMaterial({ color: color, transparent: true, opacity: 0.9 });
                var mesh = new THREE.Mesh(photonGeo, mat);
                var t = Math.random();
                mesh.position.set(
                    from[0] + (to[0]-from[0])*t,
                    from[1] + (to[1]-from[1])*t,
                    from[2] + (to[2]-from[2])*t
                );
                mesh.userData = { from: from, to: to, t: t, speed: speed, dir: Math.random() > 0.5 ? 1 : -1 };
                scene.add(mesh);
                return mesh;
            }

            for (var i = 0; i < beamPositions.length; i++) {
                for (var j = 0; j < 4; j++) {
                    photons.push(makePhoton(beamPositions[i][0], beamPositions[i][1], beamPositions[i][2], 0.004 + Math.random()*0.006));
                }
            }

            // Lights
            scene.add(new THREE.AmbientLight(0x1a2a4a, 2));
            var pLight = new THREE.PointLight(0x3a86ff, 3, 60);
            pLight.position.set(0, 0, 10);
            scene.add(pLight);
            var pLight2 = new THREE.PointLight(0x7ddcff, 1.5, 40);
            pLight2.position.set(-12, 8, 5);
            scene.add(pLight2);

            // Mouse drag rotate
            var isDragging = false, prevX = 0, prevY = 0;
            var rotVelX = 0, rotVelY = 0;
            renderer.domElement.addEventListener('mousedown', function(e) { isDragging = true; prevX = e.clientX; prevY = e.clientY; });
            window.addEventListener('mouseup', function() { isDragging = false; });
            window.addEventListener('mousemove', function(e) {
                if (!isDragging) return;
                var dx = e.clientX - prevX, dy = e.clientY - prevY;
                rotVelX += dy * 0.005; rotVelY += dx * 0.005;
                prevX = e.clientX; prevY = e.clientY;
            });
            renderer.domElement.addEventListener('touchstart', function(e) { isDragging = true; prevX = e.touches[0].clientX; prevY = e.touches[0].clientY; });
            window.addEventListener('touchend', function() { isDragging = false; });
            window.addEventListener('touchmove', function(e) {
                if (!isDragging) return;
                var dx = e.touches[0].clientX - prevX, dy = e.touches[0].clientY - prevY;
                rotVelX += dy * 0.005; rotVelY += dx * 0.005;
                prevX = e.touches[0].clientX; prevY = e.touches[0].clientY;
            });

            // Hide drag hint after 3s
            setTimeout(function() {
                var hint = document.getElementById('drag-hint');
                if (hint) hint.style.opacity = '0';
            }, 3000);

            // Pulse animation
            var clock = new THREE.Clock();
            var pivot = new THREE.Group();
            scene.add(pivot);
            beams.forEach(function(b) { pivot.add(b); });

            function animate() {
                requestAnimationFrame(animate);
                var t = clock.getElapsedTime();

                // Slow auto-rotation + inertia
                rotVelX *= 0.92; rotVelY *= 0.92;
                mainGlobe.rotation.y += 0.0015 + rotVelY;
                mainGlobe.rotation.x += rotVelX * 0.5;
                satellites.forEach(function(s, i) {
                    s.rotation.y += 0.002 + i * 0.0005;
                    s.rotation.x += 0.001;
                });
                pivot.rotation.y += 0.0008 + rotVelY * 0.5;

                // Pulsing glow on main globe
                var pulse = 0.3 + 0.12 * Math.sin(t * 1.5);
                if (mainGlobe.children[1] && mainGlobe.children[1].material) {
                    mainGlobe.children[1].material.opacity = pulse;
                }

                // Photon movement
                photons.forEach(function(ph) {
                    ph.userData.t += ph.userData.speed * ph.userData.dir;
                    if (ph.userData.t > 1) { ph.userData.t = 0; ph.userData.dir = 1; }
                    if (ph.userData.t < 0) { ph.userData.t = 1; ph.userData.dir = -1; }
                    var f = ph.userData.from, to = ph.userData.to, tt = ph.userData.t;
                    ph.position.set(
                        f[0] + (to[0]-f[0])*tt,
                        f[1] + (to[1]-f[1])*tt,
                        f[2] + (to[2]-f[2])*tt
                    );
                    ph.material.opacity = 0.5 + 0.5 * Math.sin(t * 8 + tt * Math.PI * 2);
                });

                renderer.render(scene, camera);
            }
            animate();

            window.addEventListener('resize', function() {
                var W2 = container.offsetWidth || window.innerWidth;
                var H2 = container.offsetHeight || window.innerHeight;
                camera.aspect = W2 / H2;
                camera.updateProjectionMatrix();
                renderer.setSize(W2, H2);
            });
        }

        // Load Three.js from CDN
        if (window.THREE) {
            initScene();
        } else {
            loadScript('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js', initScene);
        }
    })();
    </script>
    """)
