import random
rng=random.Random(7)
W,H=1200,300
n=46; x0=640; x1=1160; step=(x1-x0)/n
p=100.0; candles=[]
for i in range(n):
    o=p; drift=0.35 if i>n*0.45 else -0.05
    c=o+rng.gauss(drift,1.6); hi=max(o,c)+abs(rng.gauss(0,0.8)); lo=min(o,c)-abs(rng.gauss(0,0.8))
    candles.append((o,hi,lo,c)); p=c
mn=min(c[2] for c in candles); mx=max(c[1] for c in candles)
y=lambda v: 250-(v-mn)/(mx-mn)*170
parts=[]
for i,(o,hi,lo,c) in enumerate(candles):
    cx=x0+i*step+step/2; col="#2dd4bf" if c>=o else "#f87171"
    delay=f"{i*0.035:.2f}s"
    parts.append(f'<g class="c" style="animation-delay:{delay}"><line x1="{cx:.1f}" x2="{cx:.1f}" y1="{y(hi):.1f}" y2="{y(lo):.1f}" stroke="{col}" stroke-width="1.2"/>'
                 f'<rect x="{cx-step*0.32:.1f}" y="{y(max(o,c)):.1f}" width="{step*0.64:.1f}" height="{max(1.2,abs(y(o)-y(c))):.1f}" fill="{col}" rx="1"/></g>')
# EMA line
ema=None; pts=[]
for i,(o,hi,lo,c) in enumerate(candles):
    ema=c if ema is None else ema+0.18*(c-ema); pts.append(f"{x0+i*step+step/2:.1f},{y(ema):.1f}")
F="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
M="ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,monospace"
grid="".join(f'<line x1="620" x2="1180" y1="{gy}" y2="{gy}" stroke="#1f2937" stroke-dasharray="2 6"/>' for gy in (80,120,160,200,240))
tape="  ·  ".join(["LLM-VETO-DISTILL  κ≈0.45  3 ms/card","ATR-BREAKOUT v1  pre-registered","NVIDIA DLI  LLM compression  100/100","GCP ACE  in progress","C++ / RUST  learning"])
L=round(len(tape+"  ·  ")*7.3)
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Bala Nambi, quant developer in training">
<style>
.c{{opacity:0;animation:in .4s ease-out forwards}}
@keyframes in{{to{{opacity:1}}}}
.ema{{stroke-dasharray:1400;stroke-dashoffset:1400;animation:draw 2.4s ease-out .3s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.tape{{animation:scroll 40s linear infinite}}
@keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{L}px)}}}}
.blink{{animation:b 1.1s step-end infinite}}
@keyframes b{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.c,.ema,.tape,.blink{{animation:none;opacity:1;stroke-dashoffset:0}}}}
</style>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<clipPath id="t"><rect x="0" y="268" width="{W}" height="32"/></clipPath></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
{grid}
{''.join(parts)}
<polyline class="ema" points="{' '.join(pts)}" fill="none" stroke="#f59e0b" stroke-width="1.6"/>
<text x="1180" y="60" text-anchor="end" font-family="{M}" font-size="11" fill="#6b7280">M15 · EMA(10)</text>
<text x="56" y="92" font-family="{M}" font-size="14" fill="#2dd4bf">$ whoami<tspan class="blink">_</tspan></text>
<text x="56" y="140" font-family="{F}" font-size="44" font-weight="700" fill="#e6edf3">Bala Nambi</text>
<text x="56" y="176" font-family="{F}" font-size="20" fill="#c9d1d9">Quant developer in training</text>
<text x="56" y="208" font-family="{F}" font-size="15" fill="#8b949e">ML for trading · execution systems · cloud data pipelines</text>
<text x="56" y="232" font-family="{F}" font-size="15" fill="#8b949e">42 Paris · Python, C → C++, Rust</text>
<rect x="0" y="268" width="{W}" height="32" fill="#111827"/>
<g clip-path="url(#t)"><g class="tape" font-family="{M}" font-size="12" fill="#9ca3af">
<text x="24" y="289" xml:space="preserve" textLength="{L}" lengthAdjust="spacing">{tape}  ·  </text><text x="{24+L}" y="289" xml:space="preserve" textLength="{L}" lengthAdjust="spacing">{tape}  ·  </text><text x="{24+2*L}" y="289" xml:space="preserve" textLength="{L}" lengthAdjust="spacing">{tape}  ·  </text></g></g>
</svg>
'''
open(__import__('pathlib').Path(__file__).resolve().parent.parent/'assets'/'banner.svg','w').write(svg)
