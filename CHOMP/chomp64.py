import argparse,os,struct
class tokenizer():
    def __init__(self, infile, outfile, flags=None):
        if (flags is None):
            flags = {'v':False,'o':False}
        else:
            self.flags = flags
        self.memory_entry_point, self.memory_exit_point = 0x0801, 0x0000

        try:
            if (self.flags['v']):
                print("CHOMP64: Validating input filepath...")
            assert(self.__validate_in_file(infile)), "\nCHOMP64: Something went wrong. Please check your input filepath.\n"
        except Exception as e:
            print(e)
            exit()         
        
        try:
            if (self.flags['v']):
                print("CHOMP64: Validating output filepath...")
            assert(self.__validate_out_file(outfile)), "\nCHOMP64: Something went wrong. Please check your output filepath.\n"
        except Exception as e:
            print(e)
            exit()
        
        self.infile, self.outfile = os.path.join(os.getcwd(),infile), os.path.join(os.getcwd(), outfile)
        self.original_content = self.__file_content_splitter()
        self.tokenized_content = []
        self.line_tokens = []
        
        self.v2_list = {"END": 0x80,"FOR": 0x81,"NEXT": 0x82,
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
        
        self.keywords= list(self.v2_list.keys())
        self.tokens= list(self.v2_list.values())

    def __validate_in_file(self,file):
        path = os.path.join(os.getcwd(), file)
        correct_path_and_file = (os.path.exists(path) and os.path.isfile(path))
        correct_extension = (file[-4:] == ".bas")
        
        if (correct_extension and correct_path_and_file):
            return True
        
        return False

    def __validate_out_file(self,file):
        res = ""
        path = os.path.join(os.getcwd(), file)
        if (os.path.exists(path) and not self.flags['o']):
            while (res.upper() != 'Y' and res.upper() != "N"):
                res = input("\nCHOMP64: The output file currently exists. Would you like to overwrite it? (Y/N)  ")
                print()
            
            if (res.upper() == 'N'):
                print("CHOMP64: Please enter a new output file.\n")
                exit()

        return True

    def __file_content_splitter(self):
        input_file = open(self.infile, 'r')
        contents = input_file.readlines()
        return contents

    def tokenize(self):
        for i in range(len(self.original_content)):
            line = self.original_content[i]
            if (not line.strip()):
                continue
            
            if (self.flags['v']):
                print("CHOMP64: Crunching line:\t" + line.strip())
            
            line_num,line_content = self.__strip_line_number(line, i)
            line_content = self.__tokenize_line(line_content)
            
            if (self.flags['v']):
                print("CHOMP64: Tokens found:\t", self.line_tokens)

            self.line_tokens = []
            self.tokenized_content.append((line_num,line_content))

        if (self.flags['v']):
            print("CHOMP64: Tokenization successful, writing to output file...")

        self.__write_to_ouput_file()

        if (self.flags['v']):
            print("CHOMP64: Write successful")


    def __tokenize_line(self, line):
        line = line.upper()
        line_no_quoted_material = self.__remove_quoted_material(line)
        tokenized_line = []

        if ("REM" in line_no_quoted_material):
            if (self.flags['v']):
                print("CHOMP64: Remarked line, continuing...")
            comment_line = self.__convert_to_list(line_no_quoted_material.replace("REM",""))
            tokenized_line.extend([0x8F])
            tokenized_line.extend(comment_line)
            self.line_tokens.append("REM")
            return tokenized_line
        
        if (':' in line_no_quoted_material):
            if (self.flags['v']):
                print("CHOMP64: Multiple commands in line, splitting...")
            
            split = line.index(':')
            left, right = line[0:split], line[split+1:]
            split_left, split_right = self.__tokenize_line(left), self.__tokenize_line(right)

            tokenized_line.extend(split_left)
            tokenized_line.extend([ord(":")])
            tokenized_line.extend(split_right)

            tokenized_line = [i for i in tokenized_line if i!='']
            return tokenized_line

        for i in range(len(self.keywords)):
            current_keyword = self.keywords[i]

            if current_keyword in line_no_quoted_material:
                split = line.index(current_keyword)
                self.line_tokens.append(current_keyword)
                
                left, right = line[0:split], line[split+len(current_keyword):]
                tokenized_line_left, tokenized_line_right = self.__tokenize_line(left), self.__tokenize_line(right)

                tokenized_line.extend(tokenized_line_left)
                tokenized_line.extend([self.v2_list[current_keyword]])
                tokenized_line.extend(tokenized_line_right)

                tokenized_line = [i for i in tokenized_line if i!='']
                return tokenized_line
            
        return self.__convert_to_list(line)

    def __write_to_ouput_file(self):
        out = open(self.outfile, "wb")
        entry_point, exit_point = self.memory_entry_point, self.memory_exit_point
        packed_entry_point,packed_exit_location = struct.pack('<H', entry_point), struct.pack('<H', exit_point)
        location = entry_point
        out.write(packed_entry_point)

        for line in self.tokenized_content:
            binary_line = self.__convert_line_to_binary(line)
            location = 2 + location + len(binary_line)
            packed_location = struct.pack('<H', location)
            out.write(packed_location)
            for i in binary_line:
                out.write(i)

        out.write(packed_exit_location)

    def __convert_line_to_binary(self, line_tuple):
        line_number, line_content = line_tuple[0], line_tuple[1]
        binary_line_number, binary_line_content = struct.pack('<H', int(line_number)), []

        for i in range(len(line_content)):
            if (type(line_content[i]) == str):
                binary_line_content.append(struct.pack('B', ord(line_content[i])))
                continue
            binary_line_content.append(struct.pack('B', (line_content[i])))

        binary_line_content.insert(0,struct.pack('B',binary_line_number[1]))
        binary_line_content.insert(0,struct.pack('B',binary_line_number[0]))
        binary_line_content.append(b'\x00')
        return binary_line_content

    def __strip_line_number(self, line, content_line_number):
        newline,num = '',''
        split = 0

        while (line[split].isnumeric()):
            num += line[split]
            split +=1    
        newline+=line[split:]

        if (not num):
            print("\nCHOMP64: Something went wrong. There is no line number present on line: " + str(content_line_number+1) + "\n")
            exit()

        newline = newline.strip()
        return (num, newline)
            
    def __remove_quoted_material(self,line):
        flag = False
        newstr = ''

        for char in line:
            if (not flag and char != '\"'):
                newstr += char

            if (char=='\"'):
                flag = not flag 

        return newstr                

    def __convert_to_list(self, line):
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
    t.tokenize()
    