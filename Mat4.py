#!/usr/bin/env python
# coding: utf-8

# In[29]:


import requests, json


# In[30]:


destinations=open('dests.txt', 'r', encoding='utf-8').read().split('\n')
myKey="place api key here- from txt"
origin='תל אביב'
info_all=dict()


# In[40]:


for dest in destinations:
 ###distance and time###
    url_distancesMatrix= "https://maps.googleapis.com/maps/api/distancematrix/json?origins=%s&destinations=%s&key=%s" % (origin,dest,myKey)
    distanceMatrix= requests.get(url_distancesMatrix)
    ##check for problems
    try:
        if not distanceMatrix.status_code==200:
            print("Error")
        else:
            try:
                distanceMatrix= requests.get(url_distancesMatrix).json()
            except:
                print("Not valid")

        
        ##find distance
        distanceValue= distanceMatrix['rows'][0]['elements'][0]['distance']['text']
    
        ##find drive time
        driveValue= distanceMatrix['rows'][0]['elements'][0]['duration']['value']
        #change to hours and minutes
        hours=int(driveValue/3600)
        minutes=int((driveValue/3600-hours)*60)
        str1= ""
        str2= ""
        if hours==1:
            str1=' hour '
        else: str1=" hours "
        if minutes==1:
            str2= " minute"
        else: str2=" minutes"
        edit_driveValue=(str(hours)+str1+str(minutes)+str2) 
     
        
  ###longitude and latitude  
        url_geocode= "https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s" % (dest,myKey)
    ##check for problems:
        response=requests.get(url_geocode)
        if not response.status_code==200:
            print("Error")
            
        else:
            try:
                response_data= requests.get(url_geocode).json()
            except:
                print("Not valid")
                

    
        ##find lat and lng
        edit_response=response_data["results"][0]["geometry"]["location"]
        lng=edit_response["lng"]
        lat=edit_response["lat"]
    
        ##create dictionary
        info_all[dest]=(distanceValue, edit_driveValue, lng, lat)

        
        print("The distination is: "+ dest)
        print("The distance from Tel-Aviv is: "+distanceValue)
        print("The driving time is: "+edit_driveValue)
        print("The longitude is: "+str(lng))
        print("The latitude is: "+str(lat))
        print("_")
    
    except:
        print("This destination is not valid")
        print("_")
        
        


# In[45]:


from operator import itemgetter
farthest=(sorted(info_all.items(), key= itemgetter(1), reverse=True))
print("The farthest cities from Tel-Aviv are: ", farthest[0][0], ", ",farthest[1][0], ", ",farthest[2][0] )


# In[ ]:




