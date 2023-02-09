//      TODO : REFACTOR INQUOTES FUNCTION
//             ADD FUNCTIONALITY FOR NEWER TOKENS AND/OR SPECIAL TOKENS
//             STREAMLINE FUNCTIONS
//             GOAL : FULLY TOKENIZE colon.bas
// 

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <cstring>
#include <map>
#include <fstream>
#include <chrono>
const std::string VERSION_NUMBER = "v1.1.0";
bool VERBOSE = false;
bool OVERWRITE = false; 
char NULL_TERMINATOR = 0x00;
char lineCount = 0x01;
short MEM_ENTRY_POINT = 0x0801;
short MEM_EXIT_POINT = 0x0000;
std::string INPUT_FILE;
std::string OUTPUT_FILE;

//list of C64 basic tokens
std::map<std::string, int> tokens = {
                                    {"REM", 0x8F}, {":",0x3A},{"END", 0x80},{"FOR", 0x81},{"NEXT", 0x82},
                                    {"DATA", 0x83},{"INPUT#", 0x84},{"INPUT", 0x85},{"DIM", 0x86},{"READ", 0x87},
                                    {"LET", 0x88},{"GOTO", 0x89},{"RUN", 0x8A},{"IF", 0x8B},{"RESTORE", 0x8C},
                                    {"GOSUB", 0x8D},{"RETURN", 0x8E},{"STOP", 0x90},{"ON", 0x91},{"WAIT", 0x92},
                                    {"LOAD", 0x93},{"SAVE", 0x94},{"VERIFY", 0x95},{"DEF", 0x96},{"POKE", 0x97},
                                    {"PRINT#", 0x98},{"PRINT", 0x99},{"CONT", 0x9A},{"LIST", 0x9B},{"CLR", 0x9C},
                                    {"CMD", 0x9D},{"SYS", 0x9E},{"OPEN", 0x9F},{"CLOSE", 0xA0},{"GET", 0xA1},
                                    {"NEW", 0xA2},{"TAB(", 0xA3},{"TO", 0xA4},{"FN", 0xA5},{"SPC(", 0xA6},
                                    {"THEN", 0xA7},{"NOT", 0xA8},{"STEP", 0xA9},{"+", 0xAA},{"-", 0xAB},
                                    {"*", 0xAC},{"/", 0xAD},{"^", 0xAE},{"AND", 0xAF},{"OR", 0xB0},
                                    {">", 0xB1},{"=", 0xB2},{"<", 0xB3},{"SGN", 0xB4},{"ABS", 0xB6},
                                    {"USR", 0xB7},{"FRE", 0xB8},{"POS", 0xB9},{"SQR", 0xBA},{"RND", 0xBB},
                                    {"LOG", 0xBC},{"EXP", 0xBD},{"COS", 0xBE},{"SIN", 0xBF}, {"TAN", 0xC0},
                                    {"ATN", 0xC1},{"PEEK", 0xC2},{"LEN", 0xC3},{"STR$", 0xC4},{"VAL", 0xC5},
                                    {"ASC", 0xC6},{"CHR$", 0xC7},{"LEFT$", 0xC8},{"RIGHT$", 0xC9},{"MID$", 0xCA},
                                    {"GO", 0xCB},{"INT", 0xB5},{"CONCAT",0xCC},{"DOPEN",0xCD},{"DCLOSE",0xCD},
                                    {"RECORD",0xCF},{"HEADER",0xD0},{"COLLECT", 0xD1},{"BACKUP", 0xD2},{"COPY", 0xD3},
                                    {"APPEND", 0xD4},{"DSAVE", 0xD5},{"DLOAD", 0xD6},{"CATALOG", 0xD7},
                                    {"RENAME", 0xD8}
                                    };

//? general purpose print function -- overload this as needed
void print(std::vector<std::string> vec, int valType) {
    switch (valType)
    {
    case 0:
        for(int i=0; i<vec.size();i++) {
            std::cout << vec.at(i);
        }    
        break;
    case 1:
        for(int i=0; i<vec.size();i++) {
            for(int j=0;j<vec.at(i).size();j++) {
                std::cout << std::hex << (int) vec.at(i)[j] <<" ";
            }
        }
        break;
    case 2:
        break;
    default:
        break;
    }
}


