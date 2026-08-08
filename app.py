# import sys
# import os

# # Add root directory to python path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# import streamlit as st
# import time
# from dotenv import load_dotenv
# from utils.audio_processor import process_input
# from core.transcriber import transcribe_all
# from core.summarizer import summarize, generate_title
# from core.extractor import extract_action_items, extract_key_decisions, extract_questions
# from core.rag_engine import build_rag_chain, ask_question

# load_dotenv()

# # ─── Page Config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Smart Video AI",
#     page_icon="🎬",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # ─── Custom CSS & Advanced Dynamic Styling ──────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

# /* ── Root Variables ── */
# :root {
#     --bg: #030305;
#     --surface: #0a0a0f;
#     --surface-2: #12121a;
#     --border: #222233;
#     --border-hover: #ff6a00;
#     --accent: #ff6a00;
#     --accent-glow: #ff9d3d;
#     --accent-2: #ff0055;
#     --text: #f0f0f5;
#     --text-muted: #8888a0;
#     --success: #10b981;
#     --warning: #f59e0b;
#     --danger: #ef4444;
# }

# /* ── Global Reset ── */
# html, body, [class*="css"] {
#     font-family: 'JetBrains Mono', monospace;
#     background-color: var(--bg) !important;
#     color: var(--text) !important;
# }

# .stApp {
#     background: var(--bg) !important;
# }

# /* Dynamic Animated Grid Overlay */
# .stApp::before {
#     content: '';
#     position: fixed;
#     top: 0; left: 0;
#     width: 100vw; height: 100vh;
#     background-image:
#         linear-gradient(rgba(255, 106, 0, 0.05) 1px, transparent 1px),
#         linear-gradient(90deg, rgba(255, 106, 0, 0.05) 1px, transparent 1px);
#     background-size: 50px 50px;
#     pointer-events: none;
#     z-index: 1;
#     animation: gridDrift 20s linear infinite;
# }

# @keyframes gridDrift {
#     0%   { background-position: 0 0, 0 0; }
#     100% { background-position: 50px 50px, 50px 50px; }
# }

# /* Cursor-following CSS Glow Light */
# #cursorGlow {
#     position: fixed;
#     top: 0; left: 0;
#     width: 600px; height: 600px;
#     margin-left: -300px;
#     margin-top: -300px;
#     background: radial-gradient(circle, rgba(255, 106, 0, 0.12) 0%, rgba(255, 0, 85, 0.06) 40%, transparent 70%);
#     border-radius: 50%;
#     pointer-events: none;
#     z-index: 1;
#     transition: transform 0.15s ease-out;
#     mix-blend-mode: screen;
# }

# /* ── Sidebar Styling ── */
# [data-testid="stSidebar"] {
#     background: rgba(10, 10, 15, 0.85) !important;
#     backdrop-filter: blur(12px) !important;
#     border-right: 1px solid var(--border) !important;
#     z-index: 10 !important;
# }

# [data-testid="stSidebar"] * {
#     color: var(--text) !important;
# }

# /* ── Headings ── */
# h1, h2, h3, h4, h5, h6 {
#     font-family: 'Syne', sans-serif !important;
#     color: var(--text) !important;
# }

# /* ── Hero Animated Title ── */
# .hero-title {
#     font-family: 'Syne', sans-serif;
#     font-size: clamp(2.2rem, 5vw, 3.8rem);
#     font-weight: 800;
#     line-height: 1.1;
#     margin: 0;
#     background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 40%, var(--accent-2) 100%);
#     background-size: 200% 200%;
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     animation: shimmer 5s ease-in-out infinite;
#     text-shadow: 0 0 30px rgba(255,106,0,0.3);
# }

# @keyframes shimmer {
#     0%   { background-position: 0% 50%; }
#     50%  { background-position: 100% 50%; }
#     100% { background-position: 0% 50%; }
# }

# .hero-sub {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.8rem;
#     color: var(--text-muted);
#     letter-spacing: 0.25em;
#     text-transform: uppercase;
#     margin-top: 0.5rem;
#     opacity: 0;
#     animation: fadeInUp 0.8s ease forwards 0.2s;
# }

# @keyframes fadeInUp {
#     from { opacity: 0; transform: translateY(16px); }
#     to   { opacity: 1; transform: translateY(0); }
# }

# /* ── Modern 3D Interactive Cards ── */
# .card {
#     background: rgba(10, 10, 15, 0.75);
#     backdrop-filter: blur(10px);
#     border: 1px solid var(--border);
#     border-radius: 14px;
#     padding: 1.5rem;
#     margin-bottom: 1rem;
#     position: relative;
#     overflow: hidden;
#     transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s ease, box-shadow 0.3s ease;
#     opacity: 0;
#     animation: fadeInUp 0.6s ease forwards;
#     transform-style: preserve-3d;
# }

# .card:hover {
#     border-color: var(--accent);
#     transform: translateY(-6px) scale(1.015) rotateX(2deg) rotateY(-1deg);
#     box-shadow: 0 15px 35px rgba(255, 106, 0, 0.25), 0 0 20px rgba(255, 0, 85, 0.15);
# }

# .card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0;
#     width: 4px; height: 100%;
#     background: linear-gradient(180deg, var(--accent), var(--accent-2));
#     transition: width 0.3s ease, box-shadow 0.3s ease;
# }

# .card:hover::before {
#     width: 6px;
#     box-shadow: 0 0 16px var(--accent-glow);
# }

# /* Card Scanline Reflection Effect */
# .card::after {
#     content: '';
#     position: absolute;
#     top: -100%; left: -100%;
#     width: 300%; height: 300%;
#     background: linear-gradient(135deg, transparent 45%, rgba(255, 255, 255, 0.08) 50%, transparent 55%);
#     transition: transform 0.8s ease;
#     pointer-events: none;
# }

# .card:hover::after {
#     transform: translate(50%, 50%);
# }

# .card-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 0.75rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     color: var(--text-muted);
#     margin-bottom: 0.75rem;
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
#     transition: color 0.3s ease;
# }

# .card:hover .card-title {
#     color: var(--accent-glow);
# }

# .card-content {
#     font-size: 0.875rem;
#     line-height: 1.7;
#     color: var(--text);
# }

# /* ── Badges ── */
# .badge {
#     display: inline-block;
#     padding: 0.25rem 0.7rem;
#     border-radius: 6px;
#     font-size: 0.65rem;
#     font-weight: 600;
#     letter-spacing: 0.1em;
#     text-transform: uppercase;
#     transition: all 0.3s ease;
# }

# .badge:hover {
#     transform: translateY(-3px) scale(1.05);
# }

# .badge-purple { background: rgba(255,106,0,0.18); color: var(--accent-glow); border: 1px solid rgba(255,106,0,0.4); }
# .badge-cyan   { background: rgba(255,0,85,0.18);  color: var(--accent-2);    border: 1px solid rgba(255,0,85,0.4); }
# .badge-green  { background: rgba(16,185,129,0.18); color: var(--success);    border: 1px solid rgba(16,185,129,0.4); }

# .badge-purple:hover { box-shadow: 0 0 15px rgba(255,106,0,0.5); }
# .badge-cyan:hover   { box-shadow: 0 0 15px rgba(255,0,85,0.5); }
# .badge-green:hover  { box-shadow: 0 0 15px rgba(16,185,129,0.5); }

# /* ── Inputs & Futuristic Buttons ── */
# .stTextInput > div > div > input,
# .stSelectbox > div > div {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
#     border-radius: 8px !important;
#     color: var(--text) !important;
#     font-family: 'JetBrains Mono', monospace !important;
#     transition: all 0.3s ease !important;
# }

# .stTextInput > div > div > input:hover {
#     border-color: rgba(255,106,0,0.6) !important;
#     box-shadow: 0 0 12px rgba(255,106,0,0.15) !important;
# }

# .stTextInput > div > div > input:focus {
#     border-color: var(--accent) !important;
#     box-shadow: 0 0 15px rgba(255,106,0,0.3) !important;
# }

# .stButton > button {
#     background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
#     color: #ffffff !important;
#     border: none !important;
#     border-radius: 8px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 800 !important;
#     font-size: 0.875rem !important;
#     letter-spacing: 0.08em !important;
#     padding: 0.7rem 1.6rem !important;
#     transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
#     text-transform: uppercase !important;
#     position: relative;
#     overflow: hidden;
#     box-shadow: 0 4px 15px rgba(255, 106, 0, 0.3) !important;
# }

# .stButton > button::before {
#     content: '';
#     position: absolute;
#     top: 0; left: -100%;
#     width: 60%; height: 100%;
#     background: linear-gradient(120deg, transparent, rgba(255,255,255,0.4), transparent);
#     transform: skewX(-20deg);
#     transition: left 0.6s ease;
# }

# .stButton > button:hover::before {
#     left: 140%;
# }

# .stButton > button:hover {
#     transform: translateY(-3px) scale(1.03) !important;
#     box-shadow: 0 10px 30px rgba(255, 106, 0, 0.5), 0 0 25px rgba(255, 0, 85, 0.4) !important;
# }

# .stButton > button:active {
#     transform: translateY(0) scale(0.97) !important;
# }

# /* Secondary Button */
# .stButton > button[kind="secondary"] {
#     background: var(--surface-2) !important;
#     border: 1px solid var(--border) !important;
#     color: var(--text) !important;
#     box-shadow: none !important;
# }

# .stButton > button[kind="secondary"]:hover {
#     border-color: var(--accent) !important;
#     box-shadow: 0 6px 20px rgba(255,106,0,0.25) !important;
# }

# /* ── Progress & Status Bars ── */
# .status-bar {
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     padding: 0.8rem 1.1rem;
#     background: var(--surface-2);
#     border-radius: 10px;
#     margin: 0.4rem 0;
#     border: 1px solid var(--border);
#     font-size: 0.8rem;
#     transition: all 0.3s ease;
# }

# .status-bar:hover {
#     border-color: rgba(255,106,0,0.5);
#     transform: translateX(5px);
#     box-shadow: 0 4px 15px rgba(0,0,0,0.5);
# }

# .status-dot {
#     width: 9px; height: 9px;
#     border-radius: 50%;
#     flex-shrink: 0;
# }

# .dot-active   { background: var(--accent-glow); box-shadow: 0 0 10px var(--accent-glow); animation: pulse 1.2s infinite; }
# .dot-done     { background: var(--success); box-shadow: 0 0 8px var(--success); }
# .dot-pending  { background: var(--border); }

# @keyframes pulse {
#     0%, 100% { opacity: 1; transform: scale(1); }
#     50%       { opacity: 0.3; transform: scale(0.85); }
# }

