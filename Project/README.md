# Location of license dogs in NYC

## Team members
Scott Smith, solo project

## Objective
Identify potential areas where people might be interested in buying goods (chew toys) and services (dog walking)
for their pet dogs.

## Data sets
#### Geography at four levels
* Borough
* Community District
* Neighborhood Tabulation Area
* Tract
#### Nongeographic data
* NYC Dog Licenses
All data come from NYC Open Data

## Data manipulations required
* Removing records for dogs licenced that do not have NYC locations
* Making the delimiter the license data file consistent across all records
* Making tract identification in license data file consistent with the tract map layer
* Aggregating the number of records across each geographic level
* Simplifying the geography as needed to reduce the size for serving

## Visualizations
Choropleth map of selected geographic layers showing number of dogs licensed in each geography

## Interaction
#### As fully implemented
* Select whether to show number of dogs by borough, community district, or neighborhood
* For other than borough, select one of the boroughs or the full city
* If a borough is selected, select either full borough or one of the districts/neighborhoods
* If a neighborhood or district is selected, whether or not to show tract level data

#### Initially
* Set the level as neighborhood and the borough of Manhattan
* Select either all of Manhattan or one Manhattan neighborhood
* Possibly implement tracts option