//CHECKS LEFT AND RIGHT OF START INDEX OF TOKEN FOR QUOTATION MARKS, TRUE IF INQUOTES, FALSE ELSE
bool inQuotes(std::string keyString, int startIndex) {
    int strIter = 0;
    short qMarkFlag = 0;
    while(strIter!=startIndex) {
        if (keyString[strIter] == 0x22){
            if(qMarkFlag==1) {
                qMarkFlag = 0;
            }
            else {
                qMarkFlag = 1;
            }
        }
        strIter++;
    }
    if(qMarkFlag == 1) {
        return true;
    }
    return false;
}

bool inRem(std::string keyString, int startIndex) {
    size_t remarkFind = keyString.find("REM");
    if(remarkFind!=std::string::npos) {
        return true;
    }
    return false;
}

//SEARCHES LINE FOR KEY VALUES FOUND IN MAP "TOKENS" AND RETURNS START INDEX OF TOKEN KEYWORD 
std::string keySearch(std::string searchString) {
    auto mapIterator = tokens.begin();
    size_t keyStart;
    while(mapIterator != tokens.end()) {
        keyStart = searchString.find(mapIterator->first);
        if(keyStart!=std::string::npos && !inQuotes(searchString, keyStart)) {
            if(mapIterator->first!="REM" && inRem(searchString,keyStart-1)) {
                ++mapIterator;
                continue;
            }
            if(mapIterator->first=="INT" && searchString[keyStart-1]=='R') {
                ++mapIterator;
                continue;
            }
            if(mapIterator->first=="GO" && searchString[keyStart+2]=='T') {
                ++mapIterator;
                continue;
            }
            if(mapIterator->first=="GO" && searchString[keyStart+2]=='S') {
                ++mapIterator;
                continue;
            }
            if(mapIterator->first=="PRINT" && searchString[keyStart+5]=='#') {
                ++mapIterator;
                continue;
            }
            break;
        }
        ++mapIterator;
    }
    if(keyStart==std::string::npos) {
        return "NULL";
    }
    return mapIterator->first;
}

//RETURNS LINE NUMBER OF INPUT LINE
short getLineNum(std::string line) {
    int index=0;
    std::string numString = "";
    while(line[index]<=0x39 && line[index] >= 0x30) {
        numString+=line[index];
        index++;
    }
    return (short)std::stoi(numString);
}

//RETURNS STRING WITHOUT LINE NUMBER
std::string remLineNum(std::string line) {
    int index=0;
    std::string substring = "";
    while(line[index]<=0x39 && line[index] >= 0x30) {
        line.erase(line.begin()+index);
    }
    return line;
}

short lowHighConcat(short high, short low) {
    return (high * 256 + low);    
}

void tokenizer(std::string input, std::string outfile) {
    std::fstream out(outfile, std::fstream::app | std::fstream::binary);
    std::map<std::string, int>::iterator iterator;
    std::string key = keySearch(input); 
    int index=0;
    if(key=="NULL") {
        for(int i=0; i<input.size(); i++) {
            if(input[i]==0xa) {                
                out.write(reinterpret_cast<char*>(&NULL_TERMINATOR), sizeof(NULL_TERMINATOR));
            }
            else {
                out.write(reinterpret_cast<char*>(&input[i]), sizeof(input[i]));
            }
        }
        out.close();
    }
    else {
        if(input.find(key)>0){
            tokenizer(input.substr(0, input.find(key)), outfile);
            tokenizer(input.substr(input.find(key)), outfile);
        }
        else {
            iterator=tokens.find(key);
            char val = iterator->second;
            out.write(reinterpret_cast<char*>(&val), sizeof(val)); 
            out.close();
            while(index<(iterator->first).length()) {
                index+=1;
            }
            tokenizer(input.substr(index), outfile);
        }
    }
}

void fWriter(std::string outputFile, std::vector<char[]>) {
    std::fstream binOut(outputFile,std::fstream::out | std::fstream::binary);
    binOut.write(reinterpret_cast<char*>(&MEM_ENTRY_POINT),sizeof(MEM_ENTRY_POINT));



    binOut.write(reinterpret_cast<char*>(&MEM_EXIT_POINT),sizeof(MEM_EXIT_POINT));
    binOut.close();
}

