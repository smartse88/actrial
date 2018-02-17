"""
Created by smartse: https://en.wikipedia.org/wiki/User:Smartse 
GNU GENERAL PUBLIC LICENSE Version 3
"""

'Import modules'
import pandas as pd
import numpy as np
from pandas import ExcelWriter

data=[] #list to store data

in_df = pd.read_excel("deletiondump.xlsx", sheet_name=0) #read data in
in_df =in_df.fillna('no comment') #fills in missing values
no_logs=len(in_df['log_comment']) #counts log entries
    
'loop to classify individual log entries'
for n in range(no_logs):#
        #read each log entry (have thought about removing wiki-markup)
        log=in_df.loc[n]['log_comment']#.replace("[["," ").replace("]]"," ").replace("|"," ")

        #prevents counting G10,G11 and G12 as G1, but won't catch dual rationales
        if ('G10' or 'g10') in log:
            G10 = 1
        elif ('G11' or 'g11' or 'spam') in log:
            G11 = 1        
        elif ('G12' or 'g12') in log:
            G12 = 1  
        elif ('G1' or 'g1') in log:
            G1 = 1  
        else: 
            G1,G10,G11,G12 = 0,0,0,0
        
        #catches any dual G11/G12 deletions, others can't crossover
        if ('G12' or 'g12') in log:
            G12 = 1
        else: 
            G12=0
        if ('G9' or 'g9') in log:
            G9 = 1
        else: 
            G9=0
        if ('G8' or 'g8') in log:
            G8 = 1
        else: 
            G8=0
        if ('G7' or 'g7') in log:
            G7 = 1
        else: 
            G7=0
        if ('G6' or 'g6') in log:
            G6 = 1
        else: 
            G6=0      
            
        if 'G5' in log or 'g5' in log or 'Mass deletion of pages' in log:
            G5 = 1
        else:
            G5=0
            
        if ('G4' or 'g4') in log:
            G4 = 1
        else: 
            G4=0
        if ('G3' or 'g3') in log:
            G3 = 1
        else: 
            G3=0
        if ('G2' or 'g2') in log:
            G2 = 1
        else: 
            G2=0
            
        #essentially impossible for these to overlap, so no need to have another statement
        if ('A10' or 'a10') in log:
            A10 = 1
        elif ('A11' or 'a11') in log:
            A11 = 1        
        elif ('A1' or 'a1') in log:
            A1 = 1  
        else: 
            A1,A10,A11 = 0,0,0
            
        if ('A9' or 'a9') in log:
            A9 = 1
        else: 
            A9=0
        if ('A8' or 'a8') in log:
            A8 = 1
        else: 
            A8=0
        if ('A7' or 'a7') in log:
            A7 = 1
        else: 
            A7=0
        if ('A5' or 'a5') in log:
            A5 = 1
        else: 
            A5=0
        if ('A3' or 'a3') in log:
            A3 = 1
        else: 
            A3=0
        if ('A2' or 'a2') in log:
            A2 = 1
        else: 
            A2 = 0
        
        #AFDs are cited in some PRODs but PROD is the rationale
        if ('PROD' or 'proposed') in log:
            PROD = 1
        else:
            PROD = 0
            
        if ('Wikipedia:Articles for deletion' or 'afd' or 'AFD') in log:
            AFD = 1
        else:
            AFD = 0
            
        if 'Redirect' in log or 'redirect' in log or 'R1' in log or 'R2' in log or 'R3' in log or 'X1' in log or 'eelix' in log: #eelix catches Neelix variants
            redirect=1
        else:
            redirect=0
            
        data.append((log,G1,G2,G3,G4,G5,G6,G7,G8,G9,G10,G11,G12,A1,A2,A3,A5,A7,A8,A9,A10,A11,PROD,AFD,redirect))

#place all of the data into a dataframe
df=pd.DataFrame(data=data)

#define column names
df.columns = ['log','G1','G2','G3','G4','G5','G6','G7','G8','G9','G10','G11','G12','A1','A2',\
                'A3','A5','A7','A8','A9','A10','A11','PRODt','AFDt','redirect']

'dropping redirects completely for now, but it would be nice to deal with them properly'
redirect=df[df.redirect==1]
df=df[df.redirect != 1] #removes redirects
df=df.drop('redirect', axis=1) #removes redirect column

'calculates total and copies unclassified to a new df in output'
df['total']=df.sum(axis=1) #sums columns - unclassifed = 0
df['other']=np.where(df['total']==0,1,0) #makes other = 1 if total = 0
unclass=df[df.total == 0] #copies unclassified to a new df
writer = ExcelWriter('Deletion_counts.xlsx') #creates output files
unclass.to_excel(writer,'Unclassified') #writes unclassfied entries to file

'recalculate PROD and AFD to be only where no CSD feature. a/b is necessary to catch PRODs that reference AFDs'
df['PRODa']=np.where(np.logical_and(np.equal(df['PRODt'],1),np.equal(df['total'],1)),1,0)
df['PRODb']=np.where(np.logical_and(np.equal(df['PRODt'],1),np.equal(df['AFDt'],1)),1,0)
df['PROD']=df['PRODa']+df['PRODb']
df=df.drop('PRODa',axis=1)
df=df.drop('PRODb',axis=1)
df=df.drop('PRODt',axis=1)
df=df.drop('total', axis=1)
df['total']=df.sum(axis=1)
df['AFD']=np.where(np.logical_and(np.equal(df['AFDt'],1),np.equal(df['total'],1)),1,0)
df=df.drop('AFDt',axis=1)
df=df.drop('total', axis=1)

'convert any multiple CSD/PROD criteria into fractions'
df['speedy']=df.iloc[:,1:23].sum(axis=1) #sums CSD columns
equalise=df.iloc[:,1:23].div(df.speedy, axis=0) #divides each column by total
equalise=equalise.fillna(0) #replace zeroes
df=df.drop('speedy',axis=1) #remove speedy
df.update(equalise) #overwrite old columns

'drop all other columns from redirect df and merge into output'
redirect=redirect.drop(redirect.iloc[:,0:24],axis=1)
out_df=df.append(redirect)

'recheck that each row sums to 1'
out_df['total2']=out_df.sum(axis=1) 
multiple=out_df[out_df.total2 >= 2]
zero=out_df[out_df.total2 ==0]
out_df=out_df.drop('total2', axis=1)

'convert timestamp to date, remove other inputs and merge into output'
in_df['date'] = pd.to_datetime(in_df['log_timestamp'], format='%Y%m%d%H%M%S')
in_df=in_df.drop(in_df.iloc[:,0:3],axis=1)
out_df=pd.concat([out_df,in_df], axis=1)

'write results to excel, including debugging sheets'
out_df.sum().to_excel(writer,'Results')
multiple.to_excel(writer,'Multiple')
zero.to_excel(writer,'Zero')
writer.save()

