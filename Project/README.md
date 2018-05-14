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
* Have geographic level fixed at neighborhood
* Select full city or one of the boroughs
* Select one of the neighborhoods in the selected borough
* Select either all of Manhattan or one Manhattan neighborhood
* Possibly implement tracts option

#### As completed
* Implemented tracts option
* Allow for selection of full city or one borough
* Restricted to units of neighborhoods
* Can select individual neighborhood if a single borough is selected

## Description
Uses geographic marks encoded by color with darker blues indicating
higher numbers of dogs in the unit. Position on a 2-D suface is the
simplest way to convey location and luminance conveys the measured
feature as each location.

An alternative would be to shade on density possibly adding a dot to
indicate total population.

## Outcome
The interface works for select borough, neighborhood and
whether or not to show tracts. 
Finally got clipping to work right. Need to fix shading when
toggling between tracts on and off.
