import sys
import json
import math

def main(argv):
    '''input = open(argv[0],'r')
    output =open(argv[1],'w')
    for line in input:
        list = line.split(',')
        if list[0] in url_map:
            output.write(url_map[list[0]]+' '+list[1])'''
    input = open('pr.txt','r')
    ginput = open('gr_links.txt','r')
    count = 1
    nodeC = {}
    root = {}
    data = {}
    temp = {}
    nodes = []
    links = []
    for line in input:
        list = line.split()
        data['group'] = math.ceil((float(list[1])*100000 - 53)/3)
        data['name'] = list[0]
        if list[0] not in nodeC:
            nodeC[list[0]] = count
            count += 1
        nodes.extend([data])
        data = {}
    for line in ginput:
        list = line.split()
        temp['value'] = int(list[2])
        temp['target'] = nodeC[list[1]]
        temp['source'] = nodeC[list[0]]
        links.extend([temp])
        temp = {}
    root['links'] = links
    root['nodes'] = nodes
    json_data = json.dumps(root)
    output = open('output.json','w')
    #json.dump(json_data, output)
    print json_data        
    
if __name__=="__main__":
    main(sys.argv[1:])