# /* ── Chat Display ── */
# .chat-container {
#     background: rgba(10, 10, 15, 0.8);
#     backdrop-filter: blur(10px);
#     border: 1px solid var(--border);
#     border-radius: 14px;
#     padding: 1.25rem;
#     max-height: 420px;
#     overflow-y: auto;
#     margin-bottom: 1rem;
# }

# .chat-msg {
#     margin-bottom: 1rem;
#     display: flex;
#     flex-direction: column;
#     gap: 0.2rem;
#     opacity: 0;
#     animation: fadeInUp 0.4s ease forwards;
# }

# .chat-label {
#     font-size: 0.65rem;
#     font-weight: 700;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
# }

# .chat-bubble {
#     display: inline-block;
#     padding: 0.75rem 1.1rem;
#     border-radius: 12px;
#     font-size: 0.85rem;
#     line-height: 1.6;
#     max-width: 88%;
#     transition: all 0.25s ease;
# }

# .chat-bubble:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 8px 22px rgba(255,106,0,0.2);
# }

# .user-label  { color: var(--accent-glow); }
# .bot-label   { color: var(--accent-2); }

# .user-bubble { background: rgba(255,106,0,0.15); border: 1px solid rgba(255,106,0,0.3); align-self: flex-end; }
# .bot-bubble  { background: rgba(255,0,85,0.1);    border: 1px solid rgba(255,0,85,0.25);  align-self: flex-start; }

# /* ── Transcript Box ── */
# .transcript-box {
#     background: var(--surface-2);
#     border: 1px solid var(--border);
#     border-radius: 10px;
#     padding: 1.25rem;
#     font-size: 0.82rem;
#     line-height: 1.8;
#     max-height: 300px;
#     overflow-y: auto;
#     color: var(--text-muted);
#     white-space: pre-wrap;
#     word-break: break-word;
#     transition: border-color 0.3s ease;
# }

# .transcript-box:hover {
#     border-color: rgba(255,106,0,0.4);
# }

# /* Scrollbar Styling */
# ::-webkit-scrollbar { width: 6px; height: 6px; }
# ::-webkit-scrollbar-track { background: var(--bg); }
# ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: var(--accent); }

# /* Staggered card entrance delays */
# .card:nth-of-type(1) { animation-delay: 0.05s; }
# .card:nth-of-type(2) { animation-delay: 0.12s; }
# .card:nth-of-type(3) { animation-delay: 0.19s; }
# .card:nth-of-type(4) { animation-delay: 0.26s; }
# </style>

# <!-- Cursor Following Background Spotlight -->
# <div id="cursorGlow"></div>
# """, unsafe_allow_html=True)

# # ─── 3D Interactive WebGL Scene (Three.js with Raycasting Hover & Dynamic Lighting) ───
# st.markdown("""
# <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

# <canvas id="bg3dCanvas" style="
#     position: fixed;
#     top: 0; left: 0;
#     width: 100vw; height: 100vh;
#     pointer-events: auto;
#     z-index: 0;
#     opacity: 0.75;
# "></canvas>

# <script>
# (function() {
#     if (window.__three3DInit) return;
#     window.__three3DInit = true;

#     const canvas = document.getElementById('bg3dCanvas');
#     const cursorGlow = document.getElementById('cursorGlow');
#     if (!canvas) return;

#     // 1. Scene, Camera, WebGL Renderer
#     const scene = new THREE.Scene();
#     const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
#     camera.position.z = 24;

#     const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
#     renderer.setSize(window.innerWidth, window.innerHeight);
#     renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

#     // 2. Dynamic Lighting Engine
#     const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
#     scene.add(ambientLight);

#     // Point Light that directly tracks the user cursor in 3D Space
#     const cursorLight = new THREE.PointLight(0xff6a00, 2.5, 50);
#     scene.add(cursorLight);

#     const backLight = new THREE.PointLight(0xff0055, 1.8, 40);
#     backLight.position.set(-15, -10, -10);
#     scene.add(backLight);

#     // 3. 3D Model: Torus Knot Mesh Wireframe
#     const group = new THREE.Group();
#     scene.add(group);

#     const knotGeometry = new THREE.TorusKnotGeometry(6.5, 2.0, 140, 18);
#     const knotMaterial = new THREE.MeshStandardMaterial({
#         color: 0xff6a00,
#         wireframe: true,
#         roughness: 0.2,
#         metalness: 0.8,
#         emissive: 0x331100,
#         transparent: true,
#         opacity: 0.35
#     });
#     const torusKnot = new THREE.Mesh(knotGeometry, knotMaterial);
#     group.add(torusKnot);

#     // Floating Interactive Particle Stars Field
#     const particleCount = 800;
#     const particleGeo = new THREE.BufferGeometry();
#     const positions = new Float32Array(particleCount * 3);
#     const initialY = new Float32Array(particleCount);

#     for (let i = 0; i < particleCount; i++) {
#         const idx = i * 3;
#         positions[idx]     = (Math.random() - 0.5) * 70;
#         positions[idx + 1] = (Math.random() - 0.5) * 70;
#         positions[idx + 2] = (Math.random() - 0.5) * 70;
#         initialY[i] = positions[idx + 1];
#     }

#     particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
#     const particleMat = new THREE.PointsMaterial({
#         color: 0xff9d3d,
#         size: 0.18,
#         transparent: true,
#         opacity: 0.65
#     });
#     const particles = new THREE.Points(particleGeo, particleMat);
#     group.add(particles);

