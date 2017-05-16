import sys
import os

#Init the basePath array
basePath = []
compCount = 0

def getUserYN(query):
    validInput = {'yes': True, 'y': True,
        'no': False, 'n': False}
    prompt = '[y/n]'

    while True:
        sys.stdout.write(query + ' - ' + prompt + ': ')
        userInput = input().lower()
        if userInput in validInput:
            return validInput[userInput]
        else:
            sys.stdout.write("Only enter yes or no.\n")

def verifyArgs(arg1, arg2):
    #Ensure the origin arg is an existing folder
    if (os.path.exists(arg1)):
        if (os.path.isfile(arg1)):
            raise Exception('Orgin path is a file')
            sys.exit(1)
    else:
        raise Exception('Orgin path does not exist')

    #Ensure the destination arg is an existing folder, and if not, create it
    if (os.path.exists(arg2)):
        if (os.path.isfile(arg2)):
            raise Exception('Destination path is a file')
            sys.exit(1)
    else:
        os.makedirs(arg2)

def createPaths(arg1, arg2):
    global compCount
    global basePath

    #Split the input args into arrays and count the size
    origin = arg1.split('\\')
    dest = arg2.split('\\')
    originLen = len(origin)
    destLen = len(dest)

    #Handle figuring out the difference in array lengths
    if originLen > destLen:
        excessLen = originLen - destLen
        del origin[(originLen - excessLen):]
        compCount = destLen
    elif destLen > originLen:
        excessLen = destLen - originLen
        del dest[(destLen - excessLen):]
        compCount = originLen
    else:
        excessLen = 0

    #Append navigation cues to the basePath for each excess between the paths, minus one because a folder becomes a file later (the m3u8)
    if (excessLen != 0):
        for i in range (0, excessLen - 1):
            basePath.append('..')

    #Append additional navigation out of unique folder structures so the file can navigate back down appropriately
    for i in range (compCount - 1, 0, -1):
        basePath.append('..')
        compCount -= 1
        del dest[(compCount)]
        del origin[(compCount)]
        if dest == origin:
            break

def writeToFile(arg1, arg2):
    global basePath

    #Create the origin variable with an array of the origin, minus the path that is non-unique to the origin
    origin = sys.argv[1].split('\\')
    del origin[:compCount]
    basePath.extend(origin)

    #Get the file path and name, creating whatever is needed along the way
    fileName = sys.argv[2] + '\\' + origin[len(origin) - 2]

    if not os.path.exists(fileName):
        os.makedirs(fileName)

    fileName = fileName + '\\' + origin[len(origin) - 1] + '.m3u8'

    if os.path.exists(fileName):
        if os.path.isfile(fileName):
            userInput = getUserYN('File already exists. Overwrite? Not doing so will exit the script.')
            if userInput:
                os.remove(fileName)
            else:
                sys.stdout.write('File not changed.')
                sys.exit(2)
        else:
            sys.stdout.write('The given file is already a folder. Please remove this folder to continue.')

    #Create the file and put the origin file names into the playlist, ignoring .jpg files
    basePath = '\\'.join(map(str, basePath))
    with open(fileName, 'w') as playlistFile:
        for name in os.listdir(sys.argv[1]):
            if (os.path.isfile(sys.argv[1] + '\\' + name)):
                if not name.endswith('.jpg'):
                    playlistFile.write('%s\\%s\n' % (basePath, name))

#Handle counting the args passed in
argCount = len(sys.argv)
if argCount != 3:
    if argCount < 3:
        raise Exception('Not enough arguments given')
    elif argCount > 3:
        raise Exception('Too many arguments given')
    sys.exit(1)

verifyArgs(sys.argv[1], sys.argv[2])
createPaths(sys.argv[1], sys.argv[2])
writeToFile(sys.argv[1], sys.argv[2])