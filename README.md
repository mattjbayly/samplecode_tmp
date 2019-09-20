Python and R Sample Tools for ArcGIS
==============

Requirements
------------

 - [ArcGIS R bridge](https://github.com/R-ArcGIS/r-bridge-install) - Simple (<5 mins)
 - [R Statistical Computing Software](http://www.r-project.org)

### Overview

The following scripts are intended to show several simplified examples of selected codeing standards and examples of Python and R scripts being sourced as ESRI Toolboxes. These scripts may be run with the attached datasets, although Several other Python scripts are included as additional examples of stand alone scripts. These standalone Python scripts can be run by updating directories to point to provincial datasets (too big to store within a Github repository). 

### ESRI Toolboxes Build From R functionality.

Two example R toolboxes are provided as proof of concept showing how R can be integrated into complex data processing workflows in ArcGIS without users have knowledge of the R programming language. For these tools to function properly please enrue the [ArcGIS R bridge](https://github.com/R-ArcGIS/r-bridge-install) is installed.

In the first example a tool called 'BCFWA Streamline USDS' is provided to show how custom R functionlaity can be used to leverage networking capabilites of the BCFWA. By selecting target stream reaches users can identify all upstream and downstream streamline segments.

![](https://github.com/mattjbayly/samplecode_tmp/blob/master/img/samplenetwork.JPG)

In the second example a tool called 'BCFWA Stream Profile' is provided to show how custom R functionlaity can be used to develop dynamic displays and plot outputs (either in the processing window or exported as map PDFs/JPEGs). This example shows a vertical profile for a target stream section by extracting the Z dimension of the geometry.

![](https://github.com/mattjbayly/samplecode_tmp/blob/master/img/streamprofile.JPG)

### ESRI Toolboxes Build From Python functionality.

The final example is a typical simple Python toolbox. This function provides a summary table showing the total length of streams (by stream order) within a given distance from roads. 

![](https://github.com/mattjbayly/samplecode_tmp/blob/master/img/streamordersum.JPG)



