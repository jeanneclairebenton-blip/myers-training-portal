#!/usr/bin/env python3
"""Myers packet-style Sponsorship post. 1080x1350."""
import base64, cairosvg
from PIL import ImageFont
GOLD="#C9972C"; GOLD_BAND="#D6A73F"; GOLD_LT="#E8C96A"
CREAM="#FBF5E6"; INK="#1A1A1A"; GRAY="#6B7280"; WHITE="#FFFFFF"
FONT="Liberation Sans"; W,H=1080,1350
MYERS="/sessions/gifted-focused-wright/mnt/Myers Data Base/Myers Branding"
LOGO="data:image/png;base64,"+base64.b64encode(open(MYERS+"/MHB_Logo_4C-Pos (2).png",'rb').read()).decode()
_FP="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
def tt_center(cx,y,size,black,gold):
    total=ImageFont.truetype(_FP,size).getlength(black+gold); x0=cx-total/2
    return f'<text x="{x0}" y="{y}" text-anchor="start" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="{INK}">{black}<tspan fill="{GOLD}">{gold}</tspan></text>'
def check(x,y,col=GOLD):
    return f'<path d="M{x} {y} l9 9 l16 -18" stroke="{col}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'

body=f'<image x="64" y="52" width="230" height="76" href="{LOGO}" preserveAspectRatio="xMinYMid meet"/>'
body+=f'<text x="{W-64}" y="100" text-anchor="end" font-family="{FONT}" font-weight="bold" font-size="26" letter-spacing="4" fill="{GOLD}">PARTNER WITH MYERS</text>'
body+=f'<rect x="64" y="148" width="{W-128}" height="3" fill="{GOLD_BAND}"/>'
body+=tt_center(W/2,228,52,"Get In Front of ","Our Agents.")
body+=f'<text x="{W/2}" y="284" text-anchor="middle" font-family="{FONT}" font-size="27" fill="{GRAY}">Biweekly trainings &amp; events. Real face time &#8212; not a logo lost in a feed.</text>'

def package(x, w, tier, price, bullets, featured):
    top=330; band_h=118; box_h=618
    out=f'<rect x="{x}" y="{top}" width="{w}" height="{box_h}" rx="22" fill="{WHITE}" stroke="{GOLD_BAND}" stroke-width="{4 if featured else 3}"/>'
    bandfill=GOLD_BAND if featured else INK
    txtcol=INK if featured else WHITE
    # rounded top band
    out+=f'<path d="M{x+2} {top+band_h} L{x+2} {top+22} Q{x+2} {top+2} {x+22} {top+2} L{x+w-22} {top+2} Q{x+w-2} {top+2} {x+w-2} {top+22} L{x+w-2} {top+band_h} Z" fill="{bandfill}"/>'
    if featured:
        out+=f'<rect x="{x+w-160}" y="{top-16}" width="150" height="34" rx="17" fill="{INK}"/>'
        out+=f'<text x="{x+w-85}" y="{top+8}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="18" letter-spacing="2" fill="{GOLD_LT}">BEST VALUE</text>'
    out+=f'<text x="{x+w/2}" y="{top+46}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="26" letter-spacing="2" fill="{txtcol}">{tier}</text>'
    out+=f'<text x="{x+w/2}" y="{top+96}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="40" fill="{txtcol}">{price} <tspan font-size="20" font-weight="normal">/ event</tspan></text>'
    by=top+band_h+44
    for b in bullets:
        bold = b.endswith(":")
        out+=check(x+24, by-8)
        out+=f'<text x="{x+62}" y="{by}" font-family="{FONT}" font-size="22" font-weight="{"bold" if bold else "normal"}" fill="{INK if bold else "#333"}">{b}</text>'
        by+=52
    return out

body+=package(64, 456, "COMMUNITY", "$250",
    ["Logo on flyer &amp; email blast","Tagged in every event post","Network with agents live","Agent contact list for you"], False)
body+=package(560, 456, "FEATURED", "$500",
    ["Everything in Community, plus:","Teach a 1-hour class","Opt-in attendee sign-up list","Dedicated post + recap logo","Be the expert, not the seller"], True)

body+=f'<text x="{W/2}" y="1010" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="25" fill="{GOLD}">Book 4 events, save 10%  ·  Annual Partner program: 3 partners, 1 per industry</text>'
# CTA button
by=1044; bh=118
body+=f'<rect x="120" y="{by}" width="{W-240}" height="{bh}" rx="24" fill="{INK}"/>'
body+=f'<text x="{W/2}" y="{by+52}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="38" fill="{WHITE}">Reserve Your Event  &#8594;</text>'
body+=f'<text x="{W/2}" y="{by+90}" text-anchor="middle" font-family="{FONT}" font-size="23" fill="{GOLD_LT}">DM us or email jeanneclairebenton@gmail.com</text>'
body+=f'<rect x="64" y="{H-90}" width="{W-128}" height="2" fill="#E8E8E5"/>'
body+=f'<text x="{W/2}" y="{H-42}" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GRAY}">Myers Home Buyers · One published rate card, same for every partner · joinmyers.com</text>'

svg=f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{WHITE}"/>{body}</svg>'
cairosvg.svg2png(bytestring=svg.encode(),write_to="/sessions/gifted-focused-wright/mnt/outputs/v9-sponsorship.png",output_width=W,output_height=H)
print("rendered v9-sponsorship")
