#Building an Apache-Solr based Search Engine and Ranking Algorithms for NSF and NASA Polar Datasets

##Description of session with Dr. Burgess
The objective of the hangout session was to discuss about how to come with science questions for the polar dataset. 
Dr. Burgess emphasized on the importance of sciencekeywords. She said the keywords would help us frame queries for 
the science questions we come up with. As we know, the data accumulated over projects and expeditions by polar scientists is hosted on the sites we crawled. Along with this data uploaded, thereis metadata associated. From this metadata we can find keywords to use in our queries. We were suggested to look into properties or fields such as description, attributes which
mention science keywords and spatial keywords. We talked about the geographic regions which encompass the polar regions and its importance. The spatial metadata provides bounding coordinates that cover the region from where the data was recorded.
She mentioned a data set which contains information accumulated from the entire world, hence it contains information about the polar regions as well. But it would be better to ignore that kind of data and consider the data set closer to the region we are
looking at. We extensively discussed of how the arctic conditions is associated with issues around the world such as oil, natural resources, global warming, rising sea levels and national security. So, the question should be formed such that we can cover different topics which are directly or indirectly affected by polar data.

##Constructing Scientific Questions
First we browsed through all the sites i.e. AMD, NSIDC and ACADIS. In the home directory we saw a classification of topics. We browsed through them and read some project descriptions. Then came up with a few general topics such as global warming,
to base our queries on. We searched the website for these topics. We read a couple of project abstracts and found a common phenomenon, event or global concern they covered. Then we looked for a geographic region where multiple projects of the sort
were done. Taking all of this into account we designed our science questions. Using the search facility provided on the websites we searched for articles related to our question. This helped us judge the correctness of our search results. We observed the pattern in which the description was written. For example, AMD has title of project, abstract,
graphical coverage, spatial coordinates, temporal coverage, location keywords, science keywords, ISO topic category and other useful information. This helped us determine how we could go about designing our algorithms.

##Scientific questions
1. What has been observed about the trend in change of ice thickness in Antarctica region from 2002 to 2014?
2. How has global warming impacted water temperature of warm pools in the Indo-Pacific ocean?
3. What is the trend zooplankton grazing rate in the North Pacific Ocean region?
4. How has ozone depletion caused UV-induced changes impacting the marine life and cryosphere in the antarctic region?
5. What is the impact on glacier hydrology due to Greenland ice sheet melting?

##Nutch/Tika + SolrIndexing Vs SolrCell
Indexing process for SolrIndexing:
● First we dump our crawl data and get all the documents, images, audios etc crawled.
● Then we used a python script to iterate over all the data and index it in Solr using the curl command: 

    curl"http://localhost:8983/solr/update/extract?literal.id=doc1&uprefix=attr_&fmap.content=
    attr_content&commit=true" -F "myfile=@filename.ext"

###Indexing process for Nutch/Tika + SolrIndexing:
To integrate Nutch/Tika and with Solr we need to make the following changes before indexing:
● Add the following fields to schema.xml of solr (by matching them to schema.xml of nutch-trunk):

    <field name="digest" type="string" stored="true" indexed="true"/>
    <field name="boost" type="float" stored="true" indexed="true"/>
    <field name="segment" type="string" stored="true" indexed="true"/>
    <field name="host" type="string" stored="true" indexed="true"/>
    <field name="tstamp" type="date" stored="true" indexed="true"/>
    <field name="anchor" type="string" stored="true" indexed="true" multiValued="true"/>
    <field name="content" type="text_general" indexed="true" stored="true" multiValued="true"/>
    <field name="exactMatch" type="text_exact_match" indexed="true" stored="true" multiValued="true"/>
    <copyField source="content" dest="exactMatch"/>
    <fieldType name="text_exact_match" class="solr.TextField" positionIncrementGap="100">
        <analyzer type="index">
            <charFilter class="solr.HTMLStripCharFilterFactory"/>
            <tokenizer class="solr.StandardTokenizerFactory"/>
            <!--<tokenizer class="solr.WhitespaceTokenizerFactory"/>
            <filter class="solr.ShingleFilterFactory" minShingleSize="3" maxShingleSize="3"/>-->
        </analyzer>
        <analyzer type="query">
            <charFilter class="solr.HTMLStripCharFilterFactory"/>
            <tokenizer class="solr.StandardTokenizerFactory"/>
            <!--<tokenizer class="solr.WhitespaceTokenizerFactory"/>
            <filter class="solr.ShingleFilterFactory" minShingleSize="3" maxShingleSize="3"/>-->
        </analyzer>
    </fieldType>
    
