import sys
import re

def main(argv):
    input = open(argv[0], 'r')
    output = open('MaxAltitude.txt','w')
    url = ""
    for line in input:
        list = line.split()
        if len(list) == 2:
            if list[0] == 'Recno::':
                url = ""
            if list[0] == 'URL::':
                url = list[1]
                #output.write(url.split('/')[-1]+',')
        if len(list) > 2 and line.find("Max Altitude:") != -1:
                index = list.index('Altitude:')
                dt = list[index+1]
                if len(dt) == 3:
                    output.write(url.split('/')[-1]+','+dt+'\n')
    
if __name__=="__main__":
    main(sys.argv[1:])