#     // 4. Mouse Tracking & Raycasting Setup
#     const raycaster = new THREE.Raycaster();
#     const mouse2D = new THREE.Vector2(-100, -100);
#     let targetX = 0, targetY = 0;
#     let isHovered = false;

#     window.addEventListener('mousemove', (e) => {
#         // Update 2D Normalized Coordinates for Raycasting
#         mouse2D.x = (e.clientX / window.innerWidth) * 2 - 1;
#         mouse2D.y = -(e.clientY / window.innerHeight) * 2 + 1;

#         targetX = mouse2D.x * 0.8;
#         targetY = mouse2D.y * 0.8;

#         // Update Cursor Following Glow Spotlight
#         if (cursorGlow) {
#             cursorGlow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
#         }

#         // Map 2D Cursor to 3D Space for Cursor Point Light
#         cursorLight.position.x = mouse2D.x * 15;
#         cursorLight.position.y = mouse2D.y * 15;
#         cursorLight.position.z = 10;
#     });

#     window.addEventListener('resize', () => {
#         camera.aspect = window.innerWidth / window.innerHeight;
#         camera.updateProjectionMatrix();
#         renderer.setSize(window.innerWidth, window.innerHeight);
#     });

#     // 5. Animation Render Loop
#     let clock = new THREE.Clock();

#     function animate() {
#         requestAnimationFrame(animate);

#         const elapsedTime = clock.getElapsedTime();

#         // Wave motion for particles
#         const posAttr = particleGeo.attributes.position;
#         for (let i = 0; i < particleCount; i++) {
#             const idx = i * 3;
#             posAttr.array[idx + 1] = initialY[i] + Math.sin(elapsedTime * 1.5 + posAttr.array[idx]) * 0.8;
#         }
#         posAttr.needsUpdate = true;

#         // Raycasting for 3D Model Hover Detection
#         raycaster.setFromCamera(mouse2D, camera);
#         const intersects = raycaster.intersectObject(torusKnot);

#         if (intersects.length > 0) {
#             if (!isHovered) {
#                 isHovered = true;
#                 // Color morph on hover: Neon Orange -> Electric Magenta
#                 torusKnot.material.color.setHex(0xff0055);
#                 torusKnot.material.emissive.setHex(0xaa0033);
#                 torusKnot.material.opacity = 0.75;
#                 cursorLight.color.setHex(0xff0055);
#             }
#         } else {
#             if (isHovered) {
#                 isHovered = false;
#                 // Revert color back on exit
#                 torusKnot.material.color.setHex(0xff6a00);
#                 torusKnot.material.emissive.setHex(0x331100);
#                 torusKnot.material.opacity = 0.35;
#                 cursorLight.color.setHex(0xff6a00);
#             }
#         }

#         // Smooth Physics Rotation & Spring Interpolation
#         const speedMultiplier = isHovered ? 2.5 : 1.0;
#         group.rotation.x += 0.002 * speedMultiplier;
#         group.rotation.y += 0.003 * speedMultiplier;

#         // Smooth Mouse Rotation Tilting
#         group.rotation.y += (targetX - group.rotation.y) * 0.03;
#         group.rotation.x += (-targetY - group.rotation.x) * 0.03;

#         // Pulsing Mesh Scale Effect on Hover
#         const targetScale = isHovered ? 1.15 : 1.0;
#         torusKnot.scale.x += (targetScale - torusKnot.scale.x) * 0.05;
#         torusKnot.scale.y += (targetScale - torusKnot.scale.y) * 0.05;
#         torusKnot.scale.z += (targetScale - torusKnot.scale.z) * 0.05;

#         renderer.render(scene, camera);
#     }

#     animate();
# })();
# </script>
# """, unsafe_allow_html=True)

# # ─── Session State Init ──────────────────────────────────────────────────────────
# for key, default in {
#     "result": None,
#     "chat_history": [],
#     "processing": False,
#     "pipeline_done": False,
#     "pipeline_steps": {},
# }.items():
#     if key not in st.session_state:
#         st.session_state[key] = default

# # ─── Helpers ────────────────────────────────────────────────────────────────────
# def step_status(steps: dict, key: str) -> str:
#     s = steps.get(key, "pending")
#     if s == "active":  return "dot-active"
#     if s == "done":    return "dot-done"
#     return "dot-pending"

# def render_step_bar(label: str, key: str, icon: str):
#     css = step_status(st.session_state.pipeline_steps, key)
#     st.markdown(f"""
#     <div class="status-bar">
#         <div class="status-dot {css}"></div>
#         <span>{icon} {label}</span>
#     </div>""", unsafe_allow_html=True)

# # ─── Sidebar ────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown('<div class="hero-title" style="font-size:1.6rem">🎬 Smart Video<br>AI</div>', unsafe_allow_html=True)
#     st.markdown('<div class="hero-sub">Meeting Intelligence</div>', unsafe_allow_html=True)
#     st.markdown("---")

#     st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
#     source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

#     language = st.selectbox("Language", ["english", "hinglish"], index=0)

#     run_btn = st.button("⚡  Analyse", use_container_width=True)

#     if st.session_state.pipeline_done:
#         st.markdown("---")
#         st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
#         for step, icon, label in [
#             ("audio",      "🔊", "Audio Processing"),
#             ("transcript", "📝", "Transcription"),
#             ("title",      "🏷️", "Title Generation"),
#             ("summary",    "📋", "Summarisation"),
#             ("extract",    "🔍", "Extraction"),
#             ("rag",        "🧠", "RAG Engine"),
#         ]:
#             render_step_bar(label, step, icon)

