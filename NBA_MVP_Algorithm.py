#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd

headers  = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}
column_names = ["PLAYER_ID",
"PLAYER_NAME",
"NICKNAME",
"TEAM_ID",
"TEAM_ABBREVIATION",
"AGE",
"GP",
"W",
"L",
"W_PCT",
"MIN",
"FGM",
"FGA",
"FG_PCT",
"FG3M",
"FG3A",
"FG3_PCT",
"FTM",
"FTA",
"FT_PCT",
"OREB",
"DREB",
"REB",
"AST",
"TOV",
"STL",
"BLK",
"BLKA",
"PF",
"PFD",
"PTS",
"PLUS_MINUS",
"NBA_FANTASY_PTS",
"DD2",
"TD3",
"WNBA_FANTASY_PTS",
"GP_RANK",
"W_RANK",
"L_RANK",
"W_PCT_RANK",
"MIN_RANK",
"FGM_RANK",
"FGA_RANK",
"FG_PCT_RANK",
"FG3M_RANK",
"FG3A_RANK",
"FG3_PCT_RANK",
"FTM_RANK",
"FTA_RANK",
"FT_PCT_RANK",
"OREB_RANK",
"DREB_RANK",
"REB_RANK",
"AST_RANK",
"TOV_RANK",
"STL_RANK",
"BLK_RANK",
"BLKA_RANK",
"PF_RANK",
"PFD_RANK",
"PTS_RANK",
"PLUS_MINUS_RANK",
"NBA_FANTASY_PTS_RANK",
"DD2_RANK",
"TD3_RANK",
"WNBA_FANTASY_PTS_RANK",
"CFID",
"CFPARAMS"]

cols = ["PLAYER_NAME","W_PCT", "MIN", "GP","FG_PCT_RANK","PTS_RANK", "NBA_FANTASY_PTS_RANK","W_PCT_RANK", "PLUS_MINUS_RANK","REB_RANK","AST_RANK","TOV_RANK","STL_RANK","BLK_RANK"]


# In[2]:


d = [*range(96,100,1)]
e = [*range(0,10,1)]
f = [*range(10,23,1)]
for i in range(len(e)):
    e[i] = '%02d' % i
    
for i in range(len(d)):
    d[i] = str(d[i])
    
for i in range(len(f)):
    f[i] = str(f[i])
    
    

years = d + e + f

for i in range(len(years)-1):
    years[i] = str(years[i]+"-"+years[i+1])
    
    if years[i][0] == '8' or years[i][0] == '9':
        years[i] = str('19'+years[i])
        
for i in range(4,len(years)-1,1):
    years[i] = str('20'+years[i])
    

years.pop()
print(years)


# In[3]:


urlyearslist = []
i = 0
while i < len(years):
    playerinfourl = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=' + years[i] + '&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
    urlyearslist.append(str(playerinfourl))
    i = i+1


# In[4]:


d = {}
j = 0
while j < len(urlyearslist):
    tempurl = urlyearslist[j]
    
    response = requests.get(url=tempurl,headers=headers).json()
    player_info = response['resultSets'][0]['rowSet']
    
    d[years[j]] = pd.DataFrame(player_info, columns = column_names)
    print(j)
    j = j+1


# In[79]:


def pointsrank(row):
    if row['PTS_RANK'] > 1:
        return 1
    else:
        return 0.85


# In[80]:


n = 0
newdf = {}
while n<len(years):
    newdf[years[n]] = d[years[n]][cols]
    newdf[years[n]]['points_rank_multiplier'] = newdf[years[n]].apply(lambda row: pointsrank(row), axis=1)
    
    
    n = n+1


# In[81]:


firstsumcols = ["PTS_RANK", "W_PCT_RANK","TOV_RANK","REB_RANK","AST_RANK","NBA_FANTASY_PTS_RANK"]
#
m = 0
while m<len(years):
    if m == 2:
        newdf[years[m]] = newdf[years[m]][newdf[years[m]]['GP']>30]
        newdf[years[m]] = newdf[years[m]][newdf[years[m]]['MIN']>25]
        m = m+1
        continue
        
    else:
        newdf[years[m]] = newdf[years[m]][newdf[years[m]]['GP']>55]
        newdf[years[m]] = newdf[years[m]][newdf[years[m]]['MIN']>25]
    
    m = m+1
    
print(newdf[years[0]].head(3))


# In[82]:


z = 0
sum_df = {}
another_df = {}

while z<len(years):
    sum_df[years[z]] = newdf[years[z]]
    sum_df[years[z]]['sum'] = sum_df[years[z]][firstsumcols].sum(axis=1)
    sum_df[years[z]]['inversewinpercentage'] = 1-sum_df[years[z]]['W_PCT']
    sum_df[years[z]]['sumtimesinversewinpercentage'] = sum_df[years[z]]['sum']*sum_df[years[z]]['inversewinpercentage']*sum_df[years[z]]['points_rank_multiplier']
    
   
    
    another_df[years[z]] = sum_df[years[z]].sort_values(by=['sumtimesinversewinpercentage'])
    print(z)
    z = z+1


v = 0
top5_df = {}
while v<len(years):
    top5_df[years[v]] = another_df[years[v]].head(5)
    v = v+1
print(top5_df[years[1]])


# In[83]:


winners = ["Karl Malone","Michael Jordan","Karl Malone","Shaquille O'Neal",'Allen Iverson','Tim Duncan','Tim Duncan','Kevin Garnett','Steve Nash','Steve Nash','Dirk Nowitzki','Kobe Bryant','LeBron James','LeBron James','Derrick Rose','LeBron James','LeBron James','Kevin Durant','Stephen Curry','Stephen Curry','Russell Westbrook','James Harden','Giannis Antetokounmpo','Giannis Antetokounmpo','Nikola Jokic','Nikola Jokic']


# In[87]:



it = 0
firstplacepredictlist = []

while it <len(years):
    firstholder = top5_df[years[it]].iloc[0]["PLAYER_NAME"]
    
    firstplacepredictlist.append(firstholder)
    
    it = it+1
    
correct = 0
correctscoreiter = 0

while correctscoreiter < len(firstplacepredictlist):
    if firstplacepredictlist[correctscoreiter] == winners[correctscoreiter]:
        correct = correct+ 1
    correctscoreiter = correctscoreiter+1

score = correct/len(years)
print(correct)
print(len(years))
print(score)


# In[ ]:


#first place mvp correctly predicted 18/26 or 0.6923076923076923 or 69.23% of the time


# In[ ]:




