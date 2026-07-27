#!/usr/bin/env python3
"""Myers 'SOLD' announcement template (New Western style). 1080x1350."""
import base64, io, cairosvg
from PIL import Image, ImageOps
GOLD="#C9972C"; GOLD_LT="#E8C96A"; INK="#1A1A1A"; GRAY="#9AA0A6"; WHITE="#FFFFFF"; FONT="Liberation Sans"
W,H=1080,1350
MYERS="/sessions/gifted-focused-wright/mnt/Myers Data Base/Myers Branding"
def b64(p):
    ext=p.rsplit('.',1)[1].lower(); mime='png' if ext=='png' else 'jpeg'
    return f"data:image/{mime};base64,"+base64.b64encode(open(p,'rb').read()).decode()
def b64img(path,maxw=1400):
    im=ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    buf=io.BytesIO(); im.save(buf,"JPEG",quality=88)
    return "data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()
LOGO_NEG=b64(MYERS+"/MHB_Stacked-Logo_4C-Neg.png")
PHOTO=b64img("/sessions/gifted-focused-wright/mnt/outputs/after-1.jpg")

ph=800  # photo height
body=f'''<defs><clipPath id="pc"><rect x="0" y="0" width="{W}" height="{ph}"/></clipPath>
<clipPath id="head"><circle cx="905" cy="205" r="128"/></clipPath></defs>
<image x="0" y="0" width="{W}" height="{ph}" href="{PHOTO}" preserveAspectRatio="xMidYMid slice" clip-path="url(#pc)"/>'''
# agent headshot placeholder (top-right)
body+=f'<circle cx="905" cy="205" r="134" fill="{WHITE}"/><circle cx="905" cy="205" r="128" fill="#3a3a3a"/>'
body+=f'<text x="905" y="188" text-anchor="middle" font-family="{FONT}" font-size="26" fill="{GRAY}">AGENT</text>'
body+=f'<text x="905" y="222" text-anchor="middle" font-family="{FONT}" font-size="26" fill="{GRAY}">PHOTO</text>'
# dark banner
body+=f'<rect x="0" y="{ph}" width="{W}" height="{H-ph}" fill="{INK}"/>'
# Property Available (struck)
body+=f'<text x="{W/2}" y="{ph+78}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="46" letter-spacing="2" fill="#C9C9C9">Property Available</text>'
body+=f'<line x1="300" y1="{ph+64}" x2="780" y2="{ph+64}" stroke="#8A8A8A" stroke-width="5"/>'
# SOLD!
body+=f'<text x="{W/2}" y="{ph+230}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="150" letter-spacing="6" fill="{GOLD}">SOLD!</text>'
# subline
body+=f'<text x="{W/2}" y="{ph+300}" text-anchor="middle" font-family="{FONT}" font-style="italic" font-size="27" fill="#E8E8E8">Contact me today to request access to our exclusive</text>'
body+=f'<text x="{W/2}" y="{ph+336}" text-anchor="middle" font-family="{FONT}" font-style="italic" font-size="27" fill="#E8E8E8">inventory of off-market investment properties.</text>'
# contact placeholders
body+=f'<text x="300" y="{ph+416}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="28" fill="{GOLD_LT}">(000) 000-0000</text>'
body+=f'<text x="780" y="{ph+416}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="28" fill="{GOLD_LT}">agent@joinmyers.com</text>'
# logo
body+=f'<image x="{W/2-150}" y="{ph+448}" width="300" height="86" href="{LOGO_NEG}" preserveAspectRatio="xMidYMid meet"/>'

svg=f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{INK}"/>{body}</svg>'
cairosvg.svg2png(bytestring=svg.encode(),write_to="/sessions/gifted-focused-wright/mnt/outputs/v10-sold-template.png",output_width=W,output_height=H)
print("rendered v10-sold-template")
