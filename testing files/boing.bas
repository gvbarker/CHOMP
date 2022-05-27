10 print chr$(147)
20 poke 2040,13
30 v=53248
40 pokev+21,1
50 pokev+39,5
51 x=50:y=30
60 pokev,x
70 pokev+1,y

81 poke 832,0
82 poke 833,126
83 poke 834,0

84 poke 835,3
85 poke 836,255
86 poke 837,192

87 poke 838,7
88 poke 839,255
89 poke 840,224

90 poke 841,31
91 poke 842,255
92 poke 843,248

93 poke 844,31
94 poke 845,255
95 poke 846,248

96 poke 847,63
97 poke 848,255
98 poke 849,252

99 poke 850,127
100 poke 851,255
101 poke 852,254

102 poke 853,127
103 poke 854,255
104 poke 855,254

105 poke 856,255
106 poke 857,255
107 poke 858,255

108 poke 859,255
109 poke 860,255
110 poke 861,255

111 poke 862,255
112 poke 863,255
113 poke 864,255

114 poke 865,255
115 poke 866,255
116 poke 867,255

117 poke 868,255
118 poke 869,255
119 poke 870,255

120 poke 871,127
121 poke 872,255
122 poke 873,254

123 poke 874,127
124 poke 875,255
125 poke 876,254

126 poke 877,63
127 poke 878,255
128 poke 879,252

129 poke 880,31
130 poke 881,255
131 poke 882,248

132 poke 883,31
133 poke 884,255
134 poke 885,248

135 poke 886,7
136 poke 887,255
137 poke 888,244

138 poke 889,3
139 poke 890,255
140 poke 891,192

141 poke 892,0
142 poke 893,126
143 poke 894,0

150 fori=31to229step1
160 pokev+1,i:next
170 fori=229to133step-1
180 pokev+1,i:next
181 pokev+1,134
182 pokev+1,135
183 pokev+1,136
184 pokev+1,137
185 pokev+1,138
190 fori=135to229step1
200 pokev+1,i:next
210 fori=229to182step-1
220 pokev+1,i:pokev,x+1
221 x=x+1:next
230 fori=182to229step1
240 pokev+1,i:pokev,x+1
241 x=x+1:next
250 fori=229to205step-1
260 pokev+1,i:pokev,x-1
270 x=x-1:next
280 fori=205to229step1
290 pokev+1,i:pokev,x-2
300 x=x-2:next
310 fori=229to217step-1
320 pokev+1,i:pokev,x-3
330 x=x-3:next
340 fori=217to229step1
350 pokev+1,i:pokev,x-2
360 x=x-2:next
370 fori=229to224step-1
380 pokev+1,i:pokev,x-1
390 x=x-1:next
400 rem I really wanted to do the DVD logo
401 rem didnt have enough time to really work it out
402 rem wabash takes another soul :(