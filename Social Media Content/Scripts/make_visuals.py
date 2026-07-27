#!/usr/bin/env python3
"""Myers packet-style social graphics — 1080x1350 (4:5)."""
import base64, io, cairosvg
from PIL import Image, ImageOps

GOLD = "#C9972C"; GOLD_BAND = "#D6A73F"; GOLD_LT = "#E8C96A"
CREAM = "#FBF5E6"; INK = "#1A1A1A"; GRAY = "#6B7280"; WHITE = "#FFFFFF"
FONT = "Liberation Sans"
W, H = 1080, 1350
MYERS = "/sessions/gifted-focused-wright/mnt/Myers Data Base/Myers "

def b64img(path, max_w=1600):
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if img.width > max_w:
        img = img.resize((max_w, int(img.height * max_w / img.width)), Image.LANCZOS)
    buf = io.BytesIO(); img.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode(), img.size

def b64png(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()

LOGO = b64png(MYERS + "/MHB_Logo_4C-Pos (2).png")
CARROT = b64png("/sessions/gifted-focused-wright/mnt/outputs/carrot-logo.png")

def header(kicker):
    return f'''
  <image x="64" y="52" width="230" height="76" href="{LOGO}" preserveAspectRatio="xMinYMid meet"/>
  <text x="{W-64}" y="100" text-anchor="end" font-family="{FONT}" font-weight="bold"
        font-size="26" letter-spacing="6" fill="{GOLD}">{kicker}</text>
  <rect x="64" y="148" width="{W-128}" height="3" fill="{GOLD_BAND}"/>'''

def footer():
    return f'''
  <rect x="64" y="{H-90}" width="{W-128}" height="2" fill="#E8E8E5"/>
  <text x="{W/2}" y="{H-42}" text-anchor="middle" font-family="{FONT}" font-size="24"
        fill="{GRAY}">Myers Home Buyers · Where Agents Become Investors · joinmyers.com</text>'''

def photo_card(path, x, y, w, h, rid):
    data, (iw, ih) = b64img(path)
    return f'''
  <clipPath id="{rid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24"/></clipPath>
  <image x="{x}" y="{y}" width="{w}" height="{h}" href="{data}"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#{rid})"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="none" stroke="{GOLD_BAND}" stroke-width="3"/>'''

def stat_band(y, stats, h=170):
    n = len(stats); cw = (W - 128) / n
    cells = ""
    for i, (big, small) in enumerate(stats):
        cx = 64 + cw * i + cw / 2
        if i: cells += f'<rect x="{64+cw*i}" y="{y+38}" width="2" height="{h-76}" fill="#00000022"/>'
        cells += f'''
  <text x="{cx}" y="{y+h/2+2}" text-anchor="middle" font-family="{FONT}" font-weight="bold"
        font-size="54" fill="{INK}">{big}</text>
  <text x="{cx}" y="{y+h/2+52}" text-anchor="middle" font-family="{FONT}" font-weight="bold"
        font-size="21" letter-spacing="2.5" fill="#5b4310">{small}</text>'''
    return f'<rect x="64" y="{y}" width="{W-128}" height="{h}" rx="18" fill="{GOLD_BAND}"/>' + cells

def two_tone(x, y, size, black, gold, anchor="start"):
    return f'''<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{FONT}"
    font-weight="bold" font-size="{size}" fill="{INK}">{black}<tspan fill="{GOLD}">{gold}</tspan></text>'''

from PIL import ImageFont
_FP = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
def two_tone_center(cx, y, size, black, gold):
    total = ImageFont.truetype(_FP, size).getlength(black + gold)
    x0 = cx - total/2
    return (f'<text x="{x0}" y="{y}" text-anchor="start" font-family="{FONT}" '
            f'font-weight="bold" font-size="{size}" fill="{INK}">{black}'
            f'<tspan fill="{GOLD}">{gold}</tspan></text>')

def render(name, body):
    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{WHITE}"/>{body}{footer()}</svg>'''
    cairosvg.svg2png(bytestring=svg.encode(), write_to=f"/sessions/gifted-focused-wright/mnt/outputs/{name}.png",
                     output_width=W, output_height=H)
    print("rendered", name)

# ---------- 1. FLIP REVEAL ----------
body = header("AGENT WIN")
body += two_tone(64, 226, 58, "This Is What Our Agents", "")
body += two_tone(64, 296, 58, "Do... ", "Themselves.")
body += f'<text x="64" y="348" font-family="{FONT}" font-size="29" fill="{GRAY}">Cynthia O. took this Garland house down to the studs — now it&#8217;s a stunner.</text>'
body += photo_card(MYERS + "/../Agent Marketing/Cynthia_Before_1708 High Point Cir, Garland, TX 75041/1 Before.jpg", 64, 386, W-128, 566, "p1")
body += f'''<rect x="84" y="406" width="210" height="64" rx="12" fill="{INK}" opacity="0.85"/>
  <text x="189" y="448" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="30"
        letter-spacing="4" fill="{GOLD_LT}">BEFORE</text>'''
body += stat_band(990, [("$450K", "LIST PRICE"), ("ALL-NEW", "HVAC · ELEC · PLUMB"), ("GARLAND", "1708 HIGH POINT CIR")])
body += f'<text x="{W/2}" y="1215" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="34" fill="{INK}">Swipe for the befores &#8594;</text>'
render("v1-flip-reveal", body)

# ---------- 2. MYERS x CARROT ----------
body = header("PARTNERSHIP ANNOUNCEMENT")
# Myers + Carrot logo lockup
body += f'<image x="150" y="196" width="300" height="96" href="{LOGO}" preserveAspectRatio="xMidYMid meet"/>'
body += f'<text x="{W/2}" y="262" text-anchor="middle" font-family="{FONT}" font-size="52" fill="{GRAY}">&#215;</text>'
body += f'<image x="590" y="196" width="340" height="96" href="{CARROT}" preserveAspectRatio="xMidYMid meet"/>'
body += two_tone_center(W/2, 372, 56, "Most Brokerages Hire Agents.", "")
body += two_tone_center(W/2, 442, 56, "We Build ", "Entrepreneurs.")
body += f'''<rect x="64" y="490" width="{W-128}" height="352" rx="24" fill="{CREAM}" stroke="{GOLD_BAND}" stroke-width="3"/>
  <text x="{W/2}" y="566" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="30" letter-spacing="5" fill="{GOLD}">THE ENGINE</text>
  <text x="{W/2}" y="636" text-anchor="middle" font-family="{FONT}" font-size="32" fill="{INK}">An AI-powered lead engine that finds sellers,</text>
  <text x="{W/2}" y="684" text-anchor="middle" font-family="{FONT}" font-size="32" fill="{INK}">scores who&#8217;s ready, and follows up for you.</text>
  <text x="{W/2}" y="756" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="33" fill="{INK}">Ownership + AI = A Business That Runs</text>
  <text x="{W/2}" y="800" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="33" fill="{INK}">While You Build It.</text>'''
body += f'<text x="{W/2}" y="898" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="27" letter-spacing="2" fill="{GRAY}">CARROT&#8217;S PLATFORM TRACK RECORD</text>'
body += stat_band(920, [("1M+", "SELLER LEADS"), ("40K+", "LEADS / MONTH"), ("7x", "CONVERSION"), ("2.5x", "PROFIT / DEAL")])
body += f'<text x="{W/2}" y="1140" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GRAY}" font-style="italic">Source: Carrot platform data, not Myers results. Individual results vary.</text>'
render("v2-carrot", body)

# ---------- 3. JESSE DOUBLE-SIDE ----------
body = header("AGENT WIN")
body += two_tone(64, 236, 56, "One Agent. ", "Both Sides of the Deal.")
body += f'<text x="64" y="292" font-family="{FONT}" font-size="30" fill="{GRAY}">Jesse Wang acquired it, then sold it to his investor &#8212; squatter and all.</text>'
body += photo_card("/sessions/gifted-focused-wright/mnt/outputs/jesse-4x5.jpg", 280, 330, 520, 650, "p3")
pills = [("ACQUIRED IT", 355), ("SOLD IT", 505), ("SQUATTER? HANDLED.", 655)]
for label, y in pills:
    body += f'''<rect x="64" y="{y}" width="190" height="98" rx="16" fill="{CREAM}" stroke="{GOLD_BAND}" stroke-width="2.5"/>'''
body += f'''
  <text x="159" y="412" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="24" fill="{INK}">ACQUIRED</text>
  <text x="159" y="440" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="24" fill="{GOLD}">IT</text>
  <text x="159" y="562" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="24" fill="{INK}">SOLD</text>
  <text x="159" y="590" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="24" fill="{GOLD}">IT</text>
  <text x="159" y="700" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="22" fill="{INK}">SQUATTER?</text>
  <text x="159" y="728" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="22" fill="{GOLD}">HANDLED.</text>'''
body += stat_band(1030, [("2x", "COMMISSION SIDES"), ("1836", "TITLE PARTNER"), ("DFW", "OFF-MARKET DEAL")])
render("v3-jesse", body)

# ---------- 4. CROWN POINT ----------
def stars(cx, y, size=44, gap=14, fill=GOLD):
    pts="0,-1 0.225,-0.309 0.951,-0.309 0.363,0.118 0.588,0.809 0,0.382 -0.588,0.809 -0.363,0.118 -0.951,-0.309 -0.225,-0.309"
    out=""
    total=5*size+4*gap; startx=cx-total/2+size/2
    for i in range(5):
        x=startx+i*(size+gap)
        out+=f'<polygon points="{pts}" transform="translate({x},{y}) scale({size/2})" fill="{fill}"/>'
    return out
body = header("HAPPY SELLERS")
body += two_tone_center(W/2, 244, 60, "Another Happy DFW Family", "")
body += f'<text x="{W/2}" y="300" text-anchor="middle" font-family="{FONT}" font-size="29" fill="{GRAY}">Our Crown Point sellers closed with 1836 Title, on their own timeline.</text>'
body += photo_card("/sessions/gifted-focused-wright/mnt/outputs/crownpoint-4x5.jpg", 240, 340, 600, 640, "p4")
body += stars(W/2, 1032, size=50)
body += stat_band(1074, [("$0", "REPAIRS"), ("$0", "FEES"), ("3,000+", "DFW DEALS CLOSED")], h=158)
render("v4-crownpoint", body)