# # ─── Main Area ──────────────────────────────────────────────────────────────────
# st.markdown('<div class="hero-title">Smart Video AI</div>', unsafe_allow_html=True)
# st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>', unsafe_allow_html=True)
# st.markdown("---")

# # ── Run Pipeline ────────────────────────────────────────────────────────────────
# if run_btn:
#     if not source.strip():
#         st.error("Please enter a YouTube URL or file path.")
#     else:
#         st.session_state.pipeline_done = False
#         st.session_state.result = None
#         st.session_state.chat_history = []
#         st.session_state.pipeline_steps = {}

#         progress_placeholder = st.empty()

#         def update_step(key, state):
#             st.session_state.pipeline_steps[key] = state

#         try:
#             with progress_placeholder.container():
#                 st.info("⚙️ Pipeline running — see sidebar for live status…")

#             update_step("audio", "active")
#             chunks = process_input(source)
#             update_step("audio", "done")

#             update_step("transcript", "active")
#             transcript = transcribe_all(chunks, language)
#             update_step("transcript", "done")

#             update_step("title", "active")
#             title = generate_title(transcript)
#             update_step("title", "done")

#             update_step("summary", "active")
#             summary = summarize(transcript)
#             update_step("summary", "done")

#             update_step("extract", "active")
#             action_items  = extract_action_items(transcript)
#             decisions     = extract_key_decisions(transcript)
#             questions     = extract_questions(transcript)
#             update_step("extract", "done")

#             update_step("rag", "active")
#             rag_chain = build_rag_chain(transcript)
#             update_step("rag", "done")

#             st.session_state.result = {
#                 "title": title,
#                 "transcript": transcript,
#                 "summary": summary,
#                 "action_items": action_items,
#                 "key_decisions": decisions,
#                 "open_questions": questions,
#                 "rag_chain": rag_chain,
#             }
#             st.session_state.pipeline_done = True
#             progress_placeholder.success("✅ Analysis complete!")
#             time.sleep(0.5)
#             progress_placeholder.empty()
#             st.rerun()

#         except Exception as e:
#             for k in ["audio","transcript","title","summary","extract","rag"]:
#                 if st.session_state.pipeline_steps.get(k) == "active":
#                     st.session_state.pipeline_steps[k] = "pending"
#             progress_placeholder.error(f"❌ Error: {e}")

# # ── Results ──────────────────────────────────────────────────────────────────────
# if st.session_state.result:
#     r = st.session_state.result

#     # Title banner
#     st.markdown(f"""
#     <div class="card">
#         <div class="card-title">📌 Session Title</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
#             {r['title']}
#         </div>
#     </div>""", unsafe_allow_html=True)

#     # Top row: summary + transcript
#     col1, col2 = st.columns([3, 2], gap="medium")

#     with col1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">📋 Summary</div>
#             <div class="card-content">{r['summary']}</div>
#         </div>""", unsafe_allow_html=True)

#     with col2:
#         with st.expander("📝 Full Transcript", expanded=False):
#             st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

#     # Second row: action items | decisions | questions
#     c1, c2, c3 = st.columns(3, gap="medium")

#     with c1:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">✅ Action Items</div>
#             <div class="card-content">{r['action_items']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c2:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">🔑 Key Decisions</div>
#             <div class="card-content">{r['key_decisions']}</div>
#         </div>""", unsafe_allow_html=True)

#     with c3:
#         st.markdown(f"""
#         <div class="card">
#             <div class="card-title">❓ Open Questions</div>
#             <div class="card-content">{r['open_questions']}</div>
#         </div>""", unsafe_allow_html=True)

#     st.markdown("---")

#     # ── RAG Chat ──────────────────────────────────────────────────────────────
#     st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

#     # Chat history display
#     if st.session_state.chat_history:
#         chat_html = '<div class="chat-container">'
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-end">
#                     <span class="chat-label user-label">You</span>
#                     <div class="chat-bubble user-bubble">{msg['content']}</div>
#                 </div>"""
#             else:
#                 chat_html += f"""
#                 <div class="chat-msg" style="align-items:flex-start">
#                     <span class="chat-label bot-label">🤖 Assistant</span>
#                     <div class="chat-bubble bot-bubble">{msg['content']}</div>
#                 </div>"""
#         chat_html += '</div>'
#         st.markdown(chat_html, unsafe_allow_html=True)
#     else:
#         st.markdown("""
#         <div class="card" style="text-align:center;padding:2rem">
#             <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
#             <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
#         </div>""", unsafe_allow_html=True)

#     # Chat input
#     chat_col1, chat_col2 = st.columns([5, 1], gap="small")
#     with chat_col1:
#         user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
#     with chat_col2:
#         send_btn = st.button("Send →", use_container_width=True)

#     if send_btn and user_input.strip():
#         with st.spinner("Thinking…"):
#             answer = ask_question(r["rag_chain"], user_input.strip())
#         st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
#         st.session_state.chat_history.append({"role": "assistant", "content": answer})
#         st.rerun()

#     if st.session_state.chat_history:
#         if st.button("🗑️ Clear Chat", type="secondary"):
#             st.session_state.chat_history = []
#             st.rerun()