● For field Type = “text_general” add the following line to analyzer type=”index” and type =”query”:

    <filter class="solr.PorterStemFilterFactory"/> to enable stemming.
    <charFilter class="solr.HTMLStripCharFilterFactory"/> to strip html from content
    
● Change the unique key from id to url:

    <uniqueKey>url</uniqueKey> change the unique key to url.
    
● Make the following changes to solrconfig.conf:

    <p></p>
    <p>
        <requestHandler name="/nutch" class="solr.SearchHandler" >
            <lst name="defaults">
                <str name="defType">dismax</str>
                <str name="echoParams">explicit</str>
                <float name="tie">0.01</float>
                <str name="qf">
                    content^0.5 anchor^1.0 title^1.2
                </str>
                <str name="pf">
                    content^0.5 anchor^1.5 title^1.2 site^1.5
                </str>
                <str name="fl">
                    url
                </str>
                <str name="mm">
                    2&lt;-1 5&lt;-2 6<90%
                </str>
                <int name="ps">100</int>
                <bool name="hl">true</bool>
                <str name="q.alt">*:*</str>
                <str name="hl.fl">title url content</str>
                <str name="f.title.hl.fragsize">0</str>
                <str name="f.title.hl.alternateField">title</str>
                <str name="f.url.hl.fragsize">0</str>
                <str name="f.url.hl.alternateField">url</str>
                <str name="f.content.hl.fragmenter">regex</str>
            </lst>
        </requestHandler>
    </p>
    
● Then use the following command line to index the crawled data to solr:

    bin/nutch solrindex http://127.0.0.1:8983/solr/ folder/crawldb -linkdb folder/linkdb folder/segments

##What was easier – Nutch/Tika + SolrIndexing or SolrCell? What did Tika extract in Nutch compared to what SolrCell extracts?
Solrcell indexing is easier compared to Nutch+tika SolrCell. Tika extracts metadata such as: title, subject, author, keywords, comment, template, lasr_saved, revision_number, last_printed, last_saved, page_count, word_count, character_count, application_name. With SolrCell we have a wide range of metadata that we can extract before indexing. The fields specified in the schema.xml of solr can be used to specify all the features we want. We can add fields by specify the name and setting the values of indexed and stored to “true”.

    <field name="metatag.description" type="text" stored="true" indexed="true"/>
    <field name="metatag.keywords" type="text" stored="true" indexed="true"/>
    Eg. <field name="north" type="text" stored="true" indexed="true"/>
    <field name="south" type="text" stored="true" indexed="true"/>

##Content Based Algorithm
The content based algorithm is implemented using TFIDF. Given a query, we determine the key terms to be used for the calculation of the TFIDF score of the document. We utilize the TFIDF functionality of solr to rank the documents. But by default solr gives equal weight to all the keywords to calculate the score and uses all the fields. Instead,
we use function query to construct a more effective query. Through it we can specify which fields should be considered and how much it should contribute to the calculation of the score. We have included during solr indexing additional fields such as start date, end date, east, west, north, south coordinates, description, title, exact match and a couple more. Using these fields we design our function query depending on our science question. For example, q=title:<antarctic>^2 content:<ice> startyear:[2000 TO 2010]^2 is a function query in which we give more importance to the title and startyear by boosting it’s weight. Here we are looking for documents which contain the term ‘antarctic’ in its title, has content related to ‘ice’ and has been recorded between 2000 and 2010. We are using a script to determine the function query based on our science
question. To make sure that we get effective results we have done the following: stemming, removing stopwords and html stripping.

