from app import app
from flask import render_template, request
import locAmuse
import pandas
# Create mappings from the "/" and "/index" urls to this function
@app.route('/')
@app.route('/index')

def index():
    return render_template("start.html",
        title = 'Local Amusements - Search for a Location')

@app.route('/resdisp/<place>')
def resdisp(place):

    # # get the place 
    # place = request.args.get('key')
    
    # set the search type to quicker for now
    search = 'quicker'
    # get the results from the locAmuse function
    resObj = locAmuse.BestPlace(str(place))
    ( cDat, yDat, faDat, ftDat ) = resObj.mergeLocs( searchType=search )


    # Make an array of dicts suggesting places
    #Combined rankings
    CDatDict = []
    for ii in range( len(cDat) ) :
        thisDict = { 'name': cDat[ii][1], 'rank':ii+1, 'address':cDat[ii][0] }
        CDatDict.append( thisDict )

    #YELP rankings
    yDatDict = []
    for ii in range( len(yDat) ) :
        thisDict = { 'name': yDat[ii][1], 'rank':ii+1, 'address':yDat[ii][0] }
        # print yDat[ii]
        yDatDict.append( thisDict )

    #FS All rankings
    faDatDict = []
    for ii in range( len(faDat) ) :
        thisDict = { 'name': faDat[ii][1], 'rank':ii+1, 'address':faDat[ii][0] }
        faDatDict.append( thisDict )

    #FS Trending rankings
    if ftDat[0] != -1 :
        ftDatDict = []
        for ii in range( len(ftDat) ) :
            thisDict = { 'name': ftDat[ii][1], 'rank':ii+1, 'address':ftDat[ii][0] }
            ftDatDict.append( thisDict )
    else :
        ftDatDict = []
        for ii in range( len(cDat) ) :
            thisDict = { 'name': 'No Trending Places Found', 'rank':0, 'address' : place }
            ftDatDict.append( thisDict )
        # ftDatDict = { 'name': 'No Trending Places Found', 'rank':-1 }



    # pass the data to the HTML 
    return render_template("ind.html",
        title = 'Local Amusements', 
        comlocs = CDatDict, ylocs = yDatDict, falocs = faDatDict, ftlocs = ftDatDict,
        locat = place)