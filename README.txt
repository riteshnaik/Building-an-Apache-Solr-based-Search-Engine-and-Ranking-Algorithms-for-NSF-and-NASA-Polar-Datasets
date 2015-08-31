CSCI 572: Assignment II Report
Building an Apache-Solr based Search Engine and Ranking Algorithms for NSF and NASA Polar Datasets

Team Members:
Ritesh Naik, Ananya Acharya, Anuraj Shetty, Namrata Malarout and Shambhavi Punja

==============================================
LIST OF FILES (directory structure maintained)
==============================================
1. lucene_solr_4_10/solr/example/solr/collection1/schema.xml
2. lucene_solr_4_10/solr/example/solr/collection1/solrconfig.xml
3. lucene_solr_4_10/solr/example/solr/POST.py

4. Feature_Extraction/countFeatures.py
5. Feature_Extraction/extractEast.py
6. Feature_Extraction/extractEndYear.py
7. Feature_Extraction/extractMaxAltitude.py
8. Feature_Extraction/extractMaxDepth.py
9. Feature_Extraction/extractMinAltitude.py
10. Feature_Extraction/extractMinDepth.py
11. Feature_Extraction/extractNorth.py
12. Feature_Extraction/extractSouth.py
13. Feature_Extraction/extractStartYear.py
14. Feature_Extraction/extractWest.py
15. Feature_Extraction/convert.py
16. Feature_Extraction/createfileMap.py

17. CLAVIN/src/main/java/com/bericotech/clavin/resolver/ResolvedLocation.java
18. CLAVIN/src/main/java/com/bericotech/clavin/WorkflowDemo.java

19. nutch_solr_config/schema.xml
20. nutch_solr_config/solrconfig.xml

21. createJSON.py
===========================
BUILD AND EXECUTION STEPS
===========================
A. Script to index all files into Solr
--------------------------------------
This python script is uses curl command to POST all the documents to Solr, where curl uses extractingRequestHandler() to extract features. This script must be placed in lucene_solr_4_10/solr

$ python POST.py

Note: 'dump' folder must be copied to lucene_solr_4_10/solr/example/exampledocs/<respective AMD/ACADIS dump folder>
-------------------------------------
B. Feature Extraction
-------------------------------------
How to create 'dump' file:
Step 1: Merge all the segments from the segmentDB.
Step 2: Dump merged segments to a file.
Step 3: Perform feature extraction using the feature extraction scripts in Feature_Extraction folder
Ex:
$python extractEast.py <path to dump file> - Generates a respective feature file Eg:'East.txt'
$python createFileMap - generates a dictionary file with mapping between filename and indexed document ID in the SOLR 
$python convert.py East.txt East_New.txt - Generates a feature file with filename mapped to respective document ID

CLAVIN must be executed from CLAVIN/ directory and command to execute is
MAVEN_OPTS="-Xmx2g" mvn exec:java -Dexec.mainClass="com.bericotech.clavin.WorkflowDemo"

Input directory path: /home/<dump folder name>
Output directory: /home/countries_found.txt

-----------------------------
C. Update.py (Utility script)
-----------------------------
This python script is a tool to add new field to documents that are already indexed in Solr. This script is used after feature extraction to add the following fields:
STARTYEAR
ENDYEAR
NORTH
SOUTH
EAST
WEST
MAXALT (Max. Altitude)
MINALT (Min. Altitude)
MAXDEP (Max. Depth)
MINDEP (Min. Depth)
PRSCORE (Pagerank score)

$python Update.py <feature file th filename mapped to respective document ID>

---------------------
D. createGraph.py
---------------------
This python script creates a graph with documents as nodes and an edge is created when there is a common feature between these documents. This script uses networkx python library to use the Graph APIs.

$ python createGraph.py <featureFile>

---------------
E. pageRank.py
---------------
This python script uses the graph created by createGraph to compute scores for the documents using the page-rank algorithm. It generates a pr.txt file which has two fields - filename and score.

$ python pageRank.py

-------------------------------------
F. Script to Query and obtain results
-------------------------------------
This python script is used to Query the indexed files in Solr and obtain the results

$python getResult.py <query string>

Whitespace in the URL must be replaced with '%20' and quotes ("") with '%22'

Ex: $python getResult.py '%22Antarctica%20Ocean%22'

-------------------------------------
G. Schema.xml
-------------------------------------
Use this configuration Schema.xml file for Solr configuration setting. It has been updated with the following added fields.
STARTYEAR
ENDYEAR
NORTH
SOUTH
EAST
WEST
MAXALT (Max. Altitude)
MINALT (Min. Altitude)
MAXDEP (Max. Depth)
MINDEP (Min. Depth)
PRSCORE (Pagerank score)

Analyzers added to the content fields are as follows:
solr.HTMLStripCharFilterFactory -  This is to strip HTML and XML elements.
solr.StopFilterFactory - This is to remove stop words.
solr.LowerCaseFilterFactory - This is to convert the entire text to lower case.
solr.PorterStemFilterFactory - This is used for stemming.

Copy fields added are as follows:
exactMatch

------------------------------------------
H. solrconfig.xml for requests from Nutch
------------------------------------------
In solrconfig.xml we added a requestHandler="/nutch" class="solr.SearchHandler" to tell solr to listen to requests from Nutch.

Use the following config files for this purpose.
nutch_solr_config/schema.xml
nutch_solr_config/solrconfig.xml

==========================
 RESULT - Query Execution
==========================

getResult.py, this python script is used to Query the indexed files in Solr and obtain the results

$python getResult.py <query string>

Whitespace in the URL must be replaced with '%20' and quotes ("") with '%22'

Ex: $python getResult.py '%22Antarctica%20Ocean%22'

-------------------------------
Implemented Algorithm Overview
-------------------------------
There are two algorithms implemented
1. contentBased- We used analyzer, created new fields and used function query to boost fields in order to get relevant results with high precision and good recall.
2. linkBased - We parsed and extracted metadata features and then created a graph with each document being a node and weighted edges between them for common features. Pagerank was used to score the document which acted as an additional solr cell.

---------------------
D3 extra credit
---------------------
We used the constructed graph to create a json object of clusters of nodes (indexed docs) that had similar score and weighted edges over features extracted.
The script createJSON.py creates the required JSON object that can be visualized using Force-Directed Graph (or Curved Links Force-Directed Graph) in D3 or using builtin python API to visualize this cluster graph.

We have included the image of the graph that was generated using the builtin python API.