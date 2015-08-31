import sys
import re

def main(argv):
    input = open('test.txt', 'r')
    output = open('feature.txt','w')
    features = {}
    for line in input:
        list = line.split(',')
        if len(list) == 3 and len(list[2]) > 1 :
            feature_list = list[2].strip().split(' > ')
            for feature in feature_list:
                if feature not in features:
                     features[feature] = 1
                else:
                     features[feature] = features[feature] + 1       
    print(len(features))
    for key,value in features.items():
        output.write(key+' '+str(value)+'\n')

if __name__=="__main__":
    main(sys.argv[1:])
