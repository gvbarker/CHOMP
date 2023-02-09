1 a="test":b="test"
3 ax=10:ay=10:bx=20:by=20
4 m = (ay-by)/(ax-bx)
5 z = ay-(m*ax)
6 base=2*4095:poke53272,peek(53272)or8
10 poke53265,peek(53265)or32
20 fori=basetobase+7999:pokei,0:next
30 fori=1024to2023:pokei,3:next
40 forx=axtobxstep.5
60 y=int(m*x)+z
