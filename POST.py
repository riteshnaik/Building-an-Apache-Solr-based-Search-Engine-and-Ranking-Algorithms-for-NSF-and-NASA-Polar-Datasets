import sys
import os
import pickle

def main(argv):
    count = 50000
    doc_map = {}
    for f in os.listdir("/home/ritesh/CSCI572/lucene_solr_4_10/solr/example/exampledocs/ACADIS_Dump/"):
        count = count + 1
        idName = 'doc'+str(count)
        doc_map[idName] = f
        input = "curl 'http://localhost:8983/solr/update/extract?literal.id="+idName+"&commit=true' -F 'myfile=@example/exampledocs/ACADIS_Dump/"+f+"'"
        os.system(input)
    doc_map_dump = open('dump2.docMap', 'wb')
    pickle.dump(doc_map, doc_map_dump)
    doc_map_dump.close()

if __name__=="__main__":
    main(sys.argv[1:])