# else:
#     # Empty state
#     st.markdown("""
#     <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
#         <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
#         <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
#             Ready to Analyse
#         </div>
#         <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
#             Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
#         </div>
#         <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
#             <span class="badge badge-purple">Transcription</span>
#             <span class="badge badge-cyan">Summarisation</span>
#             <span class="badge badge-green">RAG Chat</span>
#         </div>
#     </div>""", unsafe_allow_html=True)


import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Video AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS & Advanced Dynamic Styling ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg: #030305;
    --surface: #0a0a0f;
    --surface-2: #12121a;
    --border: #222233;
    --border-hover: #ff6a00;
    --accent: #ff6a00;
    --accent-glow: #ff9d3d;
    --accent-2: #ff0055;
    --text: #f0f0f5;
    --text-muted: #8888a0;
    --success: #10b981;
    --warning: #f59e0b;
    --danger: #ef4444;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background: var(--bg) !important;
}

/* Dynamic Animated Grid Overlay */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    background-image:
        linear-gradient(rgba(255, 106, 0, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 106, 0, 0.05) 1px, transparent 1px);
    background-size: 50px 50px;
    pointer-events: none;
    z-index: 1;
    animation: gridDrift 20s linear infinite;
}

@keyframes gridDrift {
    0%   { background-position: 0 0, 0 0; }
    100% { background-position: 50px 50px, 50px 50px; }
}

/* Cursor-following CSS Glow Light */
#cursorGlow {
    position: fixed;
    top: 0; left: 0;
    width: 600px; height: 600px;
    margin-left: -300px;
    margin-top: -300px;
    background: radial-gradient(circle, rgba(255, 106, 0, 0.12) 0%, rgba(255, 0, 85, 0.06) 40%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
    z-index: 1;
    transition: transform 0.15s ease-out;
    mix-blend-mode: screen;
}

/* ── Sidebar Styling ── */
[data-testid="stSidebar"] {
    background: rgba(10, 10, 15, 0.85) !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid var(--border) !important;
    z-index: 10 !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Syne', sans-serif !important;
    color: var(--text) !important;
}

/* ── Hero Animated Title ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, var(--accent-glow) 40%, var(--accent-2) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 5s ease-in-out infinite;
    text-shadow: 0 0 30px rgba(255,106,0,0.3);
}

@keyframes shimmer {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.5rem;
    opacity: 0;
    animation: fadeInUp 0.8s ease forwards 0.2s;
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ── Modern 3D Interactive Cards ── */
.card {
    background: rgba(10, 10, 15, 0.75);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), border-color 0.3s ease, box-shadow 0.3s ease;
    opacity: 0;
    animation: fadeInUp 0.6s ease forwards;
    transform-style: preserve-3d;
}

.card:hover {
    border-color: var(--accent);
    transform: translateY(-6px) scale(1.015) rotateX(2deg) rotateY(-1deg);
    box-shadow: 0 15px 35px rgba(255, 106, 0, 0.25), 0 0 20px rgba(255, 0, 85, 0.15);
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, var(--accent), var(--accent-2));
    transition: width 0.3s ease, box-shadow 0.3s ease;
}

.card:hover::before {
    width: 6px;
    box-shadow: 0 0 16px var(--accent-glow);
}

/* Card Scanline Reflection Effect */
.card::after {
    content: '';
    position: absolute;
    top: -100%; left: -100%;
    width: 300%; height: 300%;
    background: linear-gradient(135deg, transparent 45%, rgba(255, 255, 255, 0.08) 50%, transparent 55%);
    transition: transform 0.8s ease;
    pointer-events: none;
}

.card:hover::after {
    transform: translate(50%, 50%);
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: color 0.3s ease;
}

.card:hover .card-title {
    color: var(--accent-glow);
}

.card-content {
    font-size: 0.875rem;
    line-height: 1.7;
    color: var(--text);
}

/* ── Badges ── */
.badge {
    display: inline-block;
    padding: 0.25rem 0.7rem;
    border-radius: 6px;
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    transition: all 0.3s ease;
}

.badge:hover {
    transform: translateY(-3px) scale(1.05);
}

.badge-purple { background: rgba(255,106,0,0.18); color: var(--accent-glow); border: 1px solid rgba(255,106,0,0.4); }
.badge-cyan   { background: rgba(255,0,85,0.18);  color: var(--accent-2);    border: 1px solid rgba(255,0,85,0.4); }
.badge-green  { background: rgba(16,185,129,0.18); color: var(--success);    border: 1px solid rgba(16,185,129,0.4); }

.badge-purple:hover { box-shadow: 0 0 15px rgba(255,106,0,0.5); }
.badge-cyan:hover   { box-shadow: 0 0 15px rgba(255,0,85,0.5); }
.badge-green:hover  { box-shadow: 0 0 15px rgba(16,185,129,0.5); }

/* ── Inputs & Futuristic Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:hover {
    border-color: rgba(255,106,0,0.6) !important;
    box-shadow: 0 0 12px rgba(255,106,0,0.15) !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 15px rgba(255,106,0,0.3) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-2)) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.7rem 1.6rem !important;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    text-transform: uppercase !important;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(255, 106, 0, 0.3) !important;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 60%; height: 100%;
    background: linear-gradient(120deg, transparent, rgba(255,255,255,0.4), transparent);
    transform: skewX(-20deg);
    transition: left 0.6s ease;
}

.stButton > button:hover::before {
    left: 140%;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.03) !important;
    box-shadow: 0 10px 30px rgba(255, 106, 0, 0.5), 0 0 25px rgba(255, 0, 85, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) scale(0.97) !important;
}

/* Secondary Button */
.stButton > button[kind="secondary"] {
    background: var(--surface-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent) !important;
    box-shadow: 0 6px 20px rgba(255,106,0,0.25) !important;
}

