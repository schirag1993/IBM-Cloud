
# coding: utf-8

# In[4]:


import json, requests, re
import numpy as np
from pprint import pprint
from watson_developer_cloud import DiscoveryV1


# In[5]:


def getIBMCreds():
#     credentials = json.load(open('../credentials.json'))
    username = input("Enter username: ")
    url = input("Enter url: ")
    password = input("Enter password: ")
    ibmCreds = {
        'username' : username,
        'password' : password,
        'url' : url
    }
#     ibmCreds = credentials['ibm']['discovery']
    return ibmCreds


# In[6]:


def getQuery():
    query = input('Enter the query to be searched: ')
    return(query)


# In[7]:


def constructQuery(query):
    query_options = {'natural_language_query': query,
                 'count' : 3,
                 'passages':True}
    return(query_options)


# In[8]:


def getQueryResults(discoveryDetails, queryOptions):
    env_id, collections, discovery = discoveryDetails
    queryResults = discovery.query(environment_id=env_id, 
                               collection_id=collections[0]['collection_id'],
                               natural_language_query=queryOptions['natural_language_query'], 
                               passages=queryOptions['passages'], count=queryOptions['count'])
    return(queryResults)


# In[9]:


def cleanPassage(passage):
    tagRegEx = re.compile('<.*?>')
    cleanedText = re.sub(tagRegEx, '', passage)
    cleanedText = cleanedText.rstrip()
    cleanedText = cleanedText.replace('\n', '. ')
    return(cleanedText)


# In[10]:


def getPassage(queryResults):
    passages = []
    for passage in queryResults['passages']:
        passages.append(passage)
    passageScore = 0
    targetPassages = []
    for passage in passages:
        for key in passage.keys():
            if(passageScore < passage['passage_score']):
                passageScore = passage['passage_score']
                targetPassages.append(passage)
    targetPassage = targetPassages[0]['passage_text']
    cleanedPassage = cleanPassage(targetPassage)
    print("Target passage with highest score is: ")
    print(targetPassage)
    return(cleanedPassage)


# In[11]:


def askDiscovery():
    print("--------------------***--------------------")
    print("IBM CREDENTIALS: ")
    print("--------------------***--------------------") 
    ibmCreds = getIBMCreds()
    print("--------------------***--------------------")
    print("--------------------***--------------------")
    discovery = DiscoveryV1(version='2017-11-07',
                            username=ibmCreds['username'],
                            password=ibmCreds['password'])
    env = discovery.list_environments()['environments'][1]
    env_id = env['environment_id']
    collections = discovery.list_collections(env_id)
    collections = collections['collections']
    discoveryDetails = (env_id, collections, discovery)
    print("--------------------***--------------------")
    print("QUERY: ")
    print("--------------------***--------------------")
    query = getQuery()
    print("--------------------***--------------------")
    print("--------------------***--------------------")
    queryOptions = constructQuery(query)
    queryResults = getQueryResults(discoveryDetails, queryOptions)
    passage = getPassage(queryResults)
    print("--------------------***--------------------")
    print("Passage after cleaning is: ")
    print("--------------------***--------------------")
    print(passage)
    print("========================================================================================")
    return(passage)


# In[ ]:


a = askDiscovery()

