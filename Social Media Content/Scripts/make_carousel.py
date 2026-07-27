#!/usr/bin/env python3
"""Cynthia flip carousel — labeled BEFORE/AFTER cards, 1080x1350 (4:5)."""
import base64, io, cairosvg
from PIL import Image, ImageOps

GOLD="#C9972C"; GOLD_BAND="#D6A73F"; GOLD_LT="#E8C96A"
CREAM="#FBF5E6"; INK="#1A1A1A"; GRAY="#6B7280"; WHITE="#FFFFFF"
FONT="Liberation Sans"
W,H=1080,1350
MYERS="/sessions/gifted-focused-wright/mnt/Myers Data Base/Myers "
D="/sessions/gifted-focused-wright/mnt/Myers Data Base/Agent Marketing/Cynthia_Before_1708 High Point Cir, Garland, TX 75041"

def b64png(p):
    return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
LOGO=b64png(MYERS+"/MHB_Logo_4C-Pos (2).png")

def b64img(path):
    img=ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if img.width>1600:
        img=img.resize((1600,int(img.height*1600/img.width)),Image.LANCZOS)
    buf=io.BytesIO(); img.save(buf,"JPEG",quality=88)
    return "data:image/jpeg;base64,"+base64.b64encode(buf.getvalue()).decode()

def card(path, kind, room, outname):
    # kind: BEFORE (charcoal) or AFTER (gold)
    badge_fill = INK if kind=="BEFORE" else GOLD
    badge_txt  = GOLD_LT if kind=="BEFORE" else WHITE
    data=b64img(path)
    px, py, pw, ph = 64, 200, W-128, 980
    svg=f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{W}" height="{H}" fill="{WHITE}"/>
  <image x="64" y="52" width="230" height="76" href="{LOGO}" preserveAspectRatio="xMinYMid meet"/>
  <text x="{W-64}" y="100" text-anchor="end" font-family="{FONT}" font-weight="bold"
        font-size="26" letter-spacing="5" fill="{GOLD}">1708 HIGH POINT CIR</text>
  <rect x="64" y="148" width="{W-128}" height="3" fill="{GOLD_BAND}"/>
  <clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24"/></clipPath>
  <image x="{px}" y="{py}" width="{pw}" height="{ph}" href="{data}"
         preserveAspectRatio="xMidYMid slice" clip-path="url(#pc)"/>
  <rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="24" fill="none" stroke="{GOLD_BAND}" stroke-width="3"/>
  <rect x="{px+20}" y="{py+20}" width="230" height="72" rx="14" fill="{badge_fill}"/>
  <text x="{px+135}" y="{py+68}" text-anchor="middle" font-family="{FONT}" font-weight="bold"
        font-size="36" letter-spacing="4" fill="{badge_txt}">{kind}</text>
  <text x="{W/2}" y="1245" text-anchor="middle" font-family="{FONT}" font-weight="bold"
        font-size="46" fill="{INK}">{room}</text>
  <text x="{W/2}" y="1302" text-anchor="middle" font-family="{FONT}" font-size="26" fill="{GRAY}">
        Renovated by Myers investor-agent Cynthia Orozco</text>
</svg>'''
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f"/sessions/gifted-focused-wright/mnt/outputs/{outname}.png",
                     output_width=W,output_height=H)
    print("rendered",outname)

pairs=[("1","Living Room"),("2","Primary Bath"),("3","Guest Bath"),("4","Bedroom")]
for n,room in pairs:
    card(f"{D}/{n} Before.jpg","BEFORE",room,f"cyn-{n}-before")
    card(f"{D}/{n} After.png","AFTER",room,f"cyn-{n}-after")
