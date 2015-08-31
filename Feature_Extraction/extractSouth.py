import sys
import re

def main(argv):
    input = open(argv[0], 'r')
    output = open('South.txt','w')
    url = ""
    for line in input:
        list = line.split()
        if len(list) == 2:
            if list[0] == 'Recno::':
                url = ""
            if list[0] == 'URL::':
                url = list[1]
                #output.write(url.split('/')[-1]+',')
        if len(list) > 2 and line.find(" Geographic Coverage ") != -1 and line.find(" S: ") != -1:
                index = list.index('S:')
                dt = list[index+1]
                if len(dt) == 3:
                    output.write(url.split('/')[-1]+','+dt+'\n')
    
if __name__=="__main__":
    main(sys.argv[1:])
