# Skeleton Program for the AQA AS1 Summer 2020 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA AS1 Programmer Team
# developed in a Python 3 environment

# Version number: 0.0.0
EMPTY_STRING = ''
MAX_WIDTH = 100
MAX_HEIGHT = 100

class FileHeader:
    def __init__(self):
        self.Title = EMPTY_STRING
        self.Width = MAX_WIDTH
        self.Height = MAX_HEIGHT
        self.FileType = EMPTY_STRING 

def DisplayError(ErrorMessage):
    print("Error: ", ErrorMessage)

def PrintHeading(Heading):
    print(Heading)
    HeadingLength = len(Heading)
    for Position in range(1, HeadingLength + 1):
        print('=', end='')
    print()

def DisplayImage(Grid, Header):
    print()
    PrintHeading(Header.Title)
    for ThisRow in range(Header.Height):
        for ThisColumn in range(Header.Width):
            print(Grid[ThisRow][ThisColumn], end='')
        print()

def Border(Grid, Header):
    border = EMPTY_STRING 
    while len(border) != 1:
        border = str(input("Enter border character: "))
    NewGrid = [['' for Column in range(MAX_WIDTH)] for Row in range(MAX_HEIGHT)]
    Header.Height += 2
    Header.Width += 2
    for x in range(Header.Width):
      NewGrid[0][x] = border
      NewGrid[Header.Height-1][x] = border
    for y in range(Header.Height):
      NewGrid[y][0] = border
      NewGrid[y][Header.Width-1] = border
    for ThisRow in range(Header.Height-2):
      for ThisColumn in range(Header.Width-2):
        NewGrid[ThisRow+1][ThisColumn+1] = Grid[ThisRow][ThisColumn]
    Grid = NewGrid
    DisplayImage(Grid, Header)


#    Header.Height += 2
#    Header.Width += 2
#    for ThisRow in range(Header.Height):
#        a = border
#        ThisColumn = 0
#        while ThisColumn <= Header.Width:
#            b = Grid[ThisRow][ThisColumn]
#            Grid[ThisRow][ThisColumn] = a
#            a = Grid[ThisRow][ThisColumn+1]
#            Grid[ThisRow][ThisColumn+1]
#            ThisColumn += 2
     
#    b = Grid[0][0] #assign b value of 00
#    Grid[0][0] = a #assign 00 value of a
#    a = Grid[0][1] #reassign a value of 01
#    Grid[0][1] = b #assign 01 value of b
    
#    b = Grid[0][2] #reassign b value of 02
#    Grid[0][2] = a #assign 02 value of a
#    a = Grid[0][3] #reassign a value of 03
#    Grid[0][3] = b #assign 03 value of b
    
#    b = Grid[0][4] #reassign b value of 04
#    Grid[0][4] = a #assign 04 value of a
#    a = Grid[0][5] #reassign a value of 05
#    Grid[0][5] = b #assign 05 value of b
            
    

def SaveImage(Grid, Header):
    print("The current title of your image is: " + Header.Title)
    Answer = input("Do you want to use this as your filename? (Y/N) ")
    if Answer == "N" or Answer == "n":
        FileName = input("Enter a new filename: ")
    else:
        FileName = Header.Title
    FileOut = open(FileName + ".txt", 'w')
    FileOut.write(Header.Title + '\n')
    for Row in range(Header.Height):
        for Column in range(Header.Width):
            FileOut.write(Grid[Row][Column])
        FileOut.write('\n')
    FileOut.close()

def EditImage(Grid, Header):
    DisplayImage(Grid, Header)
    Answer = EMPTY_STRING
    while Answer != "N":
        Symbol = EMPTY_STRING
        NewSymbol = EMPTY_STRING
        count = 0
        while len(Symbol) != 1:
            Symbol = input("Enter the symbol you want to replace: ")
        while len(NewSymbol) != 1:
            NewSymbol = input("Enter the new symbol: ")
        for ThisRow in range(Header.Height):
            for ThisColumn in range(Header.Width):
                if Grid[ThisRow][ThisColumn] == Symbol:
                    Grid[ThisRow][ThisColumn] = NewSymbol
                    count += 1
        print(Symbol, "was replaced by", NewSymbol, ", and in total", count, "pixels were modified")
        DisplayImage(Grid, Header)
        Answer = input("Do you want to make any further changes? (Y/N) ")
    return Grid

def ConvertChar(PixelValue):
    if PixelValue <= 32:
        AsciiChar = '#'
    elif PixelValue <= 64:
        AsciiChar = '&'
    elif PixelValue <= 96:
        AsciiChar = '+'
    elif PixelValue <= 128:
        AsciiChar = ';'
    elif PixelValue <= 160:
        AsciiChar = ':'
    elif PixelValue <= 192:
        AsciiChar = ','
    elif PixelValue <= 224:
        AsciiChar = '.'
    else:
        AsciiChar = ' '
    return AsciiChar

def LoadGreyScaleImage(FileIn, Grid, Header):
    try:
        for Row in range(Header.Height):
            for Column in range(Header.Width):
                NextPixel = FileIn.readline()
                PixelValue = int(NextPixel)
                Grid[Row][Column] = ConvertChar(PixelValue)
    except:
        DisplayError("Image data error")        
    return Grid
    
def LoadAsciiImage(FileIn, Grid, Header):
    try:
        ImageData = FileIn.readline()
        NextChar = 0
        for Row in range(Header.Height):
            for Column in range(Header.Width):
                Grid[Row][Column] = ImageData[NextChar]
                NextChar += 1
    except:
        DisplayError("Image data error")
    return Grid
        
def LoadFile(Grid, Header):
    FileFound = False
    FileTypeOK = False
    FileName = input("Enter filename to load: ")
    try:
        FileIn = open(FileName + ".txt", 'r')
        FileFound = True
        HeaderLine = FileIn.readline()
        Fields = HeaderLine.split(',')
        Header.Title = Fields[0]
        Header.Width = int(Fields[1])
        Header.Height = int(Fields[2])
        Header.FileType = Fields[3]
        Header.FileType = Header.FileType[0]
        if Header.FileType == 'A':    
            Grid = LoadAsciiImage(FileIn, Grid, Header)
            FileTypeOK = True
        elif Header.FileType == 'G': 
            Grid = LoadGreyScaleImage(FileIn, Grid, Header)
            FileTypeOK = True
        FileIn.close()
        if not FileTypeOK:
            DisplayError("Unknown file type")
        else:
            DisplayImage(Grid, Header)
    except:
        if not FileFound:
            DisplayError("File not found")
        else:
            DisplayError("Unknown error")
    return Grid, Header

def SaveFile(Grid, Header):
    FileName = input("Enter filename: ")
    FileOut = open(FileName + ".txt", 'w')
    FileOut.write(Header.Title + ',' + str(Header.Width) + ',' + str(Header.Height) + ',' + 'A' + '\n')
    for Row in range(Header.Height):
        for Column in range(Header.Width):
            FileOut.write(Grid[Row][Column])
    FileOut.close()

def ClearGrid(Grid):
    for Row in range(MAX_HEIGHT):
        for Column in range(MAX_WIDTH):
            Grid[Row][Column] = '.'
    return Grid
     
def DisplayMenu():
    print()
    print("Main Menu")
    print("=========")
    print("L - Load graphics file") 
    print("D - Display image")
    print("E - Edit image")
    print("S - Save image")
    print("B - Add a border to the current image")
    print("X - Exit program") 
    print()

def GetMenuOption():
    MenuOption = EMPTY_STRING
    while len(MenuOption) != 1:
        MenuOption = input("Enter your choice: ")
    return MenuOption
    
def Graphics():
    Grid = [['' for Column in range(MAX_WIDTH)] for Row in range(MAX_HEIGHT)]
    Grid = ClearGrid(Grid)
    Header = FileHeader()
    ProgramEnd = False
    while not ProgramEnd:
        DisplayMenu()
        MenuOption = GetMenuOption()        
        if MenuOption == 'L':
            Grid, Header = LoadFile(Grid, Header)
        elif MenuOption == 'D':
            DisplayImage(Grid, Header) 
        elif MenuOption == 'E':
            Grid = EditImage(Grid, Header) 
        elif MenuOption == 'S':        
            SaveImage(Grid, Header)
        elif MenuOption == 'X':
            ProgramEnd = True
        elif MenuOption == 'B':
            Border(Grid, Header)
        else:
            print("You did not choose a valid menu option. Try again")
    print("You have chosen to exit the program")
    Answer = input("Do you want to save the image as a graphics file? (Y/N) ")
    if Answer == "Y" or Answer == "y":
        SaveFile(Grid, Header)
            
if __name__ == "__main__":
    Graphics()                 


