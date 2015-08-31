import sys
import os
import pickle

def main(argv):
    #pr = {}
    input = open(argv[0],'r')
    '''for line in input: 
        list = line.split()
        pr[list[0]] = list[1]

    for count in range(int(argv[0])):
        id = 'doc'+str(count+1)'''
    for line in input: 
        list = line.split()
        #if id in pr:
        input = "curl http://localhost:8983/solr/update -H 'Content-type:application/json' -d '[{\"id\": \""+list[0]+"\",\""+argv[1]+"\"   : {\"set\":\""+list[1]+"\"}}]'"
        '''else:
            input = "curl http://localhost:8983/solr/update -H 'Content-type:application/json' -d '[{\"id\": \"doc"+str(count+1)+"\",\""+argv[1]+"\"   : {\"set\":\""+str(0)+"\"}}]'"'''
        os.system(input)
    
if __name__=="__main__":
    main(sys.argv[1:])
