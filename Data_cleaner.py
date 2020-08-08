import csv

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


def offset(filename):
    
    with open(filename + '-NoDupes.csv','r') as inFile, open(filename + '-CLEAN.csv','w') as outFile:
        
        header = next(inFile, None)
        if header:
            outFile.write(header)
        
        victories = []
        losses = []
        for line in inFile:
            if line.split(',')[1] == "Victory":
                victories.append(1)
            elif line.split(',')[1] == "Defeat":
                losses.append(0)
        print(str(len(victories)) +" wins, and " + str(len(losses)) + " losses" )
            # outFile.write(line)


removeDupes("games")
offset("games")