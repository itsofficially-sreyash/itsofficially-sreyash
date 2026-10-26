"""Generate the animated SVGs used by the profile README.

    python make_assets.py

Writes:
  assets/banner-dark.svg / banner-light.svg  header with name, typing subtitle,
                                             drifting dots and animated waves
  assets/room.svg                            animated pixel-art dev room

Only CSS / SMIL animation is used (no scripts), so GitHub renders them
when embedded with <img>.
"""
import random

NAME = "SREYASH SINGH"
SUBTITLE = "flutter developer · student founder · builder"
STACK = "Dart  ·  Flutter  ·  C++  ·  TypeScript"
MONOGRAM = "S"

MONO = "Consolas,'SFMono-Regular','Liberation Mono',Menlo,monospace"
PAGE_BG = {"dark": "#0d1117", "light": "#ffffff"}


# --------------------------------------------------------------------------
# Banner
# --------------------------------------------------------------------------
def banner(mode):
    W, H = 1200, 400
    rnd = random.Random(7)
    css, dots = [], []

    for i in range(55):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H - 90)
        r = rnd.choice([1.5, 2, 2.5, 3, 4])
        dx, dy = rnd.randint(-70, 70), rnd.randint(-35, 35)
        dur, delay = round(rnd.uniform(9, 18), 1), round(rnd.uniform(-12, 0), 1)
        css.append(
            f"@keyframes d{i}{{50%{{transform:translate({dx}px,{dy}px)}}}}"
            f".d{i}{{animation:d{i} {dur}s ease-in-out {delay}s infinite}}"
        )
        tw = round(rnd.uniform(2.5, 5), 1)
        dots.append(
            f'<circle class="d{i}" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff">'
            f'<animate attributeName="opacity" values=".15;.7;.15" dur="{tw}s" '
            f'begin="-{rnd.uniform(0, tw):.1f}s" repeatCount="indefinite"/></circle>'
        )

    # A few connected "constellations" drifting together
    for c in range(5):
        cx, cy = rnd.uniform(80, 760), rnd.uniform(40, 260)
        pts = [(cx + rnd.uniform(-70, 70), cy + rnd.uniform(-40, 40)) for _ in range(4)]
        css.append(
            f"@keyframes k{c}{{50%{{transform:translate({rnd.randint(-40, 40)}px,"
            f"{rnd.randint(-20, 20)}px)}}}}"
            f".k{c}{{animation:k{c} {round(rnd.uniform(12, 20), 1)}s ease-in-out "
            f"{round(rnd.uniform(-10, 0), 1)}s infinite}}"
        )
        lines = "".join(
            f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}"/>'
            for a, b in zip(pts, pts[1:])
        )
        pd = "".join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.5"/>' for x, y in pts)
        dots.append(
            f'<g class="k{c}"><g stroke="#fff" stroke-opacity=".3">{lines}</g>'
            f'<g fill="#fff" fill-opacity=".6">{pd}</g></g>'
        )

    def wave(y, amp):
        # Two periods wide so translating by -W loops seamlessly
        seg = W / 2
        d = f"M0 {y}"
        for k in range(4):
            sign = -1 if k % 2 == 0 else 1
            d += f" Q{seg * k + seg / 2:.0f} {y + sign * amp} {seg * (k + 1):.0f} {y}"
        return d + f" V{H} H0Z"

    bg = PAGE_BG[mode]
    sub_w = len(SUBTITLE) * 15.5
    css.append(
        "@keyframes slide{to{transform:translateX(-1200px)}}"
        ".w1{animation:slide 14s linear infinite}"
        ".w2{animation:slide 9s linear infinite}"
        "@keyframes blink{50%{opacity:0}}.cur{animation:blink 1s steps(1) infinite}"
        "@keyframes float{50%{transform:translateY(-10px)}}.logo{animation:float 5s ease-in-out infinite}"
        "@keyframes spin{to{transform:rotate(360deg)}}"
        ".ring{transform-origin:990px 170px;animation:spin 18s linear infinite}"
        "@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
        ".name{animation:rise 1s ease-out both}.stack{animation:rise 1s ease-out 3.2s both}"
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b82f6"/><stop offset="1" stop-color="#5b9dff"/></linearGradient>
<clipPath id="type"><rect x="60" y="125" height="40" width="0">
<animate attributeName="width" values="{';'.join(f'{i * sub_w / len(SUBTITLE):.0f}' for i in range(len(SUBTITLE) + 1))}" dur="2.6s" begin=".8s" fill="freeze" calcMode="discrete" /></rect></clipPath>
</defs>
<style>{''.join(css)}</style>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
{''.join(dots)}
<text class="name" x="60" y="105" font-family="{MONO}" font-size="58" font-weight="700" fill="#0d1117">{NAME}</text>
<g clip-path="url(#type)"><text x="60" y="156" font-family="{MONO}" font-size="28" fill="#13294b">{SUBTITLE}</text></g>
<rect class="cur" x="60" y="132" width="14" height="30" fill="#13294b">
<animate attributeName="x" values="{';'.join(f'{60 + i * sub_w / len(SUBTITLE):.0f}' for i in range(len(SUBTITLE) + 1))}" dur="2.6s" begin=".8s" fill="freeze" calcMode="discrete"/></rect>
<text class="stack" x="60" y="205" font-family="{MONO}" font-size="20" fill="#e6f0ff">{STACK}</text>
<g class="logo">
<circle class="ring" cx="990" cy="170" r="104" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="3" stroke-dasharray="14 12"/>
<circle cx="990" cy="170" r="86" fill="#0d1117"/>
<text x="990" y="200" text-anchor="middle" font-family="{MONO}" font-size="92" font-weight="700" fill="#5b9dff">{MONOGRAM}</text>
</g>
<path class="w1" d="{wave(300, 45)}" fill="{bg}" fill-opacity=".45"/>
<path class="w2" d="{wave(335, 30)}" fill="{bg}"/>
</svg>
"""


# --------------------------------------------------------------------------
# Pixel-art room (original artwork, 6px "pixels")
# --------------------------------------------------------------------------
def room():
    P = 6
    GW, GH = 200, 64
    out = []

    def r(x, y, w, h, fill, cls="", extra=""):
        c = f' class="{cls}"' if cls else ""
        out.append(f'<rect{c} x="{x * P}" y="{y * P}" width="{w * P}" height="{h * P}" fill="{fill}"{extra}/>')

    def group(cls, fn):
        out.append(f'<g class="{cls}">')
        fn()
        out.append("</g>")

    # wall + floor
    r(0, 0, GW, GH, "#1a1f3d")
    for y in range(0, 46, 4):
        r(0, y, GW, 1, "#1d2346")
    r(0, 52, GW, 12, "#14172e")

    # window with night sky
    r(10, 6, 40, 28, "#2e3770")
    r(12, 8, 36, 24, "#0b1030")
    r(29, 8, 2, 24, "#2e3770")
    r(12, 19, 36, 2, "#2e3770")
    for (x, y, w) in [(38, 10, 4), (37, 11, 6), (37, 12, 6), (38, 13, 4)]:
        r(x, y, w, 1, "#f5e6a8")
    r(39, 11, 1, 1, "#d9c780")
    for i, (x, y) in enumerate([(15, 10), (22, 12), (26, 9), (17, 15), (33, 16), (44, 15), (14, 23),
                                (21, 26), (35, 24), (42, 28), (25, 29), (46, 23)]):
        r(x, y, 1, 1, "#ffffff", f"tw tw{i % 4}")
    # cloud drifting across window
    out.append('<g clip-path="url(#win)"><g class="cloud">')
    r(14, 26, 8, 2, "#2a3266"); r(16, 25, 4, 1, "#2a3266")
    out.append("</g></g>")

    # neon sign
    out.append(f'<text class="neon" x="{86 * P}" y="{14 * P}" text-anchor="middle" '
               f'font-family="{MONO}" font-size="66" font-weight="700" fill="#ff4fd8">&lt;/&gt;</text>')
    out.append(f'<text class="neon2" x="{86 * P}" y="{19 * P}" text-anchor="middle" '
               f'font-family="{MONO}" font-size="20" fill="#5ee7ff" letter-spacing="6">BUILD · SHIP · REPEAT</text>')

    # shelves with tech blocks + plant
    for sy in (14, 26):
        r(140, sy, 46, 1, "#6b4a3a")
        r(142, sy + 1, 1, 2, "#4a3328"); r(183, sy + 1, 1, 2, "#4a3328")
    blocks = [(143, "#02569B", "F"), (150, "#0175C2", "D"), (157, "#00599C", "C+"), (164, "#3178C6", "TS")]
    for x, col, lab in blocks:
        r(x, 9, 6, 5, col)
        r(x, 9, 6, 1, "#ffffff22")
        out.append(f'<text x="{(x + 3) * P}" y="{12.8 * P}" text-anchor="middle" font-family="{MONO}" '
                   f'font-size="16" font-weight="700" fill="#fff">{lab}</text>')
    # plant (sways)
    out.append(f'<g class="sway" style="transform-origin:{176 * P}px {14 * P}px">')
    for (x, y, w) in [(176, 7, 1), (174, 8, 2), (177, 8, 2), (173, 9, 2), (176, 9, 1), (178, 10, 2), (175, 10, 1)]:
        r(x, y, w, 1, "#3fbf6f")
    out.append("</g>")
    r(174, 11, 5, 3, "#b5654a")
    # books
    for i, col in enumerate(["#e0b03a", "#7f77dd", "#5dcaa5", "#e24b4a", "#378add"]):
        r(144 + i * 2, 21 + (i % 2), 2, 5 - (i % 2), col)
    r(160, 23, 8, 3, "#9a7b4f")  # box
    r(172, 20, 6, 6, "#2b2f55"); r(173, 21, 4, 3, "#5ee7ff", "led")  # tiny screen

    # desk
    r(36, 44, 130, 2, "#7a5442")
    r(36, 46, 130, 1, "#5b3d30")
    r(40, 47, 2, 6, "#5b3d30"); r(160, 47, 2, 6, "#5b3d30")

    # PC tower under desk
    r(144, 47, 10, 6, "#262a4d")
    r(146, 48, 1, 1, "#39d353", "led")
    r(148, 48, 1, 1, "#ff4fd8", "led2")

    # main monitor
    r(66, 22, 44, 21, "#3a4175")
    r(68, 24, 40, 17, "#0d1117")
    r(86, 43, 4, 1, "#3a4175"); r(82, 44, 12, 0.5, "#3a4175")
    code = [(70, 26, 14, "#ff7b72"), (72, 28, 22, "#79c0ff"), (72, 30, 17, "#d2a8ff"),
            (74, 32, 26, "#a5d6ff"), (74, 34, 12, "#7ee787"), (72, 36, 19, "#ffa657"), (70, 38, 8, "#ff7b72")]
    for i, (x, y, w, col) in enumerate(code):
        r(x, y, w, 1, col, f"code c{i}")
    r(70, 38, 1, 1, "#ffffff", "cur2")

    # laptop / phone preview running a Flutter-ish app
    r(114, 32, 18, 12, "#3a4175")
    r(115, 33, 16, 10, "#e8eefc")
    r(115, 33, 16, 2, "#02569B")
    r(117, 37, 5, 4, "#5b9dff", "bounce")
    r(124, 37, 5, 1, "#9aa8c8"); r(124, 39, 4, 1, "#9aa8c8")

    # coffee + steam
    r(140, 40, 6, 4, "#e8eefc"); r(146, 41, 1, 2, "#e8eefc"); r(141, 40, 4, 1, "#6b4a3a")
    for i, x in enumerate((141, 143, 145)):
        r(x, 38, 1, 1, "#c9d1e6", f"steam s{i}")

    # desk lamp
    r(48, 30, 1, 14, "#8b93c4")
    r(46, 28, 6, 2, "#8b93c4")
    out.append(f'<polygon class="glow" points="{46 * P},{30 * P} {52 * P},{30 * P} {62 * P},{44 * P} {38 * P},{44 * P}" fill="#f5e6a8"/>')

    # keyboard
    r(76, 42, 22, 2, "#2b2f55")
    for k in range(10):
        r(77 + k * 2, 42.5, 1, 0.6, "#5d64a0")

    # the dev (back view) on a chair
    r(82, 46, 14, 2, "#222642")          # seat
    r(88, 48, 2, 4, "#222642")           # stem
    r(84, 52, 10, 1, "#222642")          # base
    r(83, 34, 12, 12, "#5b4bb7")         # hoodie
    r(84, 35, 10, 1, "#6d5ed0")
    r(86, 26, 8, 8, "#2a1a14")           # hair
    r(85, 28, 1, 4, "#2a1a14"); r(94, 28, 1, 4, "#2a1a14")
    r(87, 25, 5, 1, "#3a261d")
    r(89, 24, 1, 1, "#2a1a14", "hairtip")
    r(93, 30, 1, 2, "#e0a98a")           # ear
    r(88, 33, 4, 1, "#e0a98a")           # neck
    group("armL", lambda: (r(80, 37, 3, 6, "#4a3d9a"), r(80, 42, 3, 1, "#e0a98a")))
    group("armR", lambda: (r(95, 37, 3, 6, "#4a3d9a"), r(95, 42, 3, 1, "#e0a98a")))

    # sleeping cat on the floor, tail wagging
    r(110, 50, 12, 3, "#9aa0b8"); r(119, 48, 4, 3, "#9aa0b8")
    r(119, 47, 1, 1, "#9aa0b8"); r(122, 47, 1, 1, "#9aa0b8")
    r(120, 49, 1, 0.4, "#2b2f55"); r(122, 49, 0.6, 0.4, "#2b2f55")
    out.append(f'<g class="tail" style="transform-origin:{110 * P}px {51 * P}px">')
    r(105, 50, 5, 1, "#9aa0b8"); r(104, 49, 1, 1, "#9aa0b8")
    out.append("</g>")
    out.append(f'<text class="zz" x="{124 * P}" y="{46 * P}" font-family="{MONO}" font-size="18" fill="#8b93c4">z</text>')

    css = [
        f"rect{{shape-rendering:crispEdges}}",
        "@keyframes tw{50%{opacity:.15}}.tw{animation:tw 2.4s steps(2) infinite}",
        ".tw1{animation-delay:-.6s}.tw2{animation-delay:-1.2s}.tw3{animation-delay:-1.8s}",
        "@keyframes cloud{from{transform:translateX(-80px)}to{transform:translateX(260px)}}",
        ".cloud{animation:cloud 22s linear infinite}",
        "@keyframes neon{0%,18%,22%,62%,64%,100%{opacity:1}20%,63%{opacity:.35}}",
        ".neon{animation:neon 4s infinite}.neon2{animation:neon 5s -1.3s infinite}",
        ".code{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:type 7s steps(8) infinite}",
        "@keyframes type{0%{transform:scaleX(0)}12%,92%{transform:scaleX(1)}100%{transform:scaleX(0)}}",
    ]
    for i in range(len(code)):
        css.append(f".c{i}{{animation-name:t{i}}}"
                   f"@keyframes t{i}{{0%,{i * 11}%{{transform:scaleX(0)}}"
                   f"{i * 11 + 9}%,92%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}")
    css += [
        "@keyframes blink{50%{opacity:0}}.cur2{animation:blink .8s steps(1) infinite}",
        "@keyframes typeL{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}",
        ".armL{animation:typeL .32s steps(1) infinite}.armR{animation:typeL .32s steps(1) -.16s infinite}",
        "@keyframes bob{50%{transform:translateY(-6px)}}.hairtip{animation:bob 1.3s steps(1) infinite}",
        "@keyframes steam{0%{transform:translateY(0);opacity:0}30%{opacity:.9}100%{transform:translateY(-36px);opacity:0}}",
        ".steam{animation:steam 2.4s linear infinite}.s1{animation-delay:-.8s}.s2{animation-delay:-1.6s}",
        "@keyframes glow{0%,100%{opacity:.10}50%{opacity:.16}}.glow{animation:glow 3s ease-in-out infinite}",
        "@keyframes led{50%{opacity:.2}}.led{animation:led 1.1s steps(1) infinite}.led2{animation:led .7s steps(1) -.3s infinite}",
        "@keyframes bounce{50%{transform:translateY(-6px)}}.bounce{animation:bounce 1s ease-in-out infinite}",
        "@keyframes sway{50%{transform:rotate(4deg)}}.sway{animation:sway 3s ease-in-out infinite}",
        "@keyframes tail{0%,100%{transform:rotate(0)}50%{transform:rotate(-14deg)}}.tail{animation:tail 1.6s steps(3) infinite}",
        "@keyframes zz{0%{transform:translate(0,0);opacity:0}30%{opacity:1}100%{transform:translate(24px,-30px);opacity:0}}",
        ".zz{animation:zz 3s linear infinite}",
    ]

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{GW * P}" height="{GH * P}" viewBox="0 0 {GW * P} {GH * P}">
<defs><clipPath id="win"><rect x="{12 * P}" y="{8 * P}" width="{36 * P}" height="{24 * P}"/></clipPath></defs>
<style>{''.join(css)}</style>
{''.join(out)}
</svg>
"""


if __name__ == "__main__":
    for mode in ("dark", "light"):
        with open(f"assets/banner-{mode}.svg", "w", encoding="utf-8") as f:
            f.write(banner(mode))
    with open("assets/room.svg", "w", encoding="utf-8") as f:
        f.write(room())
    print("wrote assets/banner-dark.svg, assets/banner-light.svg, assets/room.svg")
