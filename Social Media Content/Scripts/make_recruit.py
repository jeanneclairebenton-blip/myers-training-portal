#!/usr/bin/env python3
"""Myers packet-style recruiting graphics: Commission + Hiring. 1080x1350."""
import base64, cairosvg
from PIL import ImageFont

GOLD="#C9972C"; GOLD_BAND="#D6A73F"; GOLD_LT="#E8C96A"
CREAM="#FBF5E6"; INK="#1A1A1A"; GRAY="#6B7280"; WHITE="#FFFFFF"
FONT="Liberation Sans"
W,H=1080,1350
MYERS="/sessions/gifted-focused-wright/mnt/Myers Data Base/Myers Branding"
def b64png(p): return "data:image/png;base64,"+base64.b64encode(open(p,'rb').read()).decode()
LOGO=b64png(MYERS+"/MHB_Logo_4C-Pos (2).png")
_FP="/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def header(kicker):
    return f'''<image x="64" y="52" width="230" height="76" href="{LOGO}" preserveAspectRatio="xMinYMid meet"/>
  <text x="{W-64}" y="100" text-anchor="end" font-family="{FONT}" font-weight="bold" font-size="26" letter-spacing="5" fill="{GOLD}">{kicker}</text>
  <rect x="64" y="148" width="{W-128}" height="3" fill="{GOLD_BAND}"/>'''
def footer():
    return f'''<rect x="64" y="{H-90}" width="{W-128}" height="2" fill="#E8E8E5"/>
  <text x="{W/2}" y="{H-42}" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GRAY}">Myers Home Buyers · Where Agents Become Investors · joinmyers.com</text>'''
def tt_center(cx,y,size,black,gold):
    total=ImageFont.truetype(_FP,size).getlength(black+gold); x0=cx-total/2
    return f'<text x="{x0}" y="{y}" text-anchor="start" font-family="{FONT}" font-weight="bold" font-size="{size}" fill="{INK}">{black}<tspan fill="{GOLD}">{gold}</tspan></text>'
def stat_band(y,stats,h=170):
    n=len(stats); cw=(W-128)/n; out=f'<rect x="64" y="{y}" width="{W-128}" height="{h}" rx="18" fill="{GOLD_BAND}"/>'
    for i,(big,small) in enumerate(stats):
        cx=64+cw*i+cw/2
        if i: out+=f'<rect x="{64+cw*i}" y="{y+34}" width="2" height="{h-68}" fill="#00000022"/>'
        out+=f'<text x="{cx}" y="{y+h/2+2}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="52" fill="{INK}">{big}</text>'
        out+=f'<text x="{cx}" y="{y+h/2+48}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="20" letter-spacing="2" fill="#5b4310">{small}</text>'
    return out
def render(name,body):
    svg=f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{WHITE}"/>{header_k}{body}{footer()}</svg>'
    cairosvg.svg2png(bytestring=svg.encode(),write_to=f"/sessions/gifted-focused-wright/mnt/outputs/{name}.png",output_width=W,output_height=H)
    print("rendered",name)

def star(cx,cy,s,fill):
    pts="0,-1 0.225,-0.309 0.951,-0.309 0.363,0.118 0.588,0.809 0,0.382 -0.588,0.809 -0.363,0.118 -0.951,-0.309 -0.225,-0.309"
    return f'<polygon points="{pts}" transform="translate({cx},{cy}) scale({s})" fill="{fill}"/>'

# ---------- COMMISSION ----------
header_k=header("HOW YOU GET PAID")
body=tt_center(W/2,244,58,"Own Your Business. ","Keep 80%.")
body+=f'<text x="{W/2}" y="304" text-anchor="middle" font-family="{FONT}" font-size="30" fill="{GRAY}">80% direct payout + a 10% revenue-share pool. No desk fees. No games.</text>'
body+=stat_band(348,[("80%","DIRECT PAYOUT"),("10%","REV-SHARE POOL"),("$0","DESK FEES")],h=182)
# ladder
ly=628
body+=tt_center(W/2,ly,30,"From first deal to ","full-time investor")
steps=[("1",["Sales Agent"],"20%","payout"),("2",["Acquisition","Agent"],"60%","payout"),
       ("3",["Team Lead"],"50%","split"),("★",["Investor"],"GEN","Generational Wealth")]
n=4; pad=155; span=(W-2*pad); gap=span/(n-1); cy=ly+118
body+=f'<line x1="{pad}" y1="{cy}" x2="{W-pad}" y2="{cy}" stroke="{GOLD_BAND}" stroke-width="6"/>'
for i,(nu,names,pay,lbl) in enumerate(steps):
    cx=pad+gap*i
    body+=f'<circle cx="{cx}" cy="{cy}" r="40" fill="{GOLD}"/>'
    if nu=="★": body+=star(cx,cy,22,WHITE)
    else: body+=f'<text x="{cx}" y="{cy+13}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="40" fill="{WHITE}">{nu}</text>'
    yy=cy+88
    for nm in names:
        body+=f'<text x="{cx}" y="{yy}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="27" fill="{INK}">{nm}</text>'; yy+=34
    if pay=="GEN":
        body+=f'<text x="{cx}" y="{yy+22}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="25" fill="{GOLD}">Generational</text>'
        body+=f'<text x="{cx}" y="{yy+52}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="25" fill="{GOLD}">Wealth</text>'
    else:
        body+=f'<text x="{cx}" y="{yy+30}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="46" fill="{GOLD}">{pay}</text>'
        body+=f'<text x="{cx}" y="{yy+62}" text-anchor="middle" font-family="{FONT}" font-size="22" fill="{GRAY}">{lbl}</text>'
