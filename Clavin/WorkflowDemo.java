package com.bericotech.clavin;

import java.io.File;
import java.io.PrintWriter;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

import com.bericotech.clavin.resolver.ResolvedLocation;
import com.bericotech.clavin.util.TextUtils;

/*#####################################################################
 * 
 * CLAVIN (Cartographic Location And Vicinity INdexer)
 * ---------------------------------------------------
 * 
 * Copyright (C) 2012-2013 Berico Technologies
 * http://clavin.bericotechnologies.com
 * 
 * ====================================================================
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the License for the specific language governing
 * permissions and limitations under the License.
 * 
 * ====================================================================
 * 
 * WorkflowDemo.java
 * 
 *###################################################################*/

/**
 * Quick example showing how to use CLAVIN's capabilities.
 * 
 */
public class WorkflowDemo {

    /**
     * Run this after installing & configuring CLAVIN to get a sense of
     * how to use it.
     * 
     * @param args              not used
     * @throws Exception
     */
    public static void main(String[] args) throws Exception {
        
        // Instantiate the CLAVIN GeoParser
        GeoParser parser = GeoParserFactory.getDefault("./IndexDirectory");
        String res ="";
        PrintWriter output = new PrintWriter(new File("/home/countries_found.txt"));
        // Unstructured text file about Somalia to be geoparsed
        File folder = new File("/home/data_dir");
        File[] listOfFiles = folder.listFiles();
         int k=0;
        for (int i = 0; i < listOfFiles.length; i++)
	{
        //File inputFile = new File("src/test/resources/sample-docs/Somalia-doc.txt");
		if (listOfFiles[i].isFile())
		{
			Map locations = new HashMap();
			System.out.println("-------------------------- File : " + listOfFiles[i].getName() + " --------------------------\n");
			//File inputFile = new File(listOfFiles[i].getName());
			// Grab the contents of the text file as a String
                          res = i + "," + listOfFiles[i].getName() + ",";
			String inputString = TextUtils.fileToString(listOfFiles[i]);
		
			// Parse location names in the text into geographic entities
			List<ResolvedLocation> resolvedLocations = parser.parse(inputString);
		       
			// Display the ResolvedLocations found for the location names
                        k=0;
			for (ResolvedLocation resolvedLocation : resolvedLocations)
			{
				if(!locations.containsKey(resolvedLocation))
				{
					locations.put(resolvedLocation, true);
                            		if(k==0)
                            		{
				            res += resolvedLocation;
				            k=1;
				        }
				        else
				        {
						res = res+" > " + resolvedLocation;
					}
				}
			    //System.out.println(listOfFiles[i].getName() + " : " + resolvedLocation);
				/*System.out.println(
				String.format("%s (%s, %s)", 
				resolvedLocation.matchedName, 
				resolvedLocation.geoname.latitude, 
				resolvedLocation.geoname.longitude));*/
				//System.out.println(resolvedLocation.get
			}
              
              output.println(res);
		System.out.println(res);
	      }else if (listOfFiles[i].isDirectory()) {
		System.out.println("-------------------------- Directory " + listOfFiles[i].getName() + " --------------------------\n");
	      }        
        }
	System.out.println("-------------------------- DONE --------------------------\n");
	output.close();
    }
}
