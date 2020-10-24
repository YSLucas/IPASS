import csv
import os

def mergeCSV(filename1, filename2):
    
    with open(filename1 + '.csv','r') as file01, open(filename2 + '.csv','r') as file02, open('gamesCombined.csv','w') as outFile:

        header1 = next(file01, None)
        header2 = next(file02, None)
        if header1:
            outFile.write(header1)
        
        for line in file01:
            outFile.write(line)

        for line in file02:
            outFile.write(line)

def removeDupes(filename):
    """Removes games die meer dan één keer in de database staan zodat er maar 1 overblijft"""
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


def removeOffset(filename, offsetCount, offsetSide, rank, id):
    """Deze functie maakt de wins en losses in een database gelijk"""
    if not os.path.isfile('./' + filename + '-CLEANv1.csv'):
        with open(filename + '-NoDupes.csv','r') as inFile, open(filename + '-CLEANv1.csv','w') as outFile:
            
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
        with open(filename + '-CLEANv' + str((id - 1)) + '.csv','r') as inFile, open(filename + '-CLEANv' + str(id) + '.csv','w') as outFile:
            
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
    """Deze functie checkt hoe de losses en wins verdeeld zijn in de dataset en roept daaran removeOffset aan met de juiste parameters."""
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
    
    offsetCount = removeOffset(filename, offsetCount, offsetSide, "Diamond 3", 1)
        
    if offsetCount > 0:
        print(offsetCount)
        offsetCount = removeOffset(filename, offsetCount, offsetSide, "Diamond 2", 2)
    
    if offsetCount > 0:
        print(offsetCount)
        #   we zullen vrijwel nooit verder hoeven te gaan dan Diamond 1 om de Win/Loss ratio 50% te maken, daarom is dit de laatste keer dat we removeOffset() aanvragen
        offsetCount = removeOffset(filename, offsetCount, offsetSide, "Diamond 1", 3)

        
    with open(filename + '-CLEANv3.csv','r') as checkFile:
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
            print(str(victories) +" wins, and " + str(losses) + " losses." )
        

def cleanData(filename1, filename2, outFilename):

    mergeCSV(filename1, filename2)
    removeDupes(outFilename)
    offset(outFilename)

cleanData("gamesAllServers9-8", "gamesAllServers14-8", "gamesCombined")