body+=f'<text x="{W/2}" y="{cy+300}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="34" fill="{INK}">Licensed in TX? DM &#8220;MODEL&#8221; for the full breakdown.</text>'
render("v5-commission",body)

# ---------- COMPARISON ----------
GREEN="#2E7D32"; NAVY="#1F2D5A"; BASE="#E6BB3E"; REV="#F7E6AC"; MYLABEL="#B98A1F"
ICON="data:image/png;base64,"+base64.b64encode(open(MYERS+"/MHB_Logo_Icon_RGB (3).png",'rb').read()).decode()
cbody=header("THE DIFFERENCE")
cbody+=tt_center(W/2,226,52,"Same Job. ","We Pay More.")
cbody+=f'<text x="{W/2}" y="278" text-anchor="middle" font-family="{FONT}" font-size="27" fill="{GRAY}">What Myers pays its agents vs. a typical DFW brokerage.</text>'
# rev-share key
cbody+=f'<rect x="392" y="306" width="24" height="24" rx="5" fill="{BASE}"/><text x="424" y="325" font-family="{FONT}" font-weight="bold" font-size="20" fill="{INK}">Payout</text>'
cbody+=f'<rect x="548" y="306" width="24" height="24" rx="5" fill="{REV}"/><text x="580" y="325" font-family="{FONT}" font-weight="bold" font-size="20" fill="{INK}">+ Rev Share</text>'
# grouped bars: (role, myers_base, myers_rev, compA, compB)
baseline=1000; scale=6.2; bw=58; bgap=12
groups=[("Sales Agent",20,0,15,10),("Acquisition Agent",60,0,30,30),("Total Payout",80,10,45,40)]
gcx=[268,540,812]
for gi,(role,mb,mr,ca,cb) in enumerate(groups):
    startx=gcx[gi]-(3*bw+2*bgap)/2
    xm=startx; base_h=mb*scale; goldtop=baseline-base_h; yb=goldtop
    cbody+=f'<rect x="{xm}" y="{yb}" width="{bw}" height="{base_h}" rx="5" fill="{BASE}"/>'
    top=mb
    if mr:
        rev_h=mr*scale; yr=yb-rev_h
        cbody+=f'<rect x="{xm}" y="{yr}" width="{bw}" height="{rev_h+6}" rx="5" fill="{REV}"/>'
        cbody+=f'<rect x="{xm}" y="{yb-3}" width="{bw}" height="3" fill="{WHITE}"/>'
        cbody+=f'<text x="{xm+bw/2}" y="{yr+rev_h/2+6}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="16" fill="#5b4310">+{mr}%</text>'
        top=mb+mr; yb=yr
    cbody+=f'<text x="{xm+bw/2}" y="{yb-14}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="30" fill="{MYLABEL}">{top}%</text>'
    cbody+=f'<rect x="{xm+bw/2-22}" y="{goldtop+10}" width="44" height="44" rx="9" fill="{WHITE}"/><image x="{xm+bw/2-18}" y="{goldtop+14}" width="36" height="36" href="{ICON}"/>'
    for bi,(val,col) in enumerate([(ca,GREEN),(cb,NAVY)]):
        x=startx+(bi+1)*(bw+bgap); h=val*scale; y=baseline-h
        cbody+=f'<rect x="{x}" y="{y}" width="{bw}" height="{h}" rx="5" fill="{col}"/>'
        cbody+=f'<text x="{x+bw/2}" y="{y-14}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="26" fill="{col}">{val}%</text>'
    # angled color-matched brand labels
    lbls=[("Myers",MYLABEL),("Comp A",GREEN),("Comp B",NAVY)]
    for bi,(lbl,col) in enumerate(lbls):
        x=startx+bi*(bw+bgap)+bw/2; ly=baseline+18
        cbody+=f'<text x="{x}" y="{ly}" text-anchor="end" transform="rotate(-38 {x} {ly})" font-family="{FONT}" font-weight="bold" font-size="19" fill="{col}">{lbl}</text>'
    cbody+=f'<text x="{gcx[gi]}" y="{baseline+108}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="23" fill="{INK}">{role}</text>'
cbody+=f'<line x1="110" y1="{baseline}" x2="970" y2="{baseline}" stroke="#DDDDDD" stroke-width="2"/>'
# BIG bottom tagline (font hierarchy)
cbody+=tt_center(W/2,1190,50,"Same work. ","")
cbody+=tt_center(W/2,1254,50,"We pay agents ","like owners.")
cbody+=f'<text x="{W/2}" y="{H-22}" text-anchor="middle" font-family="{FONT}" font-size="22" fill="{GRAY}">Myers Home Buyers · Where Agents Become Investors · joinmyers.com</text>'
svg=f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="{WHITE}"/>{cbody}</svg>'
cairosvg.svg2png(bytestring=svg.encode(),write_to="/sessions/gifted-focused-wright/mnt/outputs/v7-comparison.png",output_width=W,output_height=H)
print("rendered v7-comparison")

# ---------- HIRING ----------
header_k=header("NOW HIRING")
body=tt_center(W/2,220,50,"We&#8217;re Hiring Agents Who Want","")
body+=tt_center(W/2,276,50,"to Become ","Investors.")
body+=f'<text x="{W/2}" y="322" text-anchor="middle" font-family="{FONT}" font-size="27" fill="{GRAY}">Because at Myers, they do &#8212; and agents ready to build their own brand.</text>'
body+=f'<text x="{W/2}" y="366" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="25" fill="#5b4310">Self-motivated · Coachable · Takes action · Builds relationships</text>'
items=[("Keep 80% &#8212; with a real structure","20% &#8594; 60% payout as you rise, plus a 10% rev-share pool."),
       ("Your own business, powered by Myers","Off-market deals + an AI lead engine (Myers &#215; Carrot)."),
       ("Real training","1:1 mentorship + Myers University online training."),
       ("Become an investor yourself","A real path to buying, flipping &amp; holding your own deals.")]
iy=398
for t,d in items:
    body+=f'<rect x="64" y="{iy}" width="{W-128}" height="118" rx="18" fill="{CREAM}" stroke="{GOLD_BAND}" stroke-width="3"/>'
    body+=f'<circle cx="132" cy="{iy+59}" r="30" fill="{GOLD}"/><path d="M116 {iy+59} l11 11 l20 -22" stroke="{WHITE}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    body+=f'<text x="186" y="{iy+48}" font-family="{FONT}" font-weight="bold" font-size="29" fill="{INK}">{t}</text>'
    body+=f'<text x="186" y="{iy+86}" font-family="{FONT}" font-size="24" fill="{GRAY}">{d}</text>'
    iy+=130
# CTA button (looks like a button)
by=iy+8; bh=124
body+=f'<rect x="120" y="{by}" width="{W-240}" height="{bh}" rx="26" fill="{INK}"/>'
body+=f'<text x="{W/2}" y="{by+58}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="40" fill="{WHITE}">Schedule a Call  &#8594;</text>'
body+=f'<text x="{W/2}" y="{by+96}" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GOLD_LT}">See if Myers is the right fit for you.</text>'
render("v6-hiring",body)

# ---------- PARTNER (fellow agents) ----------
header_k=header("FELLOW AGENTS")
body=tt_center(W/2,224,54,"We&#8217;re Buyers, ","Not Competitors.")
body+=f'<text x="{W/2}" y="284" text-anchor="middle" font-family="{FONT}" font-size="28" fill="{GRAY}">Our agents are investors hunting great deals. Bring us one &#8212; and get paid.</text>'
items=[("We sign buyer&#8217;s rep agreements","Represent us on the deal. Everything above board."),
       ("We pay full co-op commissions","You bring it, you get paid. No games, no cut corners."),
       ("Our agents are active investors","They&#8217;re after off-market &amp; value-add deals all year."),
       ("We make your business stronger","One more serious cash buyer in your corner.")]
iy=352
for t,d in items:
    body+=f'<rect x="64" y="{iy}" width="{W-128}" height="130" rx="18" fill="{CREAM}" stroke="{GOLD_BAND}" stroke-width="3"/>'
    body+=f'<circle cx="134" cy="{iy+65}" r="32" fill="{GOLD}"/><path d="M117 {iy+65} l12 12 l21 -23" stroke="{WHITE}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    body+=f'<text x="190" y="{iy+52}" font-family="{FONT}" font-weight="bold" font-size="30" fill="{INK}">{t}</text>'
    body+=f'<text x="190" y="{iy+92}" font-family="{FONT}" font-size="24" fill="{GRAY}">{d}</text>'
    iy+=144
by=iy+8; bh=124
body+=f'<rect x="120" y="{by}" width="{W-240}" height="{bh}" rx="26" fill="{INK}"/>'
body+=f'<text x="{W/2}" y="{by+58}" text-anchor="middle" font-family="{FONT}" font-weight="bold" font-size="38" fill="{WHITE}">Have an off-market deal?  &#8594;</text>'
body+=f'<text x="{W/2}" y="{by+96}" text-anchor="middle" font-family="{FONT}" font-size="24" fill="{GOLD_LT}">DM &#8220;DEALS&#8221; &#8212; let&#8217;s do business.</text>'
render("v8-partner",body)
