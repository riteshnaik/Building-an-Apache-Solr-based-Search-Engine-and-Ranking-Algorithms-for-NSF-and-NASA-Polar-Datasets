import sys
import pickle

def main(argv):
    url_map_file = open('dump2.fileMap', 'rb')
    url_map = pickle.load(url_map_file)
    url_map_file.close()
    input = open(argv[0],'r')
    output =open(argv[1],'w')
    for line in input:
        list = line.split(',')
        if list[0] in url_map:
            output.write(url_map[list[0]]+' '+list[1])         
    
if __name__=="__main__":
    main(sys.argv[1:])
