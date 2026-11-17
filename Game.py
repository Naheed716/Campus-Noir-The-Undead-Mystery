```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Noir: The Undead Mystery</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Inter:wght@400;600;800&family=Special+Elite&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #09090b;
            color: #f4f4f5;
            overflow: hidden;
            user-select: none;
        }
        .font-detective {
            font-family: 'Special Elite', cursive;
        }
        .font-title {
            font-family: 'Cinzel', serif;
        }
        /* Custom glow effects */
        .neon-glow-red {
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.4);
        }
        .neon-glow-cyan {
            box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
        }
        .vignette {
            box-shadow: inset 0 0 100px rgba(0, 0, 0, 0.85);
        }
        /* Scanline overlay */
        .scanlines {
            background: linear-gradient(
                rgba(18, 16, 16, 0) 50%, 
                rgba(0, 0, 0, 0.25) 50%
            ), linear-gradient(
                90deg,
                rgba(255, 0, 0, 0.03),
                rgba(0, 255, 0, 0.01),
                rgba(0, 0, 255, 0.03)
            );
            background-size: 100% 4px, 6px 100%;
            pointer-events: none;
        }
        /* Custom scrollbar for inventory/dialogue */
        ::-webkit-scrollbar {
            width: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #18181b;
        }
        ::-webkit-scrollbar-thumb {
            background: #3f3f46;
            border-radius: 3px;
        }
    </style>
</head>
<body class="h-screen w-screen flex flex-col items-center justify-center relative">

    <!-- Top Status Bar -->
    <header class="absolute top-0 left-0 right-0 h-16 bg-zinc-950/90 border-b border-zinc-800 flex items-center justify-between px-6 z-30 backdrop-blur-md">
        <div class="flex items-center space-x-4">
            <div class="flex items-center space-x-2">
                <span class="w-3 h-3 rounded-full bg-cyan-500 animate-pulse"></span>
                <h1 class="font-title text-xl font-bold tracking-wider text-cyan-400">CAMPUS NOIR</h1>
            </div>
            <span class="text-xs px-2.5 py-1 bg-zinc-800 text-zinc-400 rounded-md font-mono" id="current-zone">ZONE: QUAD (CAMPUS GROUNDS)</span>
        </div>

        <div class="flex items-center space-x-8">
            <!-- Health & Sanity -->
            <div class="flex items-center space-x-4 text-xs font-semibold">
                <div class="flex flex-col">
                    <div class="flex justify-between mb-1 text-zinc-400">
                        <span>VITALITY (HP)</span>
                        <span id="hp-text">100/100</span>
                    </div>
                    <div class="w-36 h-2.5 bg-zinc-800 rounded-full overflow-hidden border border-zinc-700">
                        <div id="hp-bar" class="h-full bg-gradient-to-r from-red-600 to-emerald-500 transition-all duration-300" style="width: 100%"></div>
                    </div>
                </div>
                <div class="flex flex-col">
                    <div class="flex justify-between mb-1 text-zinc-400">
                        <span>SANITY</span>
                        <span id="sanity-text">100%</span>
                    </div>
                    <div class="w-36 h-2.5 bg-zinc-800 rounded-full overflow-hidden border border-zinc-700">
                        <div id="sanity-bar" class="h-full bg-gradient-to-r from-purple-600 to-cyan-400 transition-all duration-300" style="width: 100%"></div>
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex items-center space-x-3">
                <button onclick="toggleNotebook()" class="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 rounded-lg text-xs font-semibold tracking-wide flex items-center space-x-2 transition shadow-md">
                    <span>📓 Evidence Board (<span id="clue-count">0</span>/5)</span>
                </button>
                <button onclick="toggleAudio()" id="audio-toggle" class="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 rounded-lg text-xs font-semibold tracking-wide transition shadow-md">
                    🔊 Audio: ON
                </button>
            </div>
        </div>
    </header>

    <!-- Main Game Container -->
    <main class="relative w-full h-full flex items-center justify-center pt-16 bg-zinc-950 overflow-hidden">
        
        <!-- Canvas for Game Rendering -->
        <canvas id="gameCanvas" class="absolute inset-0 w-full h-full cursor-crosshair"></canvas>

        <!-- Vignette & Scanline overlays -->
        <div class="absolute inset-0 vignette pointer-events-none z-10"></div>
        <div class="absolute inset-0 scanlines pointer-events-none z-10"></div>

        <!-- Interactive HUD / Floating Prompts -->
        <div id="interaction-prompt" class="absolute bottom-24 left-1/2 transform -translate-x-1/2 bg-zinc-900/90 border border-cyan-500/50 text-cyan-300 px-4 py-2 rounded-xl text-sm font-semibold tracking-wide z-25 hidden backdrop-blur shadow-2xl animate-bounce">
            Press [E] or Click to Examine / Interact
        </div>

        <!-- Dialogue / Story Box Overlay -->
        <div id="dialogue-box" class="absolute bottom-6 left-1/2 transform -translate-x-1/2 w-11/12 max-w-4xl bg-zinc-900/95 border-2 border-zinc-700 rounded-2xl p-6 z-30 shadow-2xl backdrop-blur-md hidden">
            <div class="flex items-start space-x-4">
                <div class="w-16 h-16 rounded-xl bg-zinc-800 border-2 border-cyan-500/60 flex items-center justify-center flex-shrink-0 overflow-hidden shadow-inner">
                    <img id="speaker-avatar" src="https://placehold.co/100x100/18181b/06b6d4?text=AYA" alt="Aya" class="w-full h-full object-cover">
                </div>
                <div class="flex-1">
                    <div class="flex justify-between items-center mb-1">
                        <h3 id="speaker-name" class="font-title font-bold text-cyan-400 text-lg">Aya Vance (Investigative Journalist & Best Friend)</h3>
                        <span class="text-xs text-zinc-500 font-mono">ENCRYPTED SECURE LOG</span>
                    </div>
                    <p id="dialogue-text" class="font-detective text-zinc-300 text-sm md:text-base leading-relaxed tracking-wide min-h-[3rem]">
                        "Maya... why did you have to dig into Professor Sterling's bio-lab grant? Now the campus is overrun with these things, and you're gone. I'll find whoever did this to you."
                    </p>
                </div>
            </div>
            <div class="mt-4 flex justify-end">
                <button onclick="advanceDialogue()" class="px-5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-xs font-bold tracking-wider uppercase transition shadow-lg shadow-cyan-900/40">
                    Continue [Space / Enter] ➔
                </button>
            </div>
        </div>

        <!-- Notebook / Evidence Modal -->
        <div id="notebook-modal" class="absolute inset-0 bg-black/80 backdrop-blur-md z-40 flex items-center justify-center p-6 hidden">
            <div class="w-full max-w-3xl bg-zinc-900 border-2 border-zinc-700 rounded-2xl p-6 shadow-2xl flex flex-col max-h-[85vh]">
                <div class="flex justify-between items-center border-b border-zinc-800 pb-4 mb-4">
                    <div>
                        <h2 class="font-title text-2xl font-bold text-cyan-400">INVESTIGATION NOTEBOOK</h2>
                        <p class="text-xs text-zinc-400 font-mono">Case File #8841: The Murder of Maya Thorne</p>
                    </div>
                    <button onclick="toggleNotebook()" class="text-zinc-400 hover:text-white p-2 rounded-lg bg-zinc-800 text-sm">✕ Close</button>
                </div>

                <div class="flex-1 overflow-y-auto space-y-4 pr-2" id="clues-list">
                    <!-- Populated dynamically -->
                </div>

                <div class="mt-4 pt-4 border-t border-zinc-800 flex justify-between items-center">
                    <span class="text-xs text-zinc-400 font-mono" id="notebook-status">Clues Discovered: 0 / 5</span>
                    <button id="accusation-btn" onclick="openAccusation()" class="px-5 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold tracking-wider uppercase transition shadow-lg shadow-red-900/40 opacity-50 cursor-not-allowed" disabled>
                        Make Final Accusation
                    </button>
                </div>
            </div>
        </div>

        <!-- Accusation Modal -->
        <div id="accusation-modal" class="absolute inset-0 bg-black/90 backdrop-blur-md z-50 flex items-center justify-center p-6 hidden">
            <div class="w-full max-w-2xl bg-zinc-900 border-2 border-red-600/60 rounded-2xl p-8 shadow-2xl">
                <h2 class="font-title text-2xl font-bold text-red-500 mb-2 text-center">FINAL ACCUSATION SCENE</h2>
                <p class="text-xs text-zinc-400 font-mono text-center mb-6">Review your forensic evidence and select Maya's true killer from the suspects below.</p>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div onclick="selectSuspect('sterling')" id="suspect-sterling" class="p-4 bg-zinc-800/80 border-2 border-zinc-700 rounded-xl cursor-pointer hover:border-cyan-500 transition text-center">
                        <div class="w-20 h-20 mx-auto mb-3 rounded-full bg-zinc-700 overflow-hidden border border-zinc-600">
                            <img src="https://placehold.co/100x100/27272a/ef4444?text=PROF" alt="Sterling" class="w-full h-full object-cover">
                        </div>
                        <h4 class="font-title font-bold text-sm text-zinc-200">Prof. Alistair Sterling</h4>
                        <p class="text-[10px] text-zinc-400 mt-1">Head of Bio-Research & Genetics Lab</p>
                    </div>

                    <div onclick="selectSuspect('dean')" id="suspect-dean" class="p-4 bg-zinc-800/80 border-2 border-zinc-700 rounded-xl cursor-pointer hover:border-cyan-500 transition text-center">
                        <div class="w-20 h-20 mx-auto mb-3 rounded-full bg-zinc-700 overflow-hidden border border-zinc-600">
                            <img src="https://placehold.co/100x100/27272a/eab308?text=DEAN" alt="Dean" class="w-full h-full object-cover">
                        </div>
                        <h4 class="font-title font-bold text-sm text-zinc-200">Dean Margaret Vance</h4>
                        <p class="text-[10px] text-zinc-400 mt-1">University Dean & Financial Controller</p>
                    </div>

                    <div onclick="selectSuspect('brad')" id="suspect-brad" class="p-4 bg-zinc-800/80 border-2 border-zinc-700 rounded-xl cursor-pointer hover:border-cyan-500 transition text-center">
                        <div class="w-20 h-20 mx-auto mb-3 rounded-full bg-zinc-700 overflow-hidden border border-zinc-600">
                            <img src="https://placehold.co/100x100/27272a/3b82f6?text=BRAD" alt="Brad" class="w-full h-full object-cover">
                        </div>
                        <h4 class="font-title font-bold text-sm text-zinc-200">Brad Miller</h4>
                        <p class="text-[10px] text-zinc-400 mt-1">Lead Student Assistant & Rival Researcher</p>
                    </div>
                </div>

                <div class="bg-zinc-950 p-4 rounded-xl border border-zinc-800 mb-6 min-h-[4rem] flex items-center justify-center text-center">
                    <p id="suspect-bio" class="text-xs text-zinc-400 italic">Click a suspect above to review their motive and file summary.</p>
                </div>

                <div class="flex justify-end space-x-3">
                    <button onclick="closeAccusation()" class="px-4 py-2 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 rounded-xl text-xs font-bold transition">Cancel</button>
                    <button onclick="submitAccusation()" id="confirm-accusation-btn" class="px-6 py-2 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold uppercase transition shadow-lg opacity-50 cursor-not-allowed" disabled>Submit Accusation</button>
                </div>
            </div>
        </div>

        <!-- Game Over / Victory Modal -->
        <div id="end-modal" class="absolute inset-0 bg-black/95 backdrop-blur-lg z-50 flex items-center justify-center p-6 hidden">
            <div class="w-full max-w-xl bg-zinc-900 border-2 border-cyan-500/80 rounded-2xl p-8 text-center shadow-2xl">
                <h2 id="end-title" class="font-title text-3xl font-bold text-cyan-400 mb-3">CASE CLOSED</h2>
                <p id="end-message" class="text-sm text-zinc-300 mb-6 leading-relaxed font-detective">You have solved the mystery and survived the campus nightmare.</p>
                <button onclick="restartGame()" class="px-6 py-3 bg-cyan-600 hover:bg-cyan-500 text-white rounded-xl text-sm font-bold tracking-wider uppercase transition shadow-xl shadow-cyan-900/50">Play Again</button>
            </div>
        </div>

        <!-- Start Screen Overlay -->
        <div id="start-screen" class="absolute inset-0 bg-zinc-950 z-50 flex items-center justify-center p-6">
            <div class="w-full max-w-2xl bg-zinc-900/90 border-2 border-cyan-500/50 rounded-2xl p-8 text-center shadow-2xl backdrop-blur-md relative overflow-hidden">
                <div class="absolute -right-16 -top-16 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
                <div class="absolute -left-16 -bottom-16 w-48 h-48 bg-red-500/10 rounded-full blur-3xl pointer-events-none"></div>

                <span class="text-xs uppercase tracking-widest text-cyan-400 font-mono mb-2 block">An Interactive Noir Survival Thriller</span>
                <h1 class="font-title text-4xl md:text-5xl font-extrabold text-white tracking-wider mb-4">CAMPUS NOIR</h1>
                <p class="text-zinc-400 text-xs md:text-sm mb-8 leading-relaxed max-w-lg mx-auto font-detective">
                    Your best friend Maya was murdered on campus just hours before the viral outbreak turned students and faculty into ravenous ghouls. Navigate the Quad, Library, Dorms, and Bio-Lab, evade the infected, gather forensic clues, and unmask her killer.
                </p>

                <div class="grid grid-cols-2 gap-4 max-w-md mx-auto mb-8 text-left text-xs bg-zinc-950 p-4 rounded-xl border border-zinc-800">
                    <div>
                        <span class="text-cyan-400 font-bold block mb-1">CONTROLS:</span>
                        <p class="text-zinc-400">WASD / Arrow Keys: Move</p>
                        <p class="text-zinc-400">Mouse: Flashlight Aim</p>
                        <p class="text-zinc-400">E / Click: Interact / Clue</p>
                    </div>
                    <div>
                        <span class="text-cyan-400 font-bold block mb-1">OBJECTIVE:</span>
                        <p class="text-zinc-400">1. Collect 5 forensic clues</p>
                        <p class="text-zinc-400">2. Avoid zombie patrols</p>
                        <p class="text-zinc-400">3. Accuse the true murderer</p>
                    </div>
                </div>

                <button onclick="startGame()" class="px-8 py-3.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-xl font-bold tracking-widest uppercase transition shadow-xl shadow-cyan-900/50 text-sm">
                    Begin Investigation
                </button>
            </div>
        </div>

    </main>

    <script>
        /* --- AUDIO SYNTHESIZER (Web Audio API) --- */
        let audioCtx = null;
        let audioEnabled = true;

        function initAudio() {
            if (!audioCtx) {
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }
        }

        function playSound(type) {
            if (!audioEnabled || !audioCtx) return;
            try {
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.connect(gain);
                gain.connect(audioCtx.destination);

                const now = audioCtx.currentTime;

                if (type === 'click') {
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(600, now);
                    osc.frequency.exponentialRampToValueAtTime(200, now + 0.08);
                    gain.gain.setValueAtTime(0.15, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.08);
                    osc.start(now);
                    osc.stop(now + 0.08);
                } else if (type === 'clue') {
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(440, now);
                    osc.frequency.exponentialRampToValueAtTime(880, now + 0.3);
                    gain.gain.setValueAtTime(0.2, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.3);
                    osc.start(now);
                    osc.stop(now + 0.3);
                } else if (type === 'hit') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(150, now);
                    osc.frequency.exponentialRampToValueAtTime(40, now + 0.25);
                    gain.gain.setValueAtTime(0.3, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.25);
                    osc.start(now);
                    osc.stop(now + 0.25);
                } else if (type === 'zombie') {
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(90, now);
                    osc.frequency.linearRampToValueAtTime(60, now + 0.4);
                    gain.gain.setValueAtTime(0.1, now);
                    gain.gain.linearRampToValueAtTime(0.01, now + 0.4);
                    osc.start(now);
                    osc.stop(now + 0.4);
                }
            } catch (e) {
                console.error("Audio error", e);
            }
        }

        function toggleAudio() {
            audioEnabled = !audioEnabled;
            const btn = document.getElementById('audio-toggle');
            btn.innerText = audioEnabled ? "🔊 Audio: ON" : "🔇 Audio: OFF";
            playSound('click');
        }


        /* --- GAME ENGINE & STATE --- */
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        let gameRunning = false;
        let gamePaused = false;

        // Player Stats
        let player = {
            x: 400,
            y: 300,
            radius: 16,
            speed: 3.2,
            hp: 100,
            maxHp: 100,
            sanity: 100,
            angle: 0
        };

        // Input Tracking
        const keys = { w: false, a: false, s: false, d: false, up: false, left: false, down: false, right: false };
        let mouseX = 400;
        let mouseY = 300;

        // Campus Zones & Map
        let currentZoneId = 'quad';
        const zones = {
            quad: { name: 'QUAD (CAMPUS GROUNDS)', color: '#09090b', ambient: 'rgba(5, 5, 10, 0.7)' },
            library: { name: 'UNIVERSITY LIBRARY', color: '#0f172a', ambient: 'rgba(10, 15, 30, 0.8)' },
            dorms: { name: 'STUDENT RES