For our science question 5, We got the following results:

    Question - What is the impact on glacier hydrology due to Greenland ice sheet melting?
    Query string - http://localhost:8983/solr/select?q=content:%22glacier%20hydrology%22%20AND%20greenland%20&limit=-1
    Total results - 14
    Filenames of top 10 results -
    􀀀 GrIS_radon_data.html
    􀀀 GrIS_RADON.html
    􀀀 radon222.html
    􀀀 rapid_impact_of_large_scale_greenland_ice_sheet_melting_on_glacier_hydrology_and_meltwater_geochemistry.html
    􀀀 Greenland_meltwater_microbial_diversity_and_abundance.html
    􀀀 Solid%20Earth.html
    􀀀 GrIS_radon_data.txt
    􀀀 GrIS_RADON.txt
    􀀀 radon222.txt
    􀀀 radon222.iso19139

##Link Based Algorithm
The link based algorithm is designed such that we can find relevancy between documents based on the associated features of the document. The first step is to figure out the features to be used. To do so we extract spatial coordinates, temporal coverage, location keywords, science keywords, ISO topic category and ancillary keywords from all the documents. We have written a python code for extracting most of the features and modified CLAVIN to extract cartographic features. We then construct a graph which represents the documents as nodes and the an edge represents a common feature between two documents. So we get a multi graph as the result. To convert it to a single graph we convert n edges between two documents A and B into a single edge of weight n. Then this graph is fed into the pagerank algorithm. This is done using an API called networkx. We obtain the pagerank scores of the documents and index them into solr. For this purpose we augment the documents with the pagerank score as a new field.

For our science question 5, We got the following results:

    Question - What is the impact on glacier hydrology due to Greenland ice sheet melting?
    Query string - http://localhost:8983/solr/select?q=content:%22glacier%20hydrology%22%20AND%20greenland%20&limit=-1
    Total results - 30
    Filenames of top 10 results -
    􀀀 GrIS_radon_data.html
    􀀀 Titles.do?Portal=GCMD&KeywordPath=Locations%7COCEAN%7CPACIFIC+OCEAN%7CEASTERN+PACIFIC+OCEAN&MetadataType=0&Offset=50&l      bnode=mdlb4
    􀀀 radon222.html
    􀀀 rapid_impact_of_large_scale_greenland_ice_sheet_melting_on_glacier_hydrology_and_meltwater_geochemistry.html
    􀀀 Freetext.do?KeywordPath=&Portal=antabif&MetadataType=0&Freetext=DIF%2FIDN_Node%3A+ANTABIF
    􀀀 radon222.txt
    􀀀 GrIS_radon_data.txt
    􀀀 Keywords.do?KeywordPath=%5BParent_DIF%3D%27SCARMarBIN%27%5D&Portal=GCMD&MetadataType=0
    􀀀 Keywords.do?KeywordPath=%5BParameters%3A+Topic%3D%27BIOLOGICAL+CLASSIFICATION%27%2C+Term%3D%27ANIMALS%2FVERTEBRATES%27
     %2C+Variable_Level_1%3D%27FISH%27%2C+Variable_Level_2%3D%27RAYFINNED+FISHES%27%5D&Portal=GCMD&MetadataType=0
    􀀀 Freetext.do?Freetext=DIF%2FProject%3AEBA+&KeywordPath=&Portal=eba&MetadataType=0

##Link-Based Algorithm Vs Content-Based Ranking

###How effective the link-based algorithm was compared to the content-based ranking algorithm in light of the scientific questions?
The scientific questions we have formulated are based on the properties such as ice thickness, global warming, cryosphere, water temperature etc. We have extracted keywords from these properties and performed a query on the documents using solr.
We observed that the link based algorithm was more effective than the content based in certain cases. In the link-based algorithm which is query independent, the documents are clustered based on properties such as the ones mentioned above. The document having the most number of properties which are common with other document has the highest rank. In content-based algorithm the ranking is done using TFIDF and it is solely based on the keywords passed in the queries. Thus there are cases where the documents having the required properties have not appeared in the result because the exact keyword we queried for was not present in its content. Whereas those documents are present in the clusters associated with the property. Hence, link based gave better results than content-based in scenarios where some documents were overlooked due to the absence of keywords in the content.

