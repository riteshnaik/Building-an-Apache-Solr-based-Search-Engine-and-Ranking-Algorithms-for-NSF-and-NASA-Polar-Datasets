import urllib2
import sys
import xml.etree.ElementTree as ET
import time
import pickle

def main(argv):
    doc1_map_file = open('dump.docMap', 'rb')
    doc1_map = pickle.load(doc1_map_file)
    doc1_map_file.close()

    doc2_map_file = open('dump2.docMap', 'rb')
    doc2_map = pickle.load(doc2_map_file)
    doc2_map_file.close()

    query = argv[0]
    
    raw = open('raw.xml','w')
    response = urllib2.urlopen("http://localhost:8983/solr/select?q="+query)
    xml = response.read()
    raw.write(xml)
    raw.close()
    tree = ET.parse('raw.xml')
    root = tree.getroot()
    result = root.find('result')
    #print(root)
    for doc in result.findall('doc'):
        id = doc.find('str').text
        if id in doc1_map:
            print(doc1_map[id])
        if id in doc2_map:
            print(doc2_map[id])

if __name__=="__main__":
    main(sys.argv[1:])
