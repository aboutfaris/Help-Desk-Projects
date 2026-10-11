#!/usr/bin/env python3
"""340 Collective reference design: Remote Worker Network (fictional).

Adapted from Career/Experience/340Collective/Templates/aws_architecture_template.py.
Standard: .kiro/steering/aws-architecture-diagram-style.md (owner-approved 2026-10-03).
Only the blocks marked EDIT differ from the template, plus the boundary label text
("Home network" instead of "AWS Cloud"), because the one boundary here is a home LAN.

This is a vendor-neutral, fictional work-from-home reference design. It shows roles and
RFC1918 subnets only: no device models, hardware identifiers, public addresses,
hostnames, or credentials.

Set up once:  python3 -m venv /tmp/c340_diag_venv
              /tmp/c340_diag_venv/bin/pip install diagrams==0.25.1   (official AWS icons)
              brew install librsvg                                    (rsvg-convert)
Run:          /tmp/c340_diag_venv/bin/python build_home_network_segmentation.py <out-prefix>
It writes <out-prefix>.svg and <out-prefix>.png (rendered at 2x).
"""
import base64
import os
import subprocess
import sys

import diagrams

R = os.path.join(os.path.dirname(os.path.dirname(diagrams.__file__)), "resources")
OUT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/arch"
OUT_SVG, OUT_PNG = OUT + ".svg", OUT + ".png"

# ---------------- style: owner-approved, keep as is ----------------
FONT = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, TEXT2, LINE, GROUP, BADGE, ORANGE, RULE, ACCENT = (
    "#232F3E", "#545B64", "#3F4752", "#7D8998", "#146EB4", "#FF9900", "#E3E6EA", "#8C4FFF")
ICON, HALF = 52, 26
KINDS = {  # stroke, width, dash, arrowhead marker, legend label
    "service": (LINE, 1.6, None, "ah", "AWS service flow"),
    "external": (LINE, 1.6, "6 5", "ah", "External party or control action"),
    "business": (ACCENT, 2.2, None, "ahb", "Business flow"),
}

# ---------------- EDIT: canvas text ----------------
W, H = 1900, 1070
TITLE = "Remote Worker Network"
SUBTITLE = ("340 Collective reference design for a secure remote worker. A fictional example: "
            "five isolated VLANs, a single NAT edge, and a private mesh VPN.")
BOUNDARY_LABEL = "Home network"
REGION = "on premises, RFC1918 addressing"
FOOTER_LEFT, FOOTER_RIGHT = "340 Collective", "October 2026"
# legend wording for this diagram (same strokes, widths, dashes, and markers as the standard)
KINDS = {k: v[:4] + (lab,) for (k, v), lab in zip(KINDS.items(), (
    "Network data flow",
    "Inbound port forward or encrypted VPN tunnel",
    "Management access (Personal segment only)"))}

out, icons, SEGS, BADGES = [], [], [], []
N, BOX, USED = {}, {}, set()


def add(s):
    out.append(s)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def est_w(s, size):
    return len(s) * size * 0.53


def text(x, y, s, size=13, weight=400, color=INK, anchor="middle", halo=False):
    h = (' stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round" paint-order="stroke"'
         if halo else "")
    add(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
        f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{h}>{esc(s)}</text>')


_cache = {}


def data(rel):
    if rel not in _cache:
        with open(os.path.join(R, rel), "rb") as fh:
            _cache[rel] = "data:image/png;base64," + base64.b64encode(fh.read()).decode()
    return _cache[rel]


def node(key, rel, cx, cy, l1, l2=None):
    """Register an icon at slot (cx, cy) with a service name and an optional role line."""
    assert key not in N, key
    N[key] = (cx, cy, 2 if l2 else 1)
    icons.append((rel, cx, cy, l1, l2))
    w = max(ICON, est_w(l1, 13), est_w(l2 or "", 12))
    BOX[key] = (cx - w / 2, cy - HALF, cx + w / 2, cy + HALF + (36 if l2 else 21))


def draw_nodes():
    for rel, cx, cy, l1, l2 in icons:
        add(f'<image x="{cx-HALF}" y="{cy-HALF}" width="{ICON}" height="{ICON}" '
            f'xlink:href="{data(rel)}"/>')
        text(cx, cy + HALF + 17, l1, 13, 400, INK)
        if l2:
            text(cx, cy + HALF + 32, l2, 12, 400, TEXT2)


def port(key, side, gap=5):
    """Connection point: l, r, t (top edge of icon), b (below the label block)."""
    cx, cy, n = N[key]
    return {"l": (cx - HALF - gap, cy), "r": (cx + HALF + gap, cy),
            "t": (cx, cy - HALF - gap),
            "b": (cx, cy + HALF + (36 if n == 2 else 21) + gap)}[side]


def path(pts, a, b, kind="service"):
    color, width, dash, marker, _ = KINDS[kind]
    USED.add(kind)
    for p, q in zip(pts, pts[1:]):
        assert p[0] == q[0] or p[1] == q[1], ("diagonal segment", a, b, p, q)
        SEGS.append((p, q, a, b))
    d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{da} '
        f'marker-end="url(#{marker})"/>')


def link(a, sa, b, sb, kind="service", via=None):
    """Connect two nodes. via = elbow points; every segment must be horizontal or vertical."""
    path([port(a, sa)] + (via or []) + [port(b, sb)], a, b, kind)


def badge(cx, cy, n, record=True):
    if record:
        BADGES.append((cx, cy, n))
    add(f'<rect x="{cx-12}" y="{cy-12}" width="24" height="24" rx="3" fill="{BADGE}"/>')
    text(cx, cy + 4.6, str(n), 13, 700, "#FFFFFF")


def group(x0, y0, x1, y1, title):
    add(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" '
        f'stroke="{GROUP}" stroke-width="1.3" stroke-dasharray="5 4"/>')
    text(x0 + 14, y0 + 25, title, 14.5, 700, INK, "start")


# ---------------- EDIT: grid ----------------
AX0, AX1, AY0, AY1 = 230, 1670, 110, 790             # the one boundary (home network)
COLS = [(260, 696), (732, 1168), (1204, 1640)]        # group columns
SL = [[round(x0 + (x1 - x0) * f) for f in (0.2, 0.5, 0.8)] for x0, x1 in COLS]  # icon slots
ROWS = [(190, 490), (566, 760)]                       # group rows (row 2 has one lane)
A0, B0, A1 = 280, 410, 656                            # icon lanes (center y)
XL, XR, CH = 115, 1785, 162                           # external columns, top channel y
GP, GF = 504, 548                                     # row gutter: admin line, VLAN fan-out

# ---------------- canvas and the one boundary ----------------
add(f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
    f'width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs>'
    '<marker id="ah" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6.5" '
    f'markerHeight="6.5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/></marker>'
    '<marker id="ahb" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" '
    f'markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{ACCENT}"/></marker>'
    '</defs>')
