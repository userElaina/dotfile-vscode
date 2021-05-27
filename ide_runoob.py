import os
import sys
import requests
HEADERS={
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# print(sys.argv)

language=sys.argv[1]
PTH=sys.argv[2]

p_file=sys.argv[3]
p_in=None
p_out=p_file+'.out'
p_err=p_file+'.err'
p_log=p_file+'.log'

N=4
for i in range(N,N+len(sys.argv[N:])):
    if sys.argv[i]=='--in':
        p_in=sys.argv[i+1]
    if sys.argv[i]=='--out':
        p_out=sys.argv[i+1]
    if sys.argv[i]=='--err':
        p_err=sys.argv[i+1]

def fp(x)->str:
    try:
        return open(os.path.join(PTH,x),'r').read() if x else ''
    except:
        return ''

_runoob_set0={
    'r':'R',
    'vb':'vb',
    'ts':'ts',
    'typescript':'ts',
    'kt':'kt',
    'kotlin':'kt',
    'pas':'pas',
    'pascal':'pas',
    'lua':'lua',
    'node.js':'node.js',
    'nodejs':'node.js',
    'js':'node.js',
    'go':'go',
    'golang':'go',
    'swift':'swift',
    'rs':'rs',
    'rust':'rs',
    'sh':'sh',
    'bash':'sh',
    'pl':'pl',
    'perl':'pl',
    'erl':'erl',
    'erlang':'erl',
    'scala':'scala',
    'cs':'cs',
    'c#':'cs',
    'csharp':'cs',
    'cpppp':'cs',
    'c++++':'cs',
    'c艹艹':'cs',
    'rb':'rb',
    'ruby':'rb',
    'cpp':'cpp',
    'c++':'cpp',
    'c艹':'cpp',
    'c':'c',
    'java':'java',
    'py3':'py3',
    'py':'py3',
    'py2':'py',
    'php':'php',
}
_runoob_set1={
    'R':80,
    'vb':84,
    'ts':1001,
    'kt':19,
    'pas':18,
    'lua':17,
    'node.js':4,
    'go':6,
    'swift':16,
    'rs':9,
    'sh':11,
    'pl':14,
    'erl':12,
    'scala':5,
    'cs':10,
    'rb':1,
    'cpp':7,
    'c':7,
    'java':8,
    'py3':15,
    'py':0,
    'php':3
}

url='https://tool.runoob.com/compile2.php'

def runoob(
	s:str='print(\'Hello world!\')',
	pl:str='py3',
	stdin:str=''
):
	pl=_runoob_set0[pl.lower()]
	payload={
		'code':s,
		'token':'4381fe197827ec87cbac9552f14ec62a',
		'stdin':stdin,
		'language':_runoob_set1[pl],
		'fileext':pl,
	}
	res=requests.post(url=url,headers=HEADERS,data=payload)
	return res.json()

def strunoob(
	s:str='print(\'Hello world!\')',
	pl:str='py3',
	stdin:str='',
):
	d=runoob(s,pl,stdin)
	return 'Output:\n'+d['output']+(
		('\nErrors:\n'+d['errors']) if d['errors']!='\n\n' else ''
	)

open(p_out,'w').write(strunoob(
    s=fp(p_file),
    pl=language,
    stdin=fp(p_in),
))