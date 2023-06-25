import argparse,sys,os,struct
class tokenizer():
    def __init__(self, infile, outfile, flags):
        self.flags = flags
        self.memoryEntryPoint, self.memoryExitPoint = 0x0801, 0x0000
        self.overwrite = False
        try:
            assert(self.__validateInFile(infile)), "\nCHOMP: Something went wrong. Please check your input filepath.\n"
        except Exception as e:
            print(e)
            exit()         
        try:
            assert(self.__validateOutFile(outfile)), "\nCHOMP: Something went wrong. Please check your output filepath.\n"
        except Exception as e:
            print(e)
            exit()
        self.infile, self.outfile = os.path.join(os.getcwd(),infile), os.path.join(os.getcwd(), outfile)
        self.originalContent = self.__fileContentSplitter()
        self.tokenizedContent = []
        self.v2List = {"END": 0x80,"FOR": 0x81,"NEXT": 0x82,
                        "DATA": 0x83,"INPUT#": 0x84,"INPUT": 0x85,"DIM": 0x86,"READ": 0x87,
                        "LET": 0x88,"GOTO": 0x89,"RUN": 0x8A,"IF": 0x8B,"RESTORE": 0x8C,
                        "GOSUB": 0x8D,"RETURN": 0x8E,"STOP": 0x90,"ON": 0x91,"WAIT": 0x92,
                        "LOAD": 0x93,"SAVE": 0x94,"VERIFY": 0x95,"DEF": 0x96,"POKE": 0x97,
                        "PRINT#": 0x98,"PRINT": 0x99,"CONT": 0x9A,"LIST": 0x9B,"CLR": 0x9C,
                        "CMD": 0x9D,"SYS": 0x9E,"OPEN": 0x9F,"CLOSE": 0xA0,"GET": 0xA1,
                        "NEW": 0xA2,"TAB(": 0xA3,"TO": 0xA4,"FN": 0xA5,"SPC(": 0xA6,
                        "THEN": 0xA7,"NOT": 0xA8,"STEP": 0xA9,"+": 0xAA,"-": 0xAB,
                        "*": 0xAC,"/": 0xAD,"^": 0xAE,"AND": 0xAF,"OR": 0xB0,
                        ">": 0xB1,"=": 0xB2,"<": 0xB3,"SGN": 0xB4,"ABS": 0xB6,
                        "USR": 0xB7,"FRE": 0xB8,"POS": 0xB9,"SQR": 0xBA,"RND": 0xBB,
                        "LOG": 0xBC,"EXP": 0xBD,"COS": 0xBE,"SIN": 0xBF, "TAN": 0xC0,
                        "ATN": 0xC1,"PEEK": 0xC2,"LEN": 0xC3,"STR$": 0xC4,"VAL": 0xC5,
                        "ASC": 0xC6,"CHR$": 0xC7,"LEFT$": 0xC8,"RIGHT$": 0xC9,"MID$": 0xCA,
                        "GO": 0xCB,"INT": 0xB5} 
        self.keywords= list(self.v2List.keys())
        self.tokens= list(self.v2List.values())

    def __validateInFile(self,file):
        path = os.path.join(os.getcwd(), file)
        correctPathAndFile = (os.path.exists(path) and os.path.isfile(path))
        correctExt = (file[-4:] == ".bas")
        if(correctExt and correctPathAndFile):
            return True
        return False

    def __validateOutFile(self,file):
        res = ""
        path = os.path.join(os.getcwd(), file)
        if (os.path.exists(path) and not self.overwrite):
            while (not res.upper() == 'Y' and not res.upper() == "N"):
                res = input("\nCHOMP: The output file currently exists. Would you like to overwrite it? (Y/N)  ")
                print()
            if (res.upper() == 'Y'):
                return True
            print("CHOMP: Please enter a new output file.\n")
            exit()
        return True

    def __fileContentSplitter(self):
        file = open(self.infile, 'r')
        contents = file.readlines()
        return contents


    def tokenize(self):
        for i in range(len(self.originalContent)):
            if(not self.originalContent[i].strip()):
                continue
            lineNum,lineContent = self.__stripLineNumber(self.originalContent[i], i)
            lineContent = self.__tokenizeLine(lineContent)
            self.tokenizedContent.append((lineNum,lineContent))
        self.__writeToOuputFile()

    def __tokenizeLine(self, line):
        line = line.upper()
        noQuotedMaterial = self.__removeQuotedMaterial(line)
        tokenizedLine = []

        if ("REM" in noQuotedMaterial):
            commentLine = self.__convertToList(noQuotedMaterial.replace("REM",""))
            tokenizedLine.extend([0x8F])
            tokenizedLine.extend(commentLine)
            return tokenizedLine
        if (':' in noQuotedMaterial):
            split = line.index(':')
            left, right = line[0:split], line[split+1:]
            splitLeft, splitRight = self.__tokenizeLine(left), self.__tokenizeLine(right)
            tokenizedLine.extend(splitLeft)
            tokenizedLine.extend([ord(":")])
            tokenizedLine.extend(splitRight)
            tokenizedLine = [i for i in tokenizedLine if i!='']
            return tokenizedLine

        for i in range(len(self.keywords)):
            currKeyword = self.keywords[i] 
            if currKeyword in noQuotedMaterial:
                split = line.index(currKeyword)
                left, right = line[0:split], line[split+len(currKeyword):]
                tokeLeft, tokeRight = self.__tokenizeLine(left), self.__tokenizeLine(right)
                tokenizedLine.extend(tokeLeft)
                print(currKeyword, hex(self.v2List[currKeyword]))
                tokenizedLine.extend([self.v2List[currKeyword]])
                tokenizedLine.extend(tokeRight)
                tokenizedLine = [i for i in tokenizedLine if i!='']
                return tokenizedLine
        return self.__convertToList(line)

    def __writeToOuputFile(self):
        out = open(self.outfile, "wb")
        entry,exit = self.memoryEntryPoint, self.memoryExitPoint
        entryLocation,exitLocation = struct.pack('<H', entry), struct.pack('<H', exit)
        location = entry
        out.write(entryLocation)
        for line in self.tokenizedContent:
            binLine = self.__convertLineToBinary(line)
            location = 2 + location + len(binLine)
            binlocation = struct.pack('<H', location)
            out.write(binlocation)
            for i in binLine:
                out.write(i)
        out.write(exitLocation)

    def __convertLineToBinary(self, lineTup):
        lineNumber, lineContent = lineTup[0], lineTup[1]
        binLineNumber, binLineContent = struct.pack('<H', int(lineNumber)), []
        for i in range(len(lineContent)):
            if(type(lineContent[i]) == str):
                binLineContent.append(struct.pack('B', ord(lineContent[i])))
                continue
            binLineContent.append(struct.pack('B', (lineContent[i])))
        binLineContent.insert(0,struct.pack('B',binLineNumber[1]))
        binLineContent.insert(0,struct.pack('B',binLineNumber[0]))
        binLineContent.append(b'\x00')
        return(binLineContent)

    def __stripLineNumber(self, line, contentLineNumber):
        newline,num = '',''
        split = 0
        while (line[split].isnumeric()):
            num += line[split]
            split +=1    
        newline+=line[split:]
        if(not num):
            print("\nCHOMP: Something went wrong. There is no line number present on line: " + str(contentLineNumber+1) + "\n")
            exit()
        newline = newline.strip()
        return (num, newline)
            
    def __removeQuotedMaterial(self,line):
        flag = False
        newstr = ''
        for char in line:
            if (not flag and not char == '\"'):
                newstr += char
            if(char=='\"'):
                flag = not flag 
        return newstr                

    def __convertToList(self, line):
        lineaslist = []
        lineaslist[:0]=line
        for i in range(len(line)):
            lineaslist[i] = line[i]
        return lineaslist

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inpath", help="Path to desired input file (*.bas)")
    parser.add_argument("outpath", help="Path to desired output file (*.prg)")
    parser.add_argument("-o","--overwrite", help="Overwrite output file, if it exists", action='store_true')
    parser.add_argument("-v","--verbose", help="Display tokenizer steps", action='store_true')
    args=parser.parse_args()
    t = tokenizer(args.inpath, args.outpath, {"o":args.overwrite, 'v':args.verbose})
    