add(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
text(40, 56, TITLE, 26, 700, INK, "start")
text(40, 82, SUBTITLE, 14, 400, TEXT2, "start")
add(f'<rect x="{AX0}" y="{AY0}" width="{AX1-AX0}" height="{AY1-AY0}" fill="none" '
    f'stroke="{INK}" stroke-width="1.6"/>')
add(f'<rect x="{AX0}" y="{AY0}" width="32" height="32" fill="{INK}"/>')
text(AX0 + 16, AY0 + 16, "aws", 12, 700, "#FFFFFF")
add(f'<path d="M {AX0+7},{AY0+21} Q {AX0+16},{AY0+27} {AX0+25},{AY0+21}" fill="none" '
    f'stroke="{ORANGE}" stroke-width="2" stroke-linecap="round"/>')
add(f'<path d="M {AX0+21.5},{AY0+19.5} L {AX0+25.5},{AY0+20.5} L {AX0+24.5},{AY0+24.5}" '
    f'fill="none" stroke="{ORANGE}" stroke-width="1.6" stroke-linecap="round" '
    f'stroke-linejoin="round"/>')
add(f'<text x="{AX0+44}" y="{AY0+21}" font-family="{FONT}" font-size="14.5" '
    f'font-weight="700" fill="{INK}">{esc(BOUNDARY_LABEL)}<tspan dx="10" font-weight="400" '
    f'fill="{TEXT2}">{esc(REGION)}</tspan></text>')

# ---------------- EDIT: groups, (column, row) -> title ----------------
GROUPS = {
    (0, 0): "Personal, 192.168.1.0/24", (1, 0): "WAN edge", (2, 0): "Work, 192.168.3.0/24",
    (0, 1): "Family, 192.168.4.0/24", (1, 1): "IoT, 192.168.5.0/24",
    (2, 1): "Guest, 192.168.2.0/24",
}
for (c, r), title in GROUPS.items():
    (x0, x1), (y0, y1) = COLS[c], ROWS[r]
    group(x0, y0, x1, y1, title)
    # register the title so the line, label, and badge checks also cover group titles
    BOX["title:" + title] = (x0 + 14, y0 + 12, x0 + 14 + est_w(title, 14.5), y0 + 30)

# ---------------- EDIT: nodes ----------------
GEN = "aws/general/"
NET = "aws/network/"
PAD = GEN + "ssl-padlock.png"

# outside the boundary: the ISP side and the remote mesh peers
node("inet", GEN + "internet-alt1.png", XR, CH, "Internet", "ISP uplink")
node("peers", GEN + "mobile-client.png", XL, A0, "Remote peers", "private mesh VPN")
# WAN edge: bridged modem, then the one router that does NAT, firewall, DHCP, and VLANs.
# The padlock tiles are edge policy facts, not extra devices.
node("modem", NET + "internet-gateway.png", SL[1][1], A0, "Cable modem", "bridged, no Wi-Fi")
node("nat", PAD, SL[1][0], A0, "Single NAT", "on the edge router")
node("deny", PAD, SL[1][2], A0, "WAN default-deny", "router policy, no admin")
node("router", NET + "vpc-router.png", SL[1][1], B0, "Edge router / firewall",
     "DHCP, VLAN trunk")
# Personal segment: trusted devices and the VPN exit node / subnet router
node("exit", NET + "site-to-site-vpn.png", SL[0][2], A0, "VPN exit node", "subnet router")
node("pdev", GEN + "client.png", SL[0][2], B0, "Personal devices", "laptop, phone")
# the other four segments, one client role each
node("work", GEN + "client.png", SL[2][0], B0, "Work laptop", "employer-managed")
node("family", GEN + "users.png", SL[0][1], A1, "Family devices", "phones, tablets")
node("iot", "aws/iot/iot-house.png", SL[1][1], A1, "Smart-home devices", "cameras, plugs")
node("guest", GEN + "user.png", SL[2][1], A1, "Guest devices", "internet only")

# ---------------- EDIT: connections (kind: service, external, business) ----------------
P = port
RX, RB = SL[1][1], P("router", "b")[1]          # router column and the y below its label

# ISP uplink: top channel into the bridged modem, then the modem's one cable to the router
link("inet", "l", "modem", "t", via=[(SL[1][1], CH)])
link("modem", "b", "router", "t")
# five VLANs leave the router; each segment reaches only the router (and the internet)
link("router", "l", "pdev", "r")                                                   # Personal
link("router", "r", "work", "l")                                                   # Work
path([(RX - 24, RB), (RX - 24, GF), (SL[0][1], GF), P("family", "t")], "router", "family")
link("router", "b", "iot", "t")                                                    # IoT
path([(RX + 24, RB), (RX + 24, GF), (SL[2][1], GF), P("guest", "t")], "router", "guest")
# the single inbound port forward (one UDP port) to the VPN exit node, dashed
path([(RX - HALF - 5, B0 - 14), (714, B0 - 14), (714, A0), P("exit", "r")],
     "router", "exit", "external")
# encrypted mesh tunnel from remote peers into the exit node, dashed
link("peers", "r", "exit", "l", "external")
# management plane: only the Personal segment reaches the router's admin interface
path([P("pdev", "b"), (SL[0][2], GP), (RX - 48, GP), (RX - 48, RB)], "pdev", "router",
     "business")


# ---------------- EDIT: line labels (white halo keeps them readable over lines) ----------------
def lbl(x, y, s, anchor="start", color=TEXT2):
    """Line label; its box is registered so lines, labels, and badges cannot overlap it."""
    text(x, y, s, 11.5, 400, color, anchor, halo=True)
    w = est_w(s, 11.5)
    x0 = x if anchor == "start" else (x - w / 2 if anchor == "middle" else x - w)
    BOX["lbl:" + s] = (x0, y - 10, x0 + w, y + 3)


lbl(1360, 154, "ISP line")
lbl(942, 370, "WAN", "end")
lbl(868, 388, "one UDP port forward", "end")
lbl(300, 272, "encrypted tunnel")
lbl(648, 524, "admin, Personal only", color=ACCENT)
lbl(1020, 516, "one VLAN each,")
lbl(1020, 532, "cross-traffic dropped")

draw_nodes()

# ---------------- EDIT: step badges (x, y, number), in a gutter beside their line ----------------
for cx, cy, n in [(1330, 138, 1), (976, 356, 2), (1004, 524, 3), (630, 526, 4),
                  (188, 256, 5)]:
    badge(cx, cy, n)

# ---------------- EDIT: legend steps, one short sentence each, same order as the badges ----------------
LY = AY1 + 52
STEPS = [
    "The ISP line enters a cable modem in bridge mode, which passes traffic straight to the router.",
    "The edge router holds the public IP (single NAT) and denies inbound traffic, except one UDP port.",
    "The router splits the home into five VLANs; traffic between segments is dropped.",
    "Only the Personal segment can reach the router's admin interface; other segments are denied.",
    "Remote peers join through an encrypted WireGuard mesh that reaches only the Personal segment.",
]

text(40, LY, "How it works", 16, 700, INK, "start")
per_col = (len(STEPS) + 1) // 2
for i, s in enumerate(STEPS):
    col, row = divmod(i, per_col)
    bx, by = 52 + col * 930, LY + 34 + row * 32
    badge(bx, by, i + 1, record=False)
    text(bx + 22, by + 4.6, s, 13.5, 400, INK, "start")

# line-style key, one entry per line kind actually used
KEY_Y = LY + 40 + per_col * 32
lx = 40
for k, (color, width, dash, marker, label) in KINDS.items():
    if k not in USED:
        continue
    da = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<path d="M {lx},{KEY_Y} L {lx+52},{KEY_Y}" stroke="{color}" stroke-width="{width}"'
        f'{da} marker-end="url(#{marker})"/>')
    text(lx + 62, KEY_Y + 4.5, label, 12.5, 400, TEXT2, "start")
    lx += 62 + est_w(label, 12.5) + 48

