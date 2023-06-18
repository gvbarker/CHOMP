1 print chr$(147)
5 PRINTCHR$(142)               :REM SWITCH TO UPPER CASE
10 POKE52,48:POKE 56,48:CLR    :REM RESERVE MEMORY FOR CHARACTERS
20 POKE56334,PEEK(56334)AND254 :REM TURN OFF KEYSCAN INTERRUPT TIMER
30 POKE1,PEEK(1)AND251         :REM SWITCH IN CHARACTER
40 FORI=0TO511:POKEI+12288,PEEK(I+53248):NEXT
50 POKE1,PEEK(1)OR4            :REM SWITCH IN I/O
60 POKE56334,PEEK(56334)OR1    :REM RESTART KEYSCAN INTERRUPT TIMER
70 POKE 53272,(PEEK(53272) AND 240)+12
80 FOR I=0 TO 7 
90 POKE(12288+I),255:NEXT
100 poke 53280,0
101 POKE 53281,0
102 j=15
120 for i=0 to 39
121 poke(1024+i),0:poke(55296+i),j:next
122 for i=1 to 25
123 poke(1024+39+(40*i)),0:poke(55296+39+(40*i)),j:next
124 for i=1 to 40
125 poke(2023-i),0:poke(56295-i),j:next
126 for i=0 to 21
127 poke(1944-(40*i)),0:poke(56216-(40*i)),j:next
128 for i=0 to 37
129 poke(1104+i),0:poke(55376+i),j:next
130 for i=1 to 20
131 poke(1141+(40*i)),0:poke(55413+(40*i)),j:next
132 for i=1 to 35
133 poke(1941-i),0:poke(56213-(i)),j:next
134 for i=1 to 18
135 poke(1906-(40*i)),0:poke(56178-(40*i)),j:next
136 for i=1 to 33
137 poke(1186+i),0:poke(55458+(i)),j:next
138 for i=1 to 16
139 poke(1219+(40*i)),0:poke(55491+(40*i)),j:next
140 for i=1 to 31
141 poke(1859-i),0:poke(56131-(i)),j:next
142 for i=1 to 14
143 poke(1828-(40*i)),0:poke(56100-(40*i)),j:next
144 for i=1 to 29 
145 poke(1268+i),0:poke(55540+(i)),j:next
146 for i=1 to 12
147 poke(1297+(40*i)),0:poke(55569+(40*i)),j:next
148 for i=1 to 27
149 poke(1777-i),0:poke(56049-(i)),j:next
150 for i=1 to 10
151 poke(1750-(40*i)),0:poke(56022-(40*i)),j:next
152 for i=1 to 25
153 poke(1350+i),0:poke(55622+(i)),j:next
155 for i=1 to 8
156 poke(1375+(i*40)),0:poke(55647+(40*i)),j:next
157 for i=1 to 23
158 poke(1695-i),0:poke(55967-(i)),j:next
159 for i=1 to 6
160 poke(1672-(40*i)),0:poke(55944-(40*i)),j:next
161 for i=1 to 21
162 poke(1432+i),0:poke(55704+(i)),j:next
163 for i=1 to 4
164 poke(1453+(40*i)),0:poke(55725+(40*i)),j:next
165 for i=1 to 19
166 poke(1613-i),0:poke(55885-(i)),j:next
167 for i=1 to 2
168 poke(1594-(i*40)),0:poke(55866-(40*i)),j:next
169 for i=1 to 17
170 poke(1514+i),0:poke(55786+(i)),j:next
