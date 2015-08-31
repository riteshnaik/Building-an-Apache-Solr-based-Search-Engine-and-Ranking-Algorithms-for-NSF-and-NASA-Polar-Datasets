import pickle
import sys

def main(argv):
    doc_map_file = open('dump2.docMap', 'rb')
    doc_map = pickle.load(doc_map_file)
    doc_map_file.close()
    url_map = {y:x for x,y in doc_map.iteritems()}
    url_map_dump = open('dump2.fileMap', 'wb')
    pickle.dump(url_map, url_map_dump)
    url_map_dump.close()

if __name__=="__main__":
    main(sys.argv[1:])