RULE_Y = KEY_Y + 26
add(f'<line x1="40" y1="{RULE_Y}" x2="{W-40}" y2="{RULE_Y}" stroke="{RULE}" stroke-width="1"/>')
text(40, RULE_Y + 26, FOOTER_LEFT, 13, 700, INK, "start")
text(W - 40, RULE_Y + 26, FOOTER_RIGHT, 13, 400, TEXT2, "end")
add("</svg>")
assert RULE_Y + 50 <= H, "canvas too short for the legend: raise H"


# ---------------- checks: keep all of them ----------------
def seg_hits_box(p, q, box, pad=2):
    x0, y0, x1, y1 = box
    (ax, ay), (bx, by) = p, q
    if ay == by:
        lo, hi = sorted((ax, bx))
        return y0 - pad < ay < y1 + pad and lo < x1 + pad and hi > x0 - pad
    lo, hi = sorted((ay, by))
    return x0 - pad < ax < x1 + pad and lo < y1 + pad and hi > y0 - pad


def boxes_overlap(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def crossings():
    hs = [s for s in SEGS if s[0][1] == s[1][1]]
    vs = [s for s in SEGS if s[0][0] == s[1][0]]
    found = []
    for hp, hq, ha, hb in hs:
        y = hp[1]
        x0, x1 = sorted((hp[0], hq[0]))
        for vp, vq, va, vb in vs:
            if (ha, hb) == (va, vb):
                continue
            x = vp[0]
            y0, y1 = sorted((vp[1], vq[1]))
            if x0 < x < x1 and y0 < y < y1:
                found.append(f"{ha}->{hb} x {va}->{vb}")
    return found


def shared_segments():
    found = []
    for i in range(len(SEGS)):
        for j in range(i + 1, len(SEGS)):
            (p, q, a, b), (r, s, c, d) = SEGS[i], SEGS[j]
            if (a, b) == (c, d):
                continue
            if p[1] == q[1] == r[1] == s[1]:
                lo1, hi1 = sorted((p[0], q[0]))
                lo2, hi2 = sorted((r[0], s[0]))
            elif p[0] == q[0] == r[0] == s[0]:
                lo1, hi1 = sorted((p[1], q[1]))
                lo2, hi2 = sorted((r[1], s[1]))
            else:
                continue
            if min(hi1, hi2) - max(lo1, lo2) > 0:
                found.append(f"{a}->{b} shares a segment with {c}->{d}")
    return found


problems = []
for p, q, a, b in SEGS:
    for k, box in BOX.items():
        if k not in (a, b) and seg_hits_box(p, q, box):
            problems.append(f"line {a}->{b} crosses {k}")
keys = list(BOX)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        if boxes_overlap(BOX[keys[i]], BOX[keys[j]]):
            problems.append(f"label overlap {keys[i]} / {keys[j]}")
for cx, cy, n in BADGES:
    bb = (cx - 12, cy - 12, cx + 12, cy + 12)
    for p, q, a, b in SEGS:
        if seg_hits_box(p, q, bb, pad=1):
            problems.append(f"badge {n} sits on line {a}->{b}")
    for k, box in BOX.items():
        if boxes_overlap(bb, box):
            problems.append(f"badge {n} overlaps {k}")
for k, (x0, y0, x1, y1) in BOX.items():
    for (c0, c1) in COLS:
        if c0 < (x0 + x1) / 2 < c1 and (x0 < c0 + 4 or x1 > c1 - 4):
            problems.append(f"label of {k} touches its group border")
problems += shared_segments()
X = crossings()
if len(X) > 2:
    problems.append(f"{len(X)} line crossings (2 at most, only where unavoidable)")

svg = "\n".join(out)
assert "\u2014" not in svg and "\u2013" not in svg, "em or en dash found"
with open(OUT_SVG, "w") as fh:
    fh.write(svg)
subprocess.run(["rsvg-convert", "-z", "2", "-o", OUT_PNG, OUT_SVG], check=True)
print("nodes:", len(N), "segments:", len(SEGS), "badges:", len(BADGES))
print("crossings:", len(X), *X)
print("layout problems:", problems if problems else "none")
print("wrote", OUT_SVG, "and", OUT_PNG)