/* ── Progress & Status Bars ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.8rem 1.1rem;
    background: var(--surface-2);
    border-radius: 10px;
    margin: 0.4rem 0;
    border: 1px solid var(--border);
    font-size: 0.8rem;
    transition: all 0.3s ease;
}

.status-bar:hover {
    border-color: rgba(255,106,0,0.5);
    transform: translateX(5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
}

.status-dot {
    width: 9px; height: 9px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-active   { background: var(--accent-glow); box-shadow: 0 0 10px var(--accent-glow); animation: pulse 1.2s infinite; }
.dot-done     { background: var(--success); box-shadow: 0 0 8px var(--success); }
.dot-pending  { background: var(--border); }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.3; transform: scale(0.85); }
}

/* ── Chat Display ── */
.chat-container {
    background: rgba(10, 10, 15, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.25rem;
    max-height: 420px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.chat-msg {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    opacity: 0;
    animation: fadeInUp 0.4s ease forwards;
}

.chat-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.chat-bubble {
    display: inline-block;
    padding: 0.75rem 1.1rem;
    border-radius: 12px;
    font-size: 0.85rem;
    line-height: 1.6;
    max-width: 88%;
    transition: all 0.25s ease;
}

.chat-bubble:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(255,106,0,0.2);
}

.user-label  { color: var(--accent-glow); }
.bot-label   { color: var(--accent-2); }

.user-bubble { background: rgba(255,106,0,0.15); border: 1px solid rgba(255,106,0,0.3); align-self: flex-end; }
.bot-bubble  { background: rgba(255,0,85,0.1);    border: 1px solid rgba(255,0,85,0.25);  align-self: flex-start; }

/* ── Transcript Box ── */
.transcript-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.25rem;
    font-size: 0.82rem;
    line-height: 1.8;
    max-height: 300px;
    overflow-y: auto;
    color: var(--text-muted);
    white-space: pre-wrap;
    word-break: break-word;
    transition: border-color 0.3s ease;
}

.transcript-box:hover {
    border-color: rgba(255,106,0,0.4);
}

/* Scrollbar Styling */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }

/* Staggered card entrance delays */
.card:nth-of-type(1) { animation-delay: 0.05s; }
.card:nth-of-type(2) { animation-delay: 0.12s; }
.card:nth-of-type(3) { animation-delay: 0.19s; }
.card:nth-of-type(4) { animation-delay: 0.26s; }
</style>

