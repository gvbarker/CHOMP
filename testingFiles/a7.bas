5 print(chr$(147))
10 open 1,8,2,"noprint,seq,r"
11 b=1024
12 l=0
13 c=0
14 p=1024
15 pc=0
20 get#1,b$:c=c+1
30 if(st and 64)=64 then goto 500
40 if b$=(chr$(13)) or c=41 then c=0:goto 200
50 if b$=(chr$(10)) or c=41 then c=0:goto 200
60 a=asc(b$)
65 if a>=64 then a=a-64
70 poke(p+pc),a:pc=pc+1:goto 20
200 l=l+1:p=b+(40*l):pc=0:goto 20
500 close1:end