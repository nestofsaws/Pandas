from pandas import Series, DataFrame 
import pandas as pd 
from numpy.random import randn 
import numpy as np

### reading in & cleaning data. dropping/renaming columns as necessary ###
artists = pd.read_csv('artists.dat', sep='\t')
artists_df = artists.drop(['url', 'pictureURL'], axis=1)
artists_df.columns = ['aid', 'name']

user_artists_df = pd.read_csv('user_artists.dat', sep='\t')
user_artists_df.columns = ['uid', 'aid', 'weight']

uta = pd.read_csv('user_taggedartists.dat', sep='\t') 
user_tagged_artists_df = uta[uta['year']>=2005]
user_tagged_artists_df.columns = ['uid', 'aid', 'tagID', 'day', 'month', 'year']

### merging dataframes to display artist names ###
a2ua_df = pd.merge(artists_df, user_artists_df, left_on='aid', right_on='aid')
a2uta = pd.merge(artists_df, user_tagged_artists_df, left_on='aid', right_on='aid')


###########Queries##################

### make a group object ###
n1 = a2ua_df.groupby(['aid', 'name'])['weight'].sum().order(ascending=False)[:10]

### turn the object into a new dataframe ###
number_1 = DataFrame(n1.values, index=n1.index) 

### rename the column for print output ###
number_1.columns = ['playcount']
print
print 40 * '!'
print
print "1. Who are the top artists?"
print number_1
#############################

### make a group object ###
n2 = a2ua_df.groupby(['uid'])['weight'].sum().order(ascending=False)[:10]

### turn the object into a new dataframe ###
number_2 = DataFrame(n2.values, index=n2.index) 
number_2.columns = ['playcount']
print
print 40 * '!'
print
print "2. Who are the top users?"
print number_2
########################

### make a group object ###
n3 = a2ua_df.groupby(['aid', 'name'])['uid'].count().order(ascending=False)[:10]

### turn the object into a new dataframe ###
number_3 = DataFrame(n3.values, index=n3.index) 
number_3.columns = ['numlisteners']
print
print 40 * '!'
print
print "3. What artists have the most listeners?"
print number_3
########################

### make a group object to find most plays per user ###
n4 = a2ua_df.groupby(['name', 'aid'])['weight'].mean().order(ascending=False)

### turn the object into a new dataframe ###
top_avg = DataFrame(n4.values, index=n4.index) 
top_avg.columns = ['avg plays per listener']

### make a group object to find most users per artist (in a different format than number_3 ) ###
n44 = a2ua_df.groupby(['name', 'aid'])['uid'].count().order(ascending=False)

### turn the object into a new dataframe ###
most_listeners = DataFrame(n44.values, index=n44.index) 
most_listeners.columns = ['numlisteners']

### this filters out low uid's: ###
most_listeners_df = most_listeners[most_listeners['numlisteners']>=50] 

### this joins the two dataframes on aid ###
number_4 = top_avg.join(most_listeners_df)

### this Hides nulls, but doesn't drop them: ###
number_4 = number_4[np.isfinite(number_4['numlisteners'])] 

### this drops the erroneous column: ###
number_4 = number_4.drop(['numlisteners'], axis=1) 

### this gets the output down to 2 decimal places: ###
number_4 = np.round(number_4, 2)
print
print 40 * '!'
print
print "4. What artists with at least 50 listeners have the highest average number of plays per listener?"
print
print number_4.head(10)
############################

### these columns are erroneous for this query ###
a2uta = a2uta.drop(['uid', 'day'], axis=1)

### this filters out any year not 2005 ###
oh_5 = a2uta[a2uta['year']<2006]

### these filter the months needed ###
aug = oh_5[oh_5['month']==8]
sep = oh_5[oh_5['month']==9]

### make an August group object ###
n5a = aug.groupby(['name', 'aid'])['tagID'].count().order(ascending=False)

### turn the object into a new dataframe ###
number_5a = DataFrame(n5a.values, index=n5a.index) 
number_5a.columns = ['numtags']

### make a September group object ###
n5s = sep.groupby(['name', 'aid'])['tagID'].count().order(ascending=False)

### turn the object into a new dataframe ###
number_5s = DataFrame(n5s.values, index=n5s.index) 
number_5s.columns = ['numtags']
print
print 40 * '!'
print
print "5. For August and September 2005, what artists were tagged the most?"
print 
print "Aug 2005"
print "   ", number_5a.head(10)
print
print "Sep 2005"
print "   ", number_5s.head(10)
########################