###What questions were more appropriate for the link based algorithm compared to the content one?
Link based is more appropriate when our query contains the words which are present in the features or are similar to the features used during graph construction. After the page rank is performed over the link graph, we get the scores. The document having the most number of features which are also present in other documents has the highest rank. So
we get a cluster of documents associated with the science keyword. 
For example,
suppose our question is based on the change in the thickness in ice. If ice thickness is a feature then we get better results for it compared to content-based. On the other hand content-based algorithm works better if we have a query which is
very specific. 
For example, 
suppose we want to find results for a project named BIOQUIMICA APLICADA. There is a very low possibility of this term to be a feature in link-base algorithm. Where as we would find very relevant results from content-based algorithm.

##Latent Dirichlet Allocation (LDA)
LDA is an algorithm which automatically finds topics from our crawled data. Every document is expressed as a combination of topics found by LDA. It associates the words in the document with the topics and provides us with a percentage probability of
how much a document is related to the topic. To implement LDA, we used mahout. The input to the algorithm is the extracted content from all the dumped data. To avoid generation of topics which are common words, we preprocessed the content and removed the stop words. Then we converted all the files into a SequenceFile format using ./mahout seqdirectory. This sequence file is taken as an input to produce tf vectors by using ./mahout seq2sparse. The next step is to invoke the LDA algorithm given the tf vectors as input. But in the latest version of mahout, instead of direct lda command we are suggested to use cvb command. In order to run cvb we first converted the text keys in the vectors to integer keys using ./mahout rowid. We then ran the cvb command giving number of topics as the parameter.

A part of the sample output of topics we found are:

    {continent:0.062253240607493175,ocean:0.04631503190274735,africa:0.04034630800499458
    ,europe:0.02856882508125656,asia:0.0279616891416276,america:0.02236880590126792,nort
    h:0.0198336363451713,atlantic:0.019050805417959116,western:0.014697015622096783,pacif
    ic:0.014228033171683179}
    {ice:0.014291374660605682,ocean:0.012150009519871425,aquatic:0.012093652335247325,gl
    acier:0.008230570728051759,arctic:0.008073733950530022,water:0.007911953587256331,pol
    ar:0.007436174136919549,antarctic:0.007410489895308846,marine:0.006902509674294986,t
    emperature:0.006509676211788371}
    
###What differences you see between task 4(the algorithms) and LDA technique results?
If the data is non-structured and we have no domain knowledge then LDA works well. This is because it automatically generates the topics and give us an idea of how much documents are based on these topics. But for our data we observe that the features
generated are not nearly as good as the features being used for link-based algorithm.

##Integrating the relevancy algorithms into Nutch

1. Click on import under the file menu in eclipse.
2. Under the Git category select projects from Git in the pop up and then click on next.
3. Next clone URI and then click on next.
4. Enter the following git repository - https://github.com/apache/nutch.git , in
   the text box for ‘URI’,and then click on next.
5. Select all files in branch selection pop up and click next.
6. Enter the directory where you want the Nutch repository to be stored in the
   local destination pop-up, and click on next.
7. Once all the projects download , select on import as general project option and click on next.
8. Click finish after entering project name.
9. In the package explorer, you should see a project named nutch.
10.Now in nutch -> src -> java ->org ->apache ->nutch->scoring folder, you should see a file 
   named ScoringFilters.java. Here    we should add our link-based algorithm’s code.

##D3 Visualization
We used the constructed graph to create a json object of clusters of nodes(indexed docs) that had similar score and weighted edges over features extracted. The script createJSON.py creates the required JSON object that can be visualized using force-directed graph (or Curved Links Force Directed Graph) in D3 or using built-in python API to visualized this cluster graph.
