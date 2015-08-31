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

  curl"http://localhost:8983/solr/update/extract?literal.id=doc1&uprefix=attr_&fmap.content
  =attr_content&commit=true" -F "myfile=@filename.ext"

###Indexing process for Nutch/Tika + SolrIndexing:
To integrate Nutch/Tika and with Solr we need to make the following changes before
indexing:
● Add the following fields to schema.xml of solr (by matching them to schema.xml
of nutch-trunk):
<field name="digest" type="string" stored="true" indexed="true"/>
<field name="boost" type="float" stored="true" indexed="true"/>
<field name="segment" type="string" stored="true" indexed="true"/>
<field name="host" type="string" stored="true" indexed="true"/>
<field name="tstamp" type="date" stored="true" indexed="true"/>
<field name="anchor" type="string" stored="true" indexed="true"
multiValued="true"/>
<field name="content" type="text_general" indexed="true" stored="true"
multiValued="true"/>
<field name="exactMatch" type="text_exact_match" indexed="true" stored="true"
multiValued="true"/>
<copyField source="content" dest="exactMatch"/>
<fieldType name="text_exact_match" class="solr.TextField"
positionIncrementGap="100">
<analyzer type="index">
<charFilter class="solr.HTMLStripCharFilterFactory"/>
<tokenizer class="solr.StandardTokenizerFactory"/>
<!--<tokenizer class="solr.WhitespaceTokenizerFactory"/>
<filter class="solr.ShingleFilterFactory" minShingleSize="3"
maxShingleSize="3"/>-->
</analyzer>
<analyzer type="query">
<charFilter class="solr.HTMLStripCharFilterFactory"/>
<tokenizer class="solr.StandardTokenizerFactory"/>
<!--<tokenizer class="solr.WhitespaceTokenizerFactory"/>
<filter class="solr.ShingleFilterFactory" minShingleSize="3"
maxShingleSize="3"/>-->
</analyzer>
</fieldType>
● For field Type = “text_general” add the following line to analyzer type=”index” and
type =”query”:
<filter class="solr.PorterStemFilterFactory"/> to enable stemming.
<charFilter class="solr.HTMLStripCharFilterFactory"/> to strip html from
content
● Change the unique key from id to url:
<uniqueKey>url</uniqueKey> change the unique key to url.
● Make the following changes to solrconfig.conf
<p></p>
<p><requestHandler name="/nutch" class="solr.SearchHandler" >
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
Then use the following command line to index the crawled data to solr:
bin/nutch solrindex http://127.0.0.1:8983/solr/ folder/crawldb -linkdb folder/linkdb
folder/segments
