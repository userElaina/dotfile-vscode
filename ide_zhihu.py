import os
from os import system as sh
import re
import sys
import cairosvg
import requests
from urllib.parse import unquote_to_bytes,quote_from_bytes
from typing import Union
from PIL import Image

HEADERS={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

byte_type=Union[bytes,bytearray,memoryview,]
byte_types=(bytes,bytearray,memoryview,)
bytes_type=Union[str,bytes,bytearray,memoryview,]
bytes_types=(str,bytes,bytearray,memoryview,)

def bencode(s:all)->bytes:
	if isinstance(s,byte_types):
		return bytes(s)
	try:
		return bytes(memoryview(s).tobytes())
	except TypeError:
		return str(s).encode(errors='backslashreplace')

def bdecode(s:all,p:tuple=('',False,))->bytes:
	if isinstance(s,byte_types):
		return bytes(s)
	try:
		return bytes(memoryview(s).tobytes())
	except TypeError:
		s=re.sub(p[0],'',(str(s).upper() if p[1] else str(s)))
		return s.encode(encoding='ascii',errors='backslashreplace')

def urlencode(s:str)->str:
	return quote_from_bytes(bencode(s))

def urldecode(s:str)->str:
	return unquote_to_bytes(bencode(s)).decode(errors='backslashreplace')

# print(sys.argv)

language=sys.argv[1]
PTH=sys.argv[2]

p_nm=sys.argv[3]

N=4
for i in range(N,N+len(sys.argv[N:])):
    if sys.argv[i]=='--in':
        p_in=sys.argv[i+1]
    if sys.argv[i]=='--out':
        p_out=sys.argv[i+1]

def fp(x)->str:
    try:
        return open(os.path.join(PTH,x),'r').read() if x else ''
    except:
        return ''


def s2svg(s:str)->bytes:
	s=re.sub('[\s]+',' ',str(s)).replace('\\displaystyle','')
	while s.startswith(' '):
		s=s[1:]
	while s.endswith(' '):
		s=s[:-1]
	url=r'https://www.zhihu.com/equation?tex='+urlencode(s)
	res=requests.get(url,headers=HEADERS)
	return res.content

def f_s2svg(lp:str,rp:str)->None:
	open(rp,'wb').write(s2svg(fp(lp)))

def f_svg2a(lp:str,rp:str,dpi:str)->None:
	cairosvg.svg2png(url=lp,write_to=rp,dpi=dpi)

# def f_svg2a(lp:str,rp:str,dpi:str)->None:
# 	cairosvg.svg2png(bytestring=fp(lp).replace(
# 		'text font-family=\"monospace\"',
# 		'text font-family=\"Sarasa Mono SC Nerd, Segoe UI Emoji\"'
# 	),write_to=rp,dpi=dpi)

def f_a2rgb(lp:str,rp:str,depth:int=64,bg:int=0xffffff):
	img=Image.open(lp)
	img=img.convert('RGBA')
	sp=img.size
	width=sp[0]
	height=sp[1]
	for x in range(width):
		for y in range(height):
			dot=(x,y)
			color_d=list(img.getpixel(dot))
			if color_d[3]<depth:
				color_d=[bg>>16,(bg>>8)%0x100,bg%0x100,255]
			else:
				color_d[3]=255
			img.putpixel(dot,tuple(color_d))
	img.save(rp)

def f_s2png(nm:str,dpi:int,bg:int,zhihu:bool)->None:
	p1=nm+'.zhihu'
	p2=nm+'.svg'
	p3=nm+'_argb.png'
	p4=nm+'_rgb.png'
	if zhihu:
		f_s2svg(p1,p2)
	f_svg2a(p2,p3,dpi)
	if bg:
		f_a2rgb(p3,p4,bg=bg)
		return p4		
	return p3

f_in=fp(p_in)
d={
	'bg':0xffffff,
	'dpi':500,
}

for i in fp(p_in).split('\n'):
	j=i.split('=')
	try:
		d[j[0]]=int(j[-1],16 if j[0]=='bg' else 10)
	except:
		d[j[0]]=None

od='copy "'+f_s2png(p_nm,d['dpi'],d['bg'],bool(language=='zhihu'))+'" "'+p_out+'"'
sh(od)
