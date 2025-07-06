# Pyxel Mandelbrot Set
# by Kouzerumatsukite, 6 Jul 2025

import pyxel, time

offset_x = 0
offset_y = 0
zoom     = 0
iters    = 64
itersexp = 6*16
last_time = 0

frames = 0
def update():
    global offset_x, offset_y, zoom, frames, itersexp, iters
    if pyxel.btn(pyxel.KEY_LEFT ): offset_x -= (1/32)/2**zoom; frames = 0
    if pyxel.btn(pyxel.KEY_RIGHT): offset_x += (1/32)/2**zoom; frames = 0
    if pyxel.btn(pyxel.KEY_UP   ): offset_y -= (1/32)/2**zoom; frames = 0
    if pyxel.btn(pyxel.KEY_DOWN ): offset_y += (1/32)/2**zoom; frames = 0
    if pyxel.btnp(pyxel.KEY_Z   ): zoom     += 1             ; frames = 0
    if pyxel.btnp(pyxel.KEY_X   ): zoom     -= 1*(zoom>0)    ; frames = 0
    if pyxel.btn(pyxel.KEY_A    ): itersexp += 1             ; frames = 0
    if pyxel.btn(pyxel.KEY_S    ): itersexp -= 1*(itersexp>0); frames = 0
    iters = int(2**(itersexp/16))
    pass

def pixel(x,y,ox,oy,zoom):
    cx = (((x-60)/32)/2**zoom)+ox
    cy = (((y-80)/32)/2**zoom)+oy
    zx = 0
    zy = 0
    i  = 0
    while i<iters:
        zzx = zx*zx
        zzy = zy*zy
        zzd = zzx+zzy
        if zzd>=4: break
        zy = 2*zx*zy
        zy = zy+cy
        zx = zzx-zzy+cx
        i += 1
    j = i&3
    i = i>>2
    #i = i+(((x+y&1)*2+(y&1))<j) # 2x2 bayer matrix
    i = i+((x*2+y&3)<j) # fancy 2x4 bayer matrix
    pyxel.pset(x,y,i&15)

def debug(x, y, c, offset_x, offset_y, zoom):
    pyxel.text(x,y+ 1, "(< >) offx: "+str(offset_x),c)
    pyxel.text(x,y+ 9, "(^ v) offy: "+str(offset_y),c)
    pyxel.text(x,y+17, "(z x) zoom: 2^-"+str(zoom) ,c)
    pyxel.text(x,y+25, "(a s) iter: "+str(iters)   ,c)

def draw():
    global offset_x, offset_y, zoom, iters, frames, last_time
    now = time.time()
    
    if frames==0: pyxel.cls(0); last_time = now;
    
    while(time.time()-now<1/64):
        y  = (frames+1&2)<<2|(frames+4&8)>>1|(frames+16&32)>>4|(frames+64&128)>>7
        while y<160:
            x = (frames&1)<<3|(frames&4)>>0|(frames&16)>>3|(frames&64)>>6
            while x<120:
                pixel(x,y,offset_x,offset_y,zoom)
                x += 16
            y += 16
            
        frames += 1;
    if last_time+5 > now:
        debug(+1,  0, 1, offset_x, offset_y, zoom)
        debug(-1,  0, 1, offset_x, offset_y, zoom)
        debug( 0, +1, 1, offset_x, offset_y, zoom)
        debug( 0, -1, 1, offset_x, offset_y, zoom)
        debug( 0,  0, 7, offset_x, offset_y, zoom)

pyxel.init(120, 160, fps=60)
pyxel.run(update, draw)
