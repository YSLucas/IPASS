import csv
import os

def removeDupes(filename):

    with open(filename + '.csv','r') as inFile, open(filename + '-NoDupes.csv','w') as outFile:
        
        header = next(inFile, None)
        if header:
            outFile.write(header)
        
        checked = set()
        for line in inFile:
            if line.split(',')[13] in checked:
                continue

            checked.add(line.split(',')[13])
            outFile.write(line)


def removeOffset(filename, offsetCount, offsetSide, rank):

    if not os.path.isfile('./gamesAllServers9-8-CLEAN.csv'):
        with open(filename + '-NoDupes.csv','r') as inFile, open(filename + '-CLEAN.csv','w') as outFile:
            
            header = next(inFile, None)
            if header:
                outFile.write(header)

            for line in inFile:
                if (offsetCount > 0) and (line.split(',')[1] == offsetSide) and (line.split(',')[0] == rank):
                    offsetCount -= 1
                    continue

                outFile.write(line)
        return offsetCount
    else:
        with open(filename + '-CLEAN.csv','r') as inFile, open(filename + '-CLEANv2.csv','w') as outFile:
            
            header = next(inFile, None)
            if header:
                outFile.write(header)

            for line in inFile:
                if (offsetCount > 0) and (line.split(',')[1] == offsetSide) and (line.split(',')[0] == rank):
                    offsetCount -= 1
                    continue

                outFile.write(line)
        return offsetCount


def offset(filename):
    
    with open(filename + '-NoDupes.csv','r') as inFile:
        
        header = next(inFile, None)
        
        victories = 0
        losses = 0
        for line in inFile:
            if line.split(',')[1] == "Victory":
                victories += 1
            elif line.split(',')[1] == "Defeat":
                losses += 1
        print(str(victories) +" wins, and " + str(losses) + " losses" )

        if victories > losses:
            offsetSide = "Victory"
        elif losses > victories:
            offsetSide = "Defeat"
        elif losses == victories:
            return "Perfectly balanced, as all things should be."
        offsetCount = max(victories, losses) - min(victories, losses)
        print(offsetCount, offsetSide)
    
    offsetCount = removeOffset(filename, offsetCount, offsetSide, "Diamond 3")
        
    if offsetCount > 0:
        print(offsetCount)
        removeOffset(filename, offsetCount, offsetSide, "Diamond 2")

        
    with open(filename + '-CLEANv2.csv','r') as checkFile:
        victories = 0
        losses = 0
        for line in checkFile:
            if line.split(',')[1] == "Victory":
                victories += 1
            elif line.split(',')[1] == "Defeat":
                losses += 1
        if victories == losses:
            print(str(victories) +" wins, and " + str(losses) + " losses. Perfectly balanced, as all things should be." )
        else:
            print(str(victories) +" wins, and " + str(losses) + " losses. Oops, something went wrong." )
        


removeDupes("gamesAllServers9-8")
offset("gamesAllServers9-8")