<!-- Cursor Following Background Spotlight -->
<div id="cursorGlow"></div>
""", unsafe_allow_html=True)

# ─── 3D Interactive WebGL Scene (Three.js with Raycasting Hover & Dynamic Lighting) ───
st.markdown("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<canvas id="bg3dCanvas" style="
    position: fixed;
    top: 0; left: 0;
    width: 100vw; height: 100vh;
    pointer-events: auto;
    z-index: 0;
    opacity: 0.75;
"></canvas>

<script>
(function() {
    if (window.__three3DInit) return;
    window.__three3DInit = true;

    const canvas = document.getElementById('bg3dCanvas');
    const cursorGlow = document.getElementById('cursorGlow');
    if (!canvas) return;

    // 1. Scene, Camera, WebGL Renderer
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 24;

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // 2. Dynamic Lighting Engine
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    // Point Light that directly tracks the user cursor in 3D Space
    const cursorLight = new THREE.PointLight(0xff6a00, 2.5, 50);
    scene.add(cursorLight);

    const backLight = new THREE.PointLight(0xff0055, 1.8, 40);
    backLight.position.set(-15, -10, -10);
    scene.add(backLight);

    // 3. 3D Model: Torus Knot Mesh Wireframe
    const group = new THREE.Group();
    scene.add(group);

    const knotGeometry = new THREE.TorusKnotGeometry(6.5, 2.0, 140, 18);
    const knotMaterial = new THREE.MeshStandardMaterial({
        color: 0xff6a00,
        wireframe: true,
        roughness: 0.2,
        metalness: 0.8,
        emissive: 0x331100,
        transparent: true,
        opacity: 0.35
    });
    const torusKnot = new THREE.Mesh(knotGeometry, knotMaterial);
    group.add(torusKnot);

    // Floating Interactive Particle Stars Field
    const particleCount = 800;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const initialY = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
        const idx = i * 3;
        positions[idx]     = (Math.random() - 0.5) * 70;
        positions[idx + 1] = (Math.random() - 0.5) * 70;
        positions[idx + 2] = (Math.random() - 0.5) * 70;
        initialY[i] = positions[idx + 1];
    }

    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({
        color: 0xff9d3d,
        size: 0.18,
        transparent: true,
        opacity: 0.65
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    group.add(particles);

    // 4. Mouse Tracking & Raycasting Setup
    const raycaster = new THREE.Raycaster();
    const mouse2D = new THREE.Vector2(-100, -100);
    let targetX = 0, targetY = 0;
    let isHovered = false;

    window.addEventListener('mousemove', (e) => {
        // Update 2D Normalized Coordinates for Raycasting
        mouse2D.x = (e.clientX / window.innerWidth) * 2 - 1;
        mouse2D.y = -(e.clientY / window.innerHeight) * 2 + 1;

        targetX = mouse2D.x * 0.8;
        targetY = mouse2D.y * 0.8;

        // Update Cursor Following Glow Spotlight
        if (cursorGlow) {
            cursorGlow.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
        }

        // Map 2D Cursor to 3D Space for Cursor Point Light
        cursorLight.position.x = mouse2D.x * 15;
        cursorLight.position.y = mouse2D.y * 15;
        cursorLight.position.z = 10;
    });

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });

    // 5. Animation Render Loop
    let clock = new THREE.Clock();

    function animate() {
        requestAnimationFrame(animate);

        const elapsedTime = clock.getElapsedTime();

        // Wave motion for particles
        const posAttr = particleGeo.attributes.position;
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
            posAttr.array[idx + 1] = initialY[i] + Math.sin(elapsedTime * 1.5 + posAttr.array[idx]) * 0.8;
        }
        posAttr.needsUpdate = true;

        // Raycasting for 3D Model Hover Detection
        raycaster.setFromCamera(mouse2D, camera);
        const intersects = raycaster.intersectObject(torusKnot);

        if (intersects.length > 0) {
            if (!isHovered) {
                isHovered = true;
                // Color morph on hover: Neon Orange -> Electric Magenta
                torusKnot.material.color.setHex(0xff0055);
                torusKnot.material.emissive.setHex(0xaa0033);
                torusKnot.material.opacity = 0.75;
                cursorLight.color.setHex(0xff0055);
            }
        } else {
            if (isHovered) {
                isHovered = false;
                // Revert color back on exit
                torusKnot.material.color.setHex(0xff6a00);
                torusKnot.material.emissive.setHex(0x331100);
                torusKnot.material.opacity = 0.35;
                cursorLight.color.setHex(0xff6a00);
            }
        }

        // Smooth Physics Rotation & Spring Interpolation
        const speedMultiplier = isHovered ? 2.5 : 1.0;
        group.rotation.x += 0.002 * speedMultiplier;
        group.rotation.y += 0.003 * speedMultiplier;

        // Smooth Mouse Rotation Tilting
        group.rotation.y += (targetX - group.rotation.y) * 0.03;
        group.rotation.x += (-targetY - group.rotation.x) * 0.03;

        // Pulsing Mesh Scale Effect on Hover
        const targetScale = isHovered ? 1.15 : 1.0;
        torusKnot.scale.x += (targetScale - torusKnot.scale.x) * 0.05;
        torusKnot.scale.y += (targetScale - torusKnot.scale.y) * 0.05;
        torusKnot.scale.z += (targetScale - torusKnot.scale.z) * 0.05;

        renderer.render(scene, camera);
    }

    animate();
})();
</script>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "dot-active"
    if s == "done":    return "dot-done"
    return "dot-pending"

def render_step_bar(label: str, key: str, icon: str):
    css = step_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span>{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-title" style="font-size:1.6rem">🎬 Smart Video<br>AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Meeting Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
        for step, icon, label in [
            ("audio",      "🔊", "Audio Processing"),
            ("transcript", "📝", "Transcription"),
            ("title",      "🏷️", "Title Generation"),
            ("summary",    "📋", "Summarisation"),
            ("extract",    "🔍", "Extraction"),
            ("rag",        "🧠", "RAG Engine"),
        ]:
            render_step_bar(label, step, icon)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Smart Video AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Transcribe · Summarise · Chat with your meetings</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("⚙️ Pipeline running — see sidebar for live status…")

            # 1. Process Audio / Transcript
            update_step("audio", "active")
            processed_data = process_input(source)
            update_step("audio", "done")

            # 2. Extract / Compute Transcription
            update_step("transcript", "active")
            if isinstance(processed_data, str):
                # Direct string transcript from YouTube API
                transcript = processed_data
            else:
                # Audio chunk paths to transcribe using Whisper
                transcript = transcribe_all(processed_data, language)
            update_step("transcript", "done")

            # 3. Generate Title
            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            # 4. Summarize Transcript
            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            # 5. Extract Key Metrics
            update_step("extract", "active")
            action_items  = extract_action_items(transcript)
            decisions     = extract_key_decisions(transcript)
            questions     = extract_questions(transcript)
            update_step("extract", "done")

            # 6. Build RAG Engine
            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("✅ Analysis complete!")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio", "transcript", "title", "summary", "extract", "rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.4rem;font-weight:700;color:var(--text)">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Top row: summary + transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Summary</div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    # Second row: action items | decisions | questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">✅ Action Items</div>
            <div class="card-content">{r['action_items']}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🔑 Key Decisions</div>
            <div class="card-content">{r['key_decisions']}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">❓ Open Questions</div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:1.2rem;font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label user-label">You</span>
                    <div class="chat-bubble user-bubble">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label bot-label">🤖 Assistant</span>
                    <div class="chat-bubble bot-bubble">{msg['content']}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem">
            <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
            <div style="color:var(--text-muted);font-size:0.85rem">Ask anything about your meeting transcript</div>
        </div>""", unsafe_allow_html=True)

    # Chat input
    chat_col1, chat_col2 = st.columns([5, 1], gap="small")
    with chat_col1:
        user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
    with chat_col2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 2rem;text-align:center">
        <div style="font-size:4rem;margin-bottom:1rem">🎬</div>
        <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
            Ready to Analyse
        </div>
        <div style="color:var(--text-muted);font-size:0.85rem;max-width:380px;line-height:1.7">
            Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong>Analyse</strong> to get started.
        </div>
        <div style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-green">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)