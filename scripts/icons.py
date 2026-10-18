from PIL import Image, ImageDraw
import os
HERE=os.path.dirname(os.path.abspath(__file__))
BG=(165,82,255,255)
def _base():
    src=os.path.join(HERE,"logo.png")
    if not os.path.exists(src): src=os.path.join(HERE,"..","www","icons","logo.png")
    a=Image.open(src).convert("RGBA").crop((40,20,960,940))
    bg=Image.new("RGBA",a.size,BG); return Image.alpha_composite(bg,a)
def icon(size, maskable=False):
    b=_base()
    if not maskable: return b.resize((size,size),Image.LANCZOS)
    c=Image.new("RGBA",(size,size),BG); s=int(size*0.8)
    c.paste(b.resize((s,s),Image.LANCZOS),((size-s)//2,(size-s)//2)); return c
def splash(w,h):
    im=Image.new("RGBA",(w,h),(15,12,29,255)); s=int(min(w,h)*0.34)
    ic=icon(s); m=Image.new("L",(s,s),0); ImageDraw.Draw(m).rounded_rectangle([0,0,s,s],radius=int(s*.2),fill=255)
    im.paste(ic,((w-s)//2,(h-s)//2),m); return im.convert("RGB")

if __name__=="__main__":
    import glob
    res="android/app/src/main/res"
    if os.path.isdir(res):
        leg={"mdpi":48,"hdpi":72,"xhdpi":96,"xxhdpi":144,"xxxhdpi":192}
        fg={"mdpi":108,"hdpi":162,"xhdpi":216,"xxhdpi":324,"xxxhdpi":432}
        for k,s in leg.items():
            ic=icon(s).convert("RGB"); ic.save(f"{res}/mipmap-{k}/ic_launcher.png")
            m=Image.new("L",(s,s),0);ImageDraw.Draw(m).ellipse([0,0,s-1,s-1],fill=255)
            r=Image.new("RGBA",(s,s),(0,0,0,0));r.paste(ic,(0,0),m);r.save(f"{res}/mipmap-{k}/ic_launcher_round.png")
            # icône adaptative : le logo occupe la zone visible (66 %)
            c=Image.new("RGBA",(fg[k],fg[k]),BG);t=int(fg[k]*0.72)
            c.paste(icon(t),((fg[k]-t)//2,(fg[k]-t)//2));c.save(f"{res}/mipmap-{k}/ic_launcher_foreground.png")
        open(f"{res}/values/ic_launcher_background.xml","w").write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#A552FF</color>\n</resources>\n')
        for f in glob.glob(f"{res}/drawable*/splash.png"):
            w,h=Image.open(f).size; splash(w,h).save(f)
        print("Icônes Android OK")
    ios="ios/App/App/Assets.xcassets"
    if os.path.isdir(ios):
        icon(1024).convert("RGB").save(f"{ios}/AppIcon.appiconset/AppIcon-512@2x.png")
        for f in glob.glob(f"{ios}/Splash.imageset/*.png"):
            w,h=Image.open(f).size; splash(w,h).save(f)
        print("Icônes iOS OK")