std::vector<char> tokenize(std::vector<std::string> basicContent){
    std::vector<char> tokenContent;
    short characterCount, lineNum = 0x0000;

    return tokenContent;
}

//Appends a CR to the end of the file if not present -- helps tokenizer
void validateInFile(std::string file) {
    std::ifstream in(file);
    if (!in) {
        std::cout << "File does not exist: " << file;
    }
    std::ofstream out;
    char fileChar;
    while (in >> std::noskipws >> fileChar) {
        if(in.peek()==std::fstream::traits_type::eof() && fileChar!='\n') {
            out.open(file, std::fstream::app);
            out << "\n";
            out.close();
        }
    }
    in.close();
}


//             while(remLineNum(line)[lineIterator] != 0xA) {
//                 lineCount+=0x01;
//                 lineIterator++;
//             }
//             short countEncode = lowHighConcat(0x08, lineCount);
//             out.write(reinterpret_cast<char*>(&countEncode), sizeof(countEncode));
//             short lineNumEncode = lowHighConcat(0x00, getLineNum(line));
//             out.write(reinterpret_cast<char*>(&lineNumEncode), sizeof(lineNumEncode));
//             out.close();
//             tokenizer(remLineNum(line), outfile);
//             line="";
//         }
//     }
//     out.open(outfile, std::fstream::app | std::fstream::binary);
//     out.write(reinterpret_cast<char*>(&NULL_TERMINATOR), sizeof(NULL_TERMINATOR));
//     out.write(reinterpret_cast<char*>(&NULL_TERMINATOR), sizeof(NULL_TERMINATOR));
//     out.close();                          
//     in.close();
// }

//parses input file, breaks into line-by-line, returns as vector<string>
std::vector<std::string> fReaderSplitter(std::string inputFile) {
    char fileChar;            
    std::string line;
    std::vector<std::string> contents;
    std::ifstream in(inputFile);
    while (in >> std::noskipws >> fileChar) {
        line+=fileChar;
        if(fileChar==0xA) {
            for(int i=0; i<line.size(); i++) {
                line[i]=toupper(line[i]);
            }
            contents.push_back(line);
            line="";
        }
    }
    in.close();
    return contents;
}

//TODO: FINISH THIS
void CLIValidation(int argc, char * argv[]) {
    //std::cout << argv[1] << std::endl;
    if (argc > 10) {
        std::cout << "CHOMP: Error. Too many input parameters.\n\n";
    }
    if (argc == 1) {
        std::cout << "=======================\n| CHOMP C64 Tokenizer |\n=======================\n-h for help.\n\n";
        exit(0);
    }
    if (strcmp(argv[1],"-h")==0||strcmp(argv[1],"--help")==0) {
        std::cout << "\nUsage:\n\n\
chomp -h, --help\t\t\t\tCommand help\n\
chomp --v, -version\t\t\t\tVersion\n\
chomp <PATH_TO_FILE1> <PATH_TO_FILE2>\t\tTokenize file1, output binary to file 2\n\
\nTokenizer Flags:\n\n\
chomp <PATH_TO_FILE1> -v <PATH_TO_FILE2>\tVerbose\n\
chomp <PATH_TO_FILE1> -o <PATH_TO_FILE2>\tOverwrite file2 if file2 exists.\n\n";
        exit(0);
    }
    else if (std::strcmp(argv[1],"-v")==0||strcmp(argv[1],"--version")==0) {
        std::cout << VERSION_NUMBER + "\n";  
        exit(0);
    }
    else {
        std::ifstream inCheck(argv[1]);
        if (!inCheck) {
            std::cout << "CHOMP: Error. could not open input file.\n\n";
            exit(1);
        }

    }

}

int main(int argc, char * argv[]) {
    //CLIValidation(argc,argv);    
    std::string inputFile = argv[1];  //.bas
    std::string outputFile = argv[2]; //.prg
    //validateInFile(inputFile);
    std::vector<std::string> bProgram = fReaderSplitter(inputFile);
    //std::vector<char[]> tProgram = tokenize(bProgram);
    //fWriter(outputFile, tProgram);
    return 0;
}