import struct, filecmp
print(filecmp.cmp('testingFiles\\boing.prg.txt', 'testingFiles\\boingtest.prg.txt'))

# reading files
f1 = open("C:\\Users\\mecha\\OneDrive\\Desktop\\personal projects\\CHOMP\\testingFiles\\boing.prg.txt", "r") 
f2 = open("C:\\Users\\mecha\\OneDrive\\Desktop\\personal projects\\CHOMP\\testingFiles\\boingtest.prg.txt", "r") 
 
f1_data = f1.readlines()
f2_data = f2.readlines()
 
i = 0
 
for i in range(len(f1_data)):
    if f1_data[i] == f2_data[i]: 
        # print IDENTICAL if similar
        print("Line ", i, ": IDENTICAL")      
    else:
        print("Line ", i, ":")
        # else print that line from both files
        print("\tFile 1:", f1_data[i], end='')
        print("\tFile 2:", f2_data[i], end='')

 
# closing files
f1.close()                                      
f2.close()  