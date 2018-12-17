# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 09:53:34 2018

@author: William Keilsohn 
"""

'''
A quick note before progressing:
    Where there is a link/citation at the begining of a function (like right after the colon), please assume it applies to the entier function as there is mostlikly multiple lines
    referenced from the same page within that function.In other words, there are some places where a function references a single source multiple times, and to save comment space 
    the source is only placed at the very begining of the function. 
    Thank you.
'''


# Import Packages
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import random

# Load in the Data

### Deal with some file path issues: https://stackoverflow.com/questions/7165749/open-file-in-a-relative-location-in-python
programLoc = 'C://Users//kingw//Documents//CISC8000_Projects_2018'
folderLoc = programLoc + '//FBIdata'

# Import additional files
exec(open(folderLoc + '//Girls.py').read()) #From Twitter project

### Sub folders on my Computer
dataFolders = []
for x in range(13, 18):
    dataFolders.append(folderLoc + '//20' + str(x) + '_Data//')
    
# The data will need to be cleaned as it comes in
colNames = ['City', 'Population', 'Violent Crime', 'Murder', 'Rape 1', 'Rape 2', 'Robbery', 'Aggravated Assult', 'Property Crime', 'Burglary', 'Larceny', 'Motor Vehicle Theft', 'Arson']
newNames = ['City', 'Population', 'Violent Crime', 'Murder', 'Rape 1', 'Robbery', 'Aggravated Assult', 'Property Crime', 'Burglary', 'Larceny', 'Motor Vehicle Theft', 'Arson', 'Rape 2']
droprows = [x for x in range(0,3)]
keeprows = [x for x in range(0, 13)]

def dataCleaner(file):
    fileState = ''
    tempColumns = []
    fileState = file.iloc[0][0]
    cleanerFile = file.drop(droprows) # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
    cleanerFile.columns = cleanerFile.iloc[0] #https://stackoverflow.com/questions/26147180/convert-row-to-column-header-for-pandas-dataframe
    cleanerFile = cleanerFile.reindex(cleanerFile.index.drop(3)) # Same source as directly above. This is to deal with some files having extra blank columns.
    tempColumns = list(cleanerFile.columns[0:]) # From class
    if len(cleanerFile.columns) == 12: #https://stackoverflow.com/questions/20297332/python-pandas-dataframe-retrieve-number-of-columns
        #cleanerFile.insert(loc = 0, column = 'Rape (2)', value = '&&&') #https://stackoverflow.com/questions/18674064/how-do-i-insert-a-column-at-a-specific-column-index-in-pandas
        cleanerFile['Rape (2)'] = '&&&' #Turns out 2017 data dropped the old definition of Rape completely.
        cleanerFile.columns = newNames
    elif len(tempColumns) == 13:
        if type(tempColumns[12]) is str:
            cleanerFile.columns = colNames
        else:
            cleanerFile.columns = newNames
    else:
        newColumns = tempColumns[0:13]
        cleanerFile = cleanerFile[newColumns]
        if type(newColumns[12]) is str:
            cleanerFile.columns = colNames
        else:
            cleanerFile.columns = newNames
    cleanerFile = cleanerFile[:-1] #For some reason the last row has a space in it
    cleanerFile['State'] = fileState
    cleanerFile = cleanerFile.fillna('&&&') # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.fillna.html
    '''
    I need to fill the spaces with something for this next part, but I can't do it with just 0's due to the nature of the data.
    When the FBI leaves a space blank, it is b/c data is either missing and/or not their job to keep track of. This is different
    than the data being non-existant. To place a 0 there would create a bias in the results. Therefore, here is a filler charater.
    '''
    cleanerFile = cleanerFile[cleanerFile.City != '&&&'] #https://chrisalbon.com/python/data_wrangling/pandas_dropping_column_and_rows/
    for index, row in cleanerFile.iterrows(): #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        if row[0][0].isdigit(): #https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
            cleanerFile = cleanerFile[cleanerFile.City != row[0]]
    cleanedFile = cleanerFile
    return cleanedFile



### Now load the data
def FileLoader(path): #https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory
    directory = os.fsencode(path)
    yearData = pd.DataFrame(columns = colNames)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        stateData = pd.read_excel(path + filename) # We did csv in class. When you go to type that command in, excel comes up as an option.
        newState = dataCleaner(stateData)
        #yearData = pd.concat([yearData, newState], ignore_index = True)
        yearData = yearData.append(newState, sort = True)
        #yearData = pd.concat([yearData, newState], sort = True) #Previous assingment
    return yearData # This does work, but you need to do something with the data
        #print(filename) # Just wanted to make sure this works
 

### Progress through each subfolder and create the master data set
bigData = pd.DataFrame(columns = colNames)       
        
for i in range(0, len(dataFolders)):
    folderData = FileLoader(dataFolders[i])
    folderData['Year'] = str( i + 2013) # Since I'm making one large dataframe, I want to be able to sort by year and state. 
    bigData = bigData.append(folderData, sort = True)
    #bigData = pd.concat([bigData, folderData], sort = True) #https://pandas.pydata.org/pandas-docs/stable/merging.html#set-logic-on-the-other-axes

 
'''
I'm filling in the '&&&' here with Zeros despite my earlier comments, as I'm currently not taking standard deviations.
When I need to take standard deviations, I'll see to a work around.
https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.replace.html
'''
bigData = bigData.replace('&&&', 0) # Removes old place holder characters with 0's
    
# Begin asking questions
yearNames = ['2013', '2014', '2015', '2016', '2017'] #Establish range of years.


## Functions to make graphs and plots

### Make line charts
def lineGrapher(dFrame): #https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
    ## Works!
    print('\n')
    dFrame.plot(kind = 'line') #https://www.dataquest.io/blog/pandas-pivot-table/
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0) #https://matplotlib.org/users/legend_guide.html
    plt.ylabel('Number of Crimes Known to Law Enforcement')
    plt.xticks(np.arange(len(dFrame.index.values)), dFrame.index.values) #https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xticks.html
    # https://stackoverflow.com/questions/18358938/get-row-index-values-of-pandas-dataframe-as-list
    axes = plt.gca()
    maxVal = dFrame.max().max()
    axes.set_ylim([-10, (maxVal + 10)]) #https://stackoverflow.com/questions/3777861/setting-y-axis-limit-in-matplotlib
    plt.show()
    print('\n')


### Make bar charts
def barGrapher(dFrame): #https://pythonspot.com/matplotlib-bar-chart/
    print('\n')
    fig, ax = plt.subplots()
    index = np.arange(len(dFrame.index.values)) #https://stackoverflow.com/questions/18358938/get-row-index-values-of-pandas-dataframe-as-list
    colLis = list(dFrame)
    for i in range(0, len(colLis)):
        plt.bar(index + (0.35 * i), dFrame.iloc[:, i], 0.35, label = colLis[i]) #https://stackoverflow.com/questions/18358938/get-row-index-values-of-pandas-dataframe-as-list
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0) #https://matplotlib.org/users/legend_guide.html
    plt.ylabel('Number of Crimes Known to Law Enforcement')
    plt.xticks(index, dFrame.index.values, rotation = 90, size = 6) #https://matplotlib.org/api/_as_gen/matplotlib.pyplot.xticks.html
    #https://stackoverflow.com/questions/18358938/get-row-index-values-of-pandas-dataframe-as-list
    plt.show()
    print('\n')

### Make line charts with alternative axis
def lineSideGrapher(dFrame): #https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
    print('\n')
    for index, row in dFrame.iterrows(): #https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
        yLis = []
        yLis.append(row['2013'])
        yLis.append(row['2014'])
        yLis.append(row['2015'])
        yLis.append(row['2016'])
        yLis.append(row['2017'])
        plt.plot(yearNames, yLis, label = row['City'])
    plt.ylabel('Number of Crimes Known to Law Enforcement')
    plt.xlabel('Year') #As I know I'm only going to use this in one place
    plt.legend(bbox_to_anchor = (1.05, 1), loc = 2, borderaxespad = 0) #https://matplotlib.org/users/legend_guide.html
    plt.show()
    print('\n')
    


### Data Frame/Variable Isolator
def varIsolator(editedDF, extraVar, localVar): #From previous assignment
    valLis = []
    gapVar = ''
    localVal = localVar
    valFrame = pd.DataFrame()
    if extraVar == 'Year':
        if localVar == 'State': ### Works.
            gapVar = extraVar
            valLis = colNames[2:]
        elif localVar in colNames[2:]: ### Works.
            gapVar = extraVar
            localVal = 'State'
            valLis = localVar
        else:
            gapVar = 'State'
            localVal = extraVar
            valLis = localVar            
    else:   
        if localVar == 'Year': ### Works.
            gapVar = extraVar
            valLis = colNames[2:]
        elif localVar in colNames[2:]:  ### Works.
            gapVar = extraVar
            localVal = 'Year'
            valLis = localVar
        else:  ### Works.
            gapVar = 'Year'
            localVal = extraVar
            valLis = localVar
    valFrame = editedDF.pivot_table(valLis, index = gapVar , columns = localVal, aggfunc = sum) # From previous assignment and lots of fooling around in the console  
    return valFrame    
       
#### Central State checker
# Data for postal codes provided by: https://www.bls.gov/cew/cewedr10.htm
codeFrame = pd.read_excel(folderLoc + '//postalCodes.xlsx')

upperState = []
for a in range(0, len(codeFrame)):
    upperState.append(codeFrame['State'][a].upper())
codeFrame['State'] = upperState ## Provide a dataframe of capitalized states

stateDic = {} ### Link abreviations to state
for j in range(0, len(codeFrame)):
    stateDic[codeFrame['Code'][j]] = codeFrame['State'][j]
    
def stateCleaner(state): ### Ensure that the user entered an actual state.
    if len(state) == 2:
        if state in stateDic: # https://stackoverflow.com/questions/1602934/check-if-a-given-key-already-exists-in-a-dictionary
            newState = stateDic[state]
        else:
            newState = 'DISTRICT OF COLUMBIA'
            print('The state you have entered does not appear to be avaiable in our database. May I interest you in D.C. data?')
    elif len(state) > 2:
        if state in upperState:
            newState = state
        else:
            newState = 'MARYLAND'
            print('It appears the state you have selected is not in our system. May I interest you in MD data instead?')
    else:
        newState = 'DELAWARE'
        print('It appears that state is not currently avaiable. How about DE data?')
    return newState

### Start with the year
    
### Clean up data in relation to year/crime
def yearTrimmer(yearFrame):
    newData = yearFrame.drop(columns = ['City', 'Year', 'State']) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
    totalData = pd.DataFrame(newData[colNames[2:]].sum()) # https://stackoverflow.com/questions/41286569/get-total-of-pandas-column/41286607
    totalData.columns = ['Crime'] # We covered something similar to this when we added columns. Turns out you can re-name them the same way.
    return totalData

### Search by year
def yearSearcher(year):
    if year in yearNames:
        yearData = bigData[bigData.Year == year] # From previous assignment
        userData = pd.DataFrame()
        localVar = 'Year'
        print('\n')
        print('How would you like to examine the data?')
        followUpInput = input('Please provide an indipendent variable (crime or state): ')
        followUpInput = followUpInput.title()
        if followUpInput == 'Crime':
            userData = yearTrimmer(yearData)            
            barGrapher(userData)
#            print(userData.head())
        elif followUpInput == 'State':
            userData = varIsolator(yearData, followUpInput, localVar)
            barGrapher(userData)
#            print(userData.head())
        else:
            print("It appears that you have entered an invalid option")
    else:
        print('That year is unavailable')
    
### Sort by crime
def crimeSearcher(crime):
    crime = crime.title()
    if crime in colNames:
        crimeData = bigData[['State', crime, 'Year', 'Population']] #Previous Assignment
        userData = pd.DataFrame()
        localVar = crime
        print('\n')
        print('How would you like to examine the data?')
        followUpInput = input('Please provide an independent variable (state or year): ')
        followUpInput = followUpInput.title()
        if followUpInput == 'State':
            userData = varIsolator(crimeData, followUpInput, localVar)
            barGrapher(userData)
#            print(userData.head())
        elif followUpInput == 'Year':
            userData = varIsolator(crimeData, followUpInput, localVar)
            lineGrapher(userData)
#            print(userData.head())
        else:
            print("It appears that you have entered an invalid option")
    else:
        print('Sorry but the crime data you have requested could not be found. Are you sure it was entered correctly?')
        
### Sort by state
def stateTrimmer(stateFrame): ### Clean the data by state/city
    newData = stateFrame.drop(columns = ['State']) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
    for i in range(0, len(yearNames)):
        tempData = newData[newData.Year == yearNames[i]]
        tempData = tempData.drop(columns = ['Year']) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
        tempData = tempData.pivot_table(colNames[2:], index = 'City', aggfunc = sum)
        tempData = tempData.sum(axis = 1) #http://blog.mathandpencil.com/column-and-row-sums
        tempData = pd.DataFrame(tempData)
        tempData.columns = [yearNames[i]] # See above
        tempData = tempData.reset_index() #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.reset_index.html
#    return tempData
        if i == 0:
            finalData = tempData['City']
            finalData = pd.DataFrame(finalData)
        else:
            finalData = finalData
        finalData = finalData.merge(tempData, how = 'left', on = ['City']) #https://stackoverflow.com/questions/33086881/merge-two-python-pandas-data-frames-of-different-length-but-keep-all-rows-in-out
    finalData = finalData.fillna(0) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.fillna.html
    return finalData      
        
def stateSearcher(state): ### Search by state
    state = state.upper()
    state = stateCleaner(state)
    stateData = bigData[bigData.State == state]
    userData = pd.DataFrame()
    localVar = 'State'
    print('\n')
    print('How would you like to examine the data?')
    followUpInput = input('Please enter an additional independent variable (year or city): ')
    followUpInput = followUpInput.title()
    if followUpInput == 'Year':
        userData = varIsolator(stateData, followUpInput, localVar)
        lineGrapher(userData)
#        print(userData.head())
    elif followUpInput == 'City':
        userData = stateTrimmer(stateData)
        lineSideGrapher(userData)
#        print(userData.head())
    else:
        print('The option you have selected is unavailable')

### Produce something at random
def numRandomer(): # https://www.pythoncentral.io/how-to-generate-a-random-number-in-python/
    num1 = random.randint(0, 2)
    num2 = random.randint(0, 50)
    num3 = random.randint(0, 4)
    num4 = random.randint(0, 10)
    num5 = random.randint(0, 5)
    numLis = [num1, num2, num3, num4, num5]
    return numLis
        
def supriseData(lis):
    dFrame = bigData
    if lis[0] == 0:
        tempFrame = dFrame[dFrame.Year == yearNames[lis[2]]]
        newData = tempFrame.drop(columns = ['City', 'State', 'Year']) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
        newData = newData.sum(axis = 0) # http://blog.mathandpencil.com/column-and-row-sums
        newData = newData.sum(axis = 0) # Running this again to go from a bunch of column sums to a single digit.
        finalString = 'There were \n' + str(newData) + '\ncrimes known to law \nenforcement in \n' + yearNames[lis[2]] + '.'
    elif lis[0] == 1:
        tempFrame = dFrame[dFrame.State == upperState[lis[1]]]
        newData = tempFrame.drop(columns = ['City', 'State', 'Year']) #https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.drop.html
        newData = newData.sum(axis = 0) # http://blog.mathandpencil.com/column-and-row-sums
        newData = newData.sum(axis = 0) # Running this again to go from a bunch of column sums to a single digit.
        finalString = 'There have been \n' + str(newData) + '\ncrimes known to law \nenforcement in \n' + upperState[lis[1]] + ' over the last five years.'
    else:
        numy = lis[3] + 2
        tempFrame = dFrame[colNames[numy]]
        newData = tempFrame.sum(axis = 0) # http://blog.mathandpencil.com/column-and-row-sums
        finalString = 'There have been \n' +  str(newData) + '\n ' + colNames[numy] + '(s) \n' + 'over the last five years.'
#    print(finalString)
    return finalString

def memePrinter(lis):
    string = supriseData(lis)
    print('\n')
    memeStatus = input('Would you like a meme? --Note: Selecting a meme ends the program.-- (yes/no) ')
    memeStatus = memeStatus.title()
    if memeStatus == 'Yes' or memeStatus == 'Y':
        textWritter(string, lis[4])
        print ('\n')
        print('Original image Source: ' + sourceLis[lis[4]])
    else:
        print(string)
        print('\n')
    
    
#-------------------------------------------------------------------------------------------------#    
##### Everything below this line is to make the project look better. Data processing is above. ####    
#-------------------------------------------------------------------------------------------------#    
    
### Lets's Give the user a "console" so they know what their options are going to be:
print('Hello, and Welcome to the Computer Science Final Project')

runChecker = True ### Determine if the program should continue to run.

def endProgram(string): ### Evaluate the status of the program
    string = string.title()
    if string == 'Yes' or string == 'Y':
        runChecker = True
    else:
        runChecker = False
    return runChecker


    
while runChecker == True: ### Navigate through the options
    print('\n')
    initialInput = input('Please type one of the following commands to Search By: "Year", "Crime", "State", or "Suprise Me": ')
    print('\n')
    initialInput = initialInput.title()
    yearInput = ''
    crimeInput = ''
    stateInput = ''
    if initialInput == 'Year':
        yearInput = input('Please enter an available year (2013, 2014, 2015, 2016, 2017): ')
        yearSearcher(yearInput)
        cont = input('Would you like to continue searching (yes/no)? ')
        runChecker = endProgram(cont)
    elif initialInput == 'Crime':
        optionString = 'Please enter one of the available types of crime (' + str(colNames[2:12]) + '): '
        crimeInput = input(optionString)
        crimeSearcher(crimeInput)
        cont = input('Would you like to continue searching (yes/no)? ')
        runChecker = endProgram(cont)
    elif initialInput == 'State':
        stateInput = input("Please enter the name of a state (including DC): ")
        stateSearcher(stateInput)
        cont = input('Would you like to continue searching (yes/no)? ')
        runChecker = endProgram(cont)
    elif initialInput == 'Suprise Me':
        ranLis = numRandomer()
        memePrinter(ranLis)
        runChecker = False
        break
    elif initialInput == 'Kys':
        runChecker = endProgram('kys')
    else:
        print("Look, I get that it's the end of the year, but can you please just pick one?")


if runChecker == False: ### "Close" program
    print('\n')
    print('Thank you for using my project and have a Happy Holiday!')