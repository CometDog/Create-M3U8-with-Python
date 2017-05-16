import sys
import os

#Init the basePath array
basePath = []

#Handle counting the args passed in
argCount = len(sys.argv)
if argCount != 3:
    if argCount < 3:
        raise Exception('Not enough arguments given')
    elif argCount > 3:
        raise Exception('Too many arguments given')
    sys.exit(1)

#Ensure the origin arg is an existing folder
if (os.path.exists(sys.argv[1])):
    if (os.path.isfile(sys.argv[1])):
        raise Exception('Orgin path is a file')
        sys.exit(1)
else:
    raise Exception('Orgin path does not exist')

#Ensure the destination arg is an existing folder, and if not, create it
if (os.path.exists(sys.argv[2])):
    if (os.path.isfile(sys.argv[2])):
        raise Exception('Destination path is a file')
        sys.exit(1)
else:
    os.makedirs(sys.argv[2])

#Split the intput args into arrays and count the size
origin = sys.argv[1].split('\\')
dest = sys.argv[2].split('\\')

originCount = len(origin)
destCount = len(dest)

#Handld figuring out the different in array lengths
if originCount > destCount:
    excessLen = originCount - destCount
    del origin[(originCount - excessLen):]
    originCount = destCount
elif destCount > originCount:
    excessLen = destCount - originCount
    del dest[(destCount - excessLen):]
    destCount = originCount
else:
    excessLen = 0

#Append navigation cues to the basePath for each excess between the paths, minus one because a folder becomes a file later (the m3u8)
if (excessLen != 0):
    for i in range (0, excessLen - 1):
        basePath.append('..')

#Append additional navigation out of unique folder structures so the file can navigate back down appropriately
for i in range (destCount - 1, 0, -1):
    basePath.append('..')
    destCount -= 1
    originCount -= 1
    del dest[(destCount)]
    del origin[(originCount)]
    if dest == origin:
        break

#Recreate the origin variable with an array of the origin, minus the path that is non-unique to the origin
origin = sys.argv[1].split('\\')
del origin[:originCount]
basePath.extend(origin)

#Get the file path and name, creating whatever is needed along the way
fileName = sys.argv[2] + '\\' + origin[len(origin) - 2]

if not os.path.exists(fileName):
    os.makedirs(fileName)

fileName = fileName + '\\' + origin[len(origin) - 1] + '.m3u8'

#Create the file and put the origin file names into the playlist, ignoring .jpg files
basePath = '\\'.join(map(str, basePath))
with open(fileName, 'w') as playlistFile:
    for name in os.listdir(sys.argv[1]):
        if (os.path.isfile(sys.argv[1] + '\\' + name)):
            if not name.endswith(".jpg"):
                playlistFile.write('%s\\%s\n' % (basePath, name))