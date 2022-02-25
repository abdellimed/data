import pandas as pd
import pymongo
companie=pd.read_csv('companie.csv')
funding=pd.read_csv('funding-rounds.csv')
funding=funding.rename({'Organization Name': 'company_name','Organization Name URL':'company_permalink',
                            'Organization Description':'Organization_Description',
                            'Investor Names':'Investor_names','Organization Location':'Organization_Location'}, axis=1)

companie=companie.rename({'Organization Name': 'company_name','Organization Name URL':'company_permalink',
                            'Full Description':'Full_Description','Contact Email':'Contact_Email'}, axis=1) 


list_company=companie.company_name.to_list()
company_invt= pd.concat([funding.loc[funding['company_name'] == x] for x in set(list_company)])
company_invt.drop_duplicates(subset ="company_name", keep = 'first', inplace=True)
company_invt['Full_Description']=''
company_invt['Contact_Email']=''
company_invt['Industries']=''

index_with_nan=companie[companie.Industries==''].index
companie.drop(index_with_nan,0, inplace=True)
for i in range(len(company_invt)):
    for j in range(len(companie)):
        if((company_invt.iloc[i,3]==companie.iloc[j,0]) and type(companie['Industries'][j])==str):
            
            
            company_invt['Full_Description'][i]=companie['Full_Description'][j]
            company_invt['Contact_Email'][i]=companie['Contact_Email'][j]
           # print(companie['Industries'][j])
            company_invt['Industries'][i]=companie['Industries'][j].split(',')

index_with_nan=company_invt[company_invt.Full_Description.isnull()].index
company_invt.drop(index_with_nan,0, inplace=True)

index_with_nan=company_invt[company_invt.Full_Description==''].index
company_invt.drop(index_with_nan,0, inplace=True)

myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Relatic']
startups = mydb["startups"]


myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient['Relatic']
startups = mydb["startups"]
