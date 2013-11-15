class BestPlace(object):

    def __init__(self, location):
        self.location = location




    def getYelpCatgry(self):
        """
           Since we only need results from a few categories
           We read the required categories from the web, 
           the list of subcategories is very big, so we need that instead of main categories
        """
        import bs4
        import urllib2


        # This is the list of main categories of YELP we want the sub categories for
        catArrYelp = [ 'active', 'arts', 'food', 'localflavor', 'nightlife', 'restaurants', 'shopping' ]
         # the final array of YELP subcategories we need...
        yelpCatgryArr = []


        # html file to donwload contents from
        htmlDoc = 'http://www.yelp.com/developers/documentation/category_list'
        # Parse the html document
        req = urllib2.urlopen(htmlDoc)
        #parse the document
        soup = bs4.BeautifulSoup(req)

        # the list of categories are defined in a class called "attr-list"
        sec =  soup.find('ul', attrs={'class': 'attr-list'})
        
        # They are listed in a nested list format and we'll retreive them
        sib1 = sec.findNext('ul')
        # before we make changes to sib1 lets get the list of siblings
        siblingList = sib1.find_next_siblings()

        # now sib1 is not very important so keep changing the variable
        sib1 = sib1.findAll('li')

        # All the stuff below is to populate the yelpCatgryArr..
        sib2 = sec.findNext('li').text
        sib2 = sib2.rstrip(')').rsplit('(')
        sib2 = sib2[1]
        if sib2 in catArrYelp :
            for s in sib1:
                currText = s.text
                currText = currText.rstrip(')').rsplit('(')
                #currText = currText[1]
                if ')' in currText :
                    continue
                if '(' in currText :
                    continue
                yelpCatgryArr.append( currText )

        # do the same for the rest of the siblings
           
        for countItem in range( len( siblingList ) ) :
            item = siblingList[countItem]
            if countItem % 2 == 0 :
                itemText = item.text
                itemText = itemText.rstrip(')').rsplit('(')
                itemText = itemText[1]
                if itemText in catArrYelp :
                    if countItem+1 > len(siblingList) :
                        print 'something wrong with the format, check the yelp page'
                        break
                    else :
                        slText = siblingList[countItem+1].findAll('li')
                        for ss2 in slText :
                            currText = ss2.text
                            currText = currText.rstrip(')').rsplit('(')
                            currText = currText[1]
                            if ')' in currText :
                                continue
                            if '(' in currText :
                                continue
                            yelpCatgryArr.append( currText )

        return yelpCatgryArr


    def yelpOut(self, searchType='quicker' ) :

        import oauth2
        import yelpclient
        
        # Access keys to the YELP API...secret!
        yelp_keys = {}

        yelp_keys['consumer_key'] = "8wEGelq9yzY1OSVp13Aybg"
        yelp_keys['consumer_secret'] = "3NAAYIkaQX4hvlgSdn676RuRXIU"
        yelp_keys['token'] = "gf-0vX2OcEpwp1SyiWENIRBJEa2xyT1l"
        yelp_keys['token_secret'] = "LScXVw5uFd7wNgwux0T9zwYYWpg"


        # connect with the keys
        client = yelpclient.YelpClient(yelp_keys)

        # for this app we only need these categories
        termArrYelp = self.getYelpCatgry()#[ 'nightlife', 'Arts & Entertainment', 'Restaurants', 'Shopping' ]
        
        nameArrYelp = []
        ratArrYelp = []
        revCntArrYelp = []
        snptTextArrYelp = []


        #we limit the search to with in 10 miles of loc (16000 meters)
        result_json = client.search_by_location(
            location = self.location, limit = 20, radius=16000,
            )
        # Now loop through the json to get name, ratings, reviews from the location
        # pass the turn if we get an error returned from YELP
        # this is the faster option....but sometimes might not give very few.. locations.
        if searchType == 'quicker' :
            if 'error' not in result_json :
                if 'businesses' in result_json :
                    for ly1 in range( len( result_json['businesses'] ) ) :
                        if 'categories' not in result_json['businesses'][ly1] :
                            continue
                        for c1 in result_json['businesses'][ly1]['categories'] :
                            # check the categories in the selected businness and if it is of interest to us
                            # then use if or else discard
                            for llc in range( len( c1 ) ):
                                if c1[llc] in termArrYelp :
                                    if result_json['businesses'][ly1]['name'] not in nameArrYelp :
                                        nameArrYelp.append( result_json['businesses'][ly1]['name'] )
                                        ratArrYelp.append( result_json['businesses'][ly1]['rating'] )
                                        revCntArrYelp.append( result_json['businesses'][ly1]['review_count'] )
                                        snptTextArrYelp.append( result_json['businesses'][ly1]['snippet_text'] )
                                        print 'YELP-Loc', result_json['businesses'][ly1]['location']['display_address']
                                        break                  
                        
        # there is a slower method which would produce more results 
        # leave this option to choice
        else :
            for tt in range( len( termArrYelp) )  :
                if tt % 3 == 0 :
                    trm = termArrYelp[tt:tt+3]
                    # Get the results from the given location, 
                    #we limit the search to with in 10 miles of loc (16000 meters)
                    result_json = client.search_by_location(
                        location = self.location, limit = 20, term = trm, radius=16000,
                        )
                    # Now loop through the json to get name, ratings, reviews from the location
                    # pass the turn if we get an error returned from YELP
                    if 'error' in result_json :
                        continue
                        
                    for ly1 in range( len( result_json['businesses'] ) ) :
                        if result_json['businesses'][ly1]['name'] not in nameArrYelp :
                            nameArrYelp.append( result_json['businesses'][ly1]['name'] )
                            ratArrYelp.append( result_json['businesses'][ly1]['rating'] )
                            revCntArrYelp.append( result_json['businesses'][ly1]['review_count'] )
                            snptTextArrYelp.append( result_json['businesses'][ly1]['snippet_text'] )
                            # print result_json['businesses'][ly1]['snippet_text']#nameArrYelp[-1], ratArrYelp[-1], revCntArrYelp[-1]            

       
        self.gLatRegion = result_json['region']['center']['latitude']
        self.gLonRegion = result_json['region']['center']['longitude']

        return nameArrYelp, ratArrYelp, revCntArrYelp, snptTextArrYelp


    def yelpBusiness(self, term ) :
        # get YELP data for individual business

        import oauth2
        import yelpclient
        import difflib
        
        # Access keys to the YELP API...secret!
        yelp_keys = {}

        yelp_keys['consumer_key'] = "8wEGelq9yzY1OSVp13Aybg"
        yelp_keys['consumer_secret'] = "3NAAYIkaQX4hvlgSdn676RuRXIU"
        yelp_keys['token'] = "gf-0vX2OcEpwp1SyiWENIRBJEa2xyT1l"
        yelp_keys['token_secret'] = "LScXVw5uFd7wNgwux0T9zwYYWpg"


        # connect with the keys
        client = yelpclient.YelpClient(yelp_keys)

        # for this app we only need these categories
        termFull = term + ', ' + self.location

        #we limit the search to with in 10 miles of loc (16000 meters)
        result_json = client.search_by_location(
            location = self.location, term=termFull,
            )

        # print term
        print '-----------------------------------------------'
        nameBussYELP = None
        ratBussYELP = None
        revCntBussYELP = None
        snptTextBussYELP = None
        if 'businesses' in result_json :
            if result_json['total'] > 0 :
                for i in range( len(result_json['businesses']) ) :
                    seqAll = difflib.SequenceMatcher(a=result_json['businesses'][i]['name'].lower(), b=term.lower())
                    if seqAll.ratio() > 0.8 :
                        nameBussYELP = result_json['businesses'][i]['name']
                        ratBussYELP = result_json['businesses'][i]['rating']
                        revCntBussYELP = result_json['businesses'][i]['review_count']
                        snptTextBussYELP = result_json['businesses'][i]['snippet_text']
                        print i, seqAll.ratio(), term, result_json['businesses'][i]['name']
                # print result_json['total'], result_json['businesses'][0]['name'], result_json['businesses'][0]['rating'], result_json['businesses'][0]['review_count']
            

        return nameBussYELP, ratBussYELP, revCntBussYELP, snptTextBussYELP

    def foursquareOut(self, latitude=None, longitude=None):

        # remember to call this function after calling yelpOut...
        # designed that way and works better that way as well.

        import oauth2
        import foursquare


        # The client object
        client = foursquare.Foursquare(client_id='VAFCCZPNQHVBI53GVJTBPIWXA55IOU4L32ENLK332IJ0LGJU', \
            client_secret='325EG5SUUUQJTULJ13HP33BV4SW5DGJGNSVJGHAVACHA3ZNQ')

        # Authorization url for the app
        auth_uri = client.oauth.auth_url()

        # Venues near the search latitude.
        # this turned out to be more accurate, so we are now getting the values of lat and lon from YELP

        if latitude == None or longitude == None :
            latlonVal = str(self.gLatRegion) + ',' + str(self.gLonRegion)
        else :
            latlonVal = str(latitude) + ',' + str(longitude)

        # Get the list of venues near the location
        allVenues = client.venues.explore( params={'ll': latlonVal} )

        # Get the data from allVenues JSON
        nameArrFSAll = []
        likesArrFSAll = []
        totChkinArrFSAll = []
        userChkinArrFSAll = []
        addressArrFSAll = []

        
        for lfs1 in range( len( allVenues['groups'][0]['items'] ) ) :
            if allVenues['groups'][0]['items'][lfs1]['venue']['name'] == 'Foursquare HQ' :
                continue

            nameArrFSAll.append( allVenues['groups'][0]['items'][lfs1]['venue']['name'] )
            likesArrFSAll.append( allVenues['groups'][0]['items'][lfs1]['venue']['likes']['count'] )
            totChkinArrFSAll.append( allVenues['groups'][0]['items'][lfs1]['venue']['stats']['checkinsCount'] )
            userChkinArrFSAll.append( allVenues['groups'][0]['items'][lfs1]['venue']['stats']['usersCount'] )

            if ( 'address' in allVenues['groups'][0]['items'][lfs1]['venue']['location'] ) :

                addText = allVenues['groups'][0]['items'][lfs1]['venue']['location']['address'] + ' ,'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['city'] + ' ,'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['state']+ '-'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['postalCode']
            else :

                addText = nameArrFSAll[-1] + ' ,'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['city'] + ' ,'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['state']+ '-'+ \
                            allVenues['groups'][0]['items'][lfs1]['venue']['location']['postalCode']

            addressArrFSAll.append( addText )

            

        # Get the list of trending venues near the location
        trndVenues = client.venues.trending( params={'ll': latlonVal} )

        # Get the data from allVenues JSON
        nameArrFSTrnd = []
        totChkinArrFSTrnd = []
        userChkinArrFSTrnd = []
        hereNowCntArrFSTrnd = []
        addressArrFSTrnd = []
        
        for lfs2 in range( len( trndVenues['venues'] ) ) :
            # We'll skip the FS headquarter in NY, Not really necessary
            if trndVenues['venues'][lfs2]['name'] == 'Foursquare HQ' :
                continue
            nameArrFSTrnd.append( trndVenues['venues'][lfs2]['name'] )
            totChkinArrFSTrnd.append( trndVenues['venues'][lfs2]['stats']['checkinsCount'] )
            userChkinArrFSTrnd.append( trndVenues['venues'][lfs2]['stats']['usersCount'] )
            hereNowCntArrFSTrnd.append( trndVenues['venues'][lfs2]['hereNow']['count'] )
            # print 'FSTRD', nameArrFSTrnd[-1], totChkinArrFSTrnd[-1], userChkinArrFSTrnd[-1], hereNowCntArrFSTrnd[-1]
            # print trndVenues['venues'][lfs2].keys()

            if ( 'address' in trndVenues['venues'][lfs2]['location'] ) :

                addText = trndVenues['venues'][lfs2]['location']['address'] + ' ,'+ \
                            trndVenues['venues'][lfs2]['location']['city'] + ' ,'+ \
                            trndVenues['venues'][lfs2]['location']['state']+ '-'+ \
                            trndVenues['venues'][lfs2]['location']['postalCode']
            elif ( 'city' not in trndVenues['venues'][lfs2]['location'] ) :
                addText = nameArrFSTrnd[-1] + ' ,'+ \
                            trndVenues['venues'][lfs2]['location']['state']

            elif ( 'address' not in trndVenues['venues'][lfs2]['location'] ) :
                addText = nameArrFSTrnd[-1] + ' ,'+ \
                            trndVenues['venues'][lfs2]['location']['city'] + ' ,'+ \
                            trndVenues['venues'][lfs2]['location']['state']+ '-'+ \
                            trndVenues['venues'][lfs2]['location']['postalCode']
            
            addressArrFSTrnd.append( addText )


        return nameArrFSAll, likesArrFSAll, totChkinArrFSAll, userChkinArrFSAll, addressArrFSAll, \
         nameArrFSTrnd, totChkinArrFSTrnd, userChkinArrFSTrnd, hereNowCntArrFSTrnd, addressArrFSTrnd


    def mergeLocs(self, searchType='quicker'):

        import difflib
        import numpy
        import pandas


        ### '-------------------------YELP Data Analysis---------------------------------'
        ### '-------------------------YELP Data Analysis---------------------------------'
        ### '-------------------------YELP Data Analysis---------------------------------'

        # get data from YELP
        ( nameArrYelp, ratArrYelp, revCntArrYelp, snptTextArrYelp ) = self.yelpOut( searchType=searchType )
        # get data from FS
        (nameArrFSAll, likesArrFSAll, totChkinArrFSAll, userChkinArrFSAll, addressArrFSAll, nameArrFSTrnd, totChkinArrFSTrnd,\
         userChkinArrFSTrnd, hereNowCntArrFSTrnd, addressArrFSTrnd ) = self.foursquareOut()
        
        # Convert each of these arrays into Numpy arrays
        # The YELP arrays
        nameArrYelp = numpy.array( nameArrYelp )
        ratArrYelp = numpy.array( ratArrYelp )
        revCntArrYelp = numpy.array( revCntArrYelp )
        snptTextArrYelp = numpy.array( snptTextArrYelp )
        # The FS arrays
        # Historic data from FS
        nameArrFSAll = numpy.array( nameArrFSAll )
        likesArrFSAll = numpy.array( likesArrFSAll )
        totChkinArrFSAll = numpy.array( totChkinArrFSAll )
        userChkinArrFSAll = numpy.array( userChkinArrFSAll )
        # Trending Locs from FS
        nameArrFSTrnd = numpy.array( nameArrFSTrnd )
        totChkinArrFSTrnd = numpy.array( totChkinArrFSTrnd )
        userChkinArrFSTrnd = numpy.array( userChkinArrFSTrnd )
        hereNowCntArrFSTrnd = numpy.array( hereNowCntArrFSTrnd )

        
        # # This part below is for finding the ratings in YELP for the results found only in FS
        # # Commented out currently but could be used for later purposes
        # for lfs2 in range( len( nameArrFSAll ) ) :
        #     nameCurrAllFS = nameArrFSAll[lfs2]
        #     currNamePresent = False
        #     for ly1 in range( len( nameArrYelp ) ) :
        #         nameCurrYelp = nameArrYelp[ly1]
        #         seqAll = difflib.SequenceMatcher(a=nameCurrYelp.lower(), b=nameCurrAllFS.lower())
        #         if seqAll.ratio() >= 0.8 :
        #             # print nameCurrYelp, nameCurrAllFS, 'common Trend Yelp', seqAll.ratio()
        #             currNamePresent = True
        #             break
        #     if not currNamePresent :
        #         # ( nameFSYelp, ratFSYelp, revCntFSYelp, snptTextFSYelp ) = self.yelpBusiness( term=nameCurrAllFS )
        #         termSrch = nameCurrAllFS
        #         termSrch = termSrch.encode( 'ascii', 'ignore' )
        #         (nameBussYELP, ratBussYELP, revCntBussYELP, snptTextBussYELP) = self.yelpBusiness( term=termSrch )






        # we'll get the Bayseian ratings for YELP instead of the average ratings
        # this will let us account for lower number of reviews on one and higher on the other
        meanRevCntYelp = numpy.mean( revCntArrYelp )
        meanRatYelp = 3. # I choose this value since it looked like a reasonable default rating

        baysRatYelp = []

        for y1 in range( len( nameArrYelp ) ) :
            # Also we normalize the rating values to between 0 and 1
            baysRatYelp.append( ( meanRevCntYelp * meanRatYelp + revCntArrYelp[y1] * ratArrYelp[y1] )/( meanRevCntYelp + revCntArrYelp[y1] ) )
        
        # Convert to numpy array and normalize to a scale of 1
        maxbaysRatYelp = max( baysRatYelp )
        baysRatYelp = numpy.array( baysRatYelp/maxbaysRatYelp )
    
        # now convert things into PANDAS DataFrame
        yelpData = pandas.DataFrame( { 'name' : nameArrYelp, 'rating' : baysRatYelp } )
        # sort the dictionary according to our rating
        yelpData = yelpData.sort( ['rating'], ascending=[True] )
        yelpData = yelpData[::-1]
        


        ### '-------------------------FOUR SQUARE (all data) Analysis---------------------------------'
        ### '-------------------------FOUR SQUARE (all data) Analysis---------------------------------'
        ### '-------------------------FOUR SQUARE (all data) Analysis---------------------------------'

        # we now get to the FS stuff
        # First we need to normalize the number of likes. We can make it likes/user, somewhat on the lines of ratings
        lpuFSAll = []
        for l,u in zip( likesArrFSAll, userChkinArrFSAll ):
            lpuFSAll.append( l/float(u) )


        # We need the Bayseian type of likes rather than normal likes in FS
        # we'll get the mean for both num of users and mean likes/user
        meanUsrFSAll = numpy.mean( userChkinArrFSAll )
        meanLpuFSAll = numpy.mean( lpuFSAll )

        baysLikesFS = []

        for f1 in range( len( nameArrFSAll ) ) :
            baysLikesFS.append( ( meanUsrFSAll * meanLpuFSAll + lpuFSAll[f1]*userChkinArrFSAll[f1] ) / ( meanUsrFSAll + userChkinArrFSAll[f1] ) )
            # print nameArrFSAll[f1], likesArrFSAll[f1], lpuFSAll[f1], baysLikesFS[-1], userChkinArrFSAll[f1], meanUsrFSAll, meanLpuFSAll

        # Convert to numpy array
        lpuFSAll = numpy.array( baysLikesFS )          
        #convert to numpy array and also normalize to a scale of 1
        maxLpuVal = max( lpuFSAll )
        lpuFSAll = numpy.array( lpuFSAll/maxLpuVal )
        minLpuVal = numpy.min(lpuFSAll[numpy.nonzero(lpuFSAll)])
        
        ratFSAll = []
        typeDatFSALL = []
        for u,t,lu in zip( userChkinArrFSAll, totChkinArrFSAll, lpuFSAll ):
            if lu > 0. :
                ratFSAll.append( t*lu/float(u) )
            else :
                ratFSAll.append( t*minLpuVal/float(u) )

        # Convert into a numpy array and normalize to 1
        maxRatFSAll = max( ratFSAll )
        ratFSAll = numpy.array( ratFSAll/maxRatFSAll )


        # now convert things into PANDAS DataFrame
        fsAllData = pandas.DataFrame( { 'name' : nameArrFSAll, 'rating' : ratFSAll } )
        # sort the dictionary according to our rating
        fsAllData = fsAllData.sort( ['rating'], ascending=[True] )
        fsAllData = fsAllData[::-1]
        


        # Combine the data from YELP and Four Square (all data)
        combinedData = pandas.concat( [ yelpData, fsAllData ] )
        combinedData = combinedData.sort( ['rating'], ascending=[True] )
        combinedData = combinedData[::-1]
        # we only need the top 15 locations
        if len(combinedData.index) > 15 :
            combinedData = combinedData[:15]
        
        
        ### '-------------------------FOUR SQUARE (Trending locations) Analysis---------------------------------'
        ### '-------------------------FOUR SQUARE (Trending locations) Analysis---------------------------------'
        ### '-------------------------FOUR SQUARE (Trending locations) Analysis---------------------------------'
        if len(hereNowCntArrFSTrnd) > 0 :
            # if there are any trending locations
            maxHereNowFSTrnd = max( hereNowCntArrFSTrnd )
            ratFSTRND = []
            for hn in hereNowCntArrFSTrnd :
                ratFSTRND.append( hn*1./maxHereNowFSTrnd )

            ratFSTRND = numpy.array( ratFSTRND )

            # now convert things into PANDAS DataFrame
            fsTRNDData = pandas.DataFrame( { 'name' : nameArrFSTrnd, 'rating' : ratFSTRND } )
            # sort the dictionary according to our rating
            fsTRNDData = fsTRNDData.sort( ['rating'], ascending=[True] )
            fsTRNDData = fsTRNDData[::-1]

            # Combine the FSTRND data with our original combined data
            if len( fsTRNDData.index ) > 5 :
                combinedData = pandas.concat( [ fsTRNDData[:5], combinedData ] )
            else :
                combinedData = pandas.concat( [ fsTRNDData, combinedData ] )

        print combinedData
        



def testCode(place='new york, ny', search='quicker' ):

     po = BestPlace(place) 
     yelpDict = po.mergeLocs( searchType=search )