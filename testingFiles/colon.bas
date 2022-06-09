10 open 1,8,2,"input,s,r"
20 open 2,8,3,"@0:count,s,w"
30 i=0
35 j=0
40 get#1,a$
50 if(st and 64)=64 then goto 85
60 if a$="" then print chr$(0);
65 if a$=chr$(13) then print a$ "line count: ", j : i=i+1: goto 35
70 if a$<>"" then print a$; : j=j+1 : i=i+1
80 goto 40 
85 print chr$(13) "line count: ", j
90 print chr$(13) "total count (with cr's): ", i
95 print#2, str$(i)
500 close 1 : close 2 : end
