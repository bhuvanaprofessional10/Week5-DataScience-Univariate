import pandas as pd
import numpy as np

class Univariate:
    def get_Quan_Qual(self,source):
        qual=[]
        quan=[]
        for col in source.columns:
            if(source[col].dtypes == 'O'):
                qual.append(col)
            else:
                quan.append(col)
    
        return qual,quan

    
    def get_univariate_statistics(self,dataset,quan_col):    
        UserTable_without=pd.DataFrame(index=["Mean","Median","Mode","Minimum","Maximum","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
                                     "IQR","1.5rule","Low_IQR_Limit","high_IQR_Limit"],columns=quan_col)
        for col in quan_col:
            UserTable_without.loc["Mean",col]=float(dataset[col].mean())
            UserTable_without.loc["Median",col]=float(dataset[col].median())    
            UserTable_without.loc["Mode",col]=float(dataset[col].mode()[0]) 
            UserTable_without.loc["99%",col]=float(np.percentile(dataset[col],99))
            UserTable_without.loc["Q4:100%",col]=dataset.describe()[col]["max"]
            UserTable_without.loc["Minimum",col]=float(dataset[col].min())
            UserTable_without.loc["Maximum",col]=float(dataset[col].max())
            UserTable_without.loc["Q1:25%",col]=dataset.describe()[col]["25%"]
            UserTable_without.loc["Q2:50%",col]=dataset.describe()[col]["50%"]
            UserTable_without.loc["Q3:75%",col]=dataset.describe()[col]["75%"]
            UserTable_without.loc["IQR",col]= dataset.describe()[col]["75%"] - dataset.describe()[col]["25%"]
            UserTable_without.loc["1.5rule",col]= 1.5 * UserTable_without.loc["IQR",col]
            UserTable_without.loc["Low_IQR_Limit",col]= UserTable_without.loc["Q1:25%",col] - UserTable_without.loc["1.5rule",col]
            UserTable_without.loc["high_IQR_Limit",col]= UserTable_without.loc["Q3:75%",col] + UserTable_without.loc["1.5rule",col]
            
        return UserTable_without

    def get_outlier(UserTable,quan):
        lesser_outlier=[]
        greater_outlier=[]
    
        for col in quan:
            if UserTable[col]["Minimum"] < UserTable[col]["Low_IQR_Limit"]:
                lesser_outlier.append(col)
            if UserTable[col]["Maximum"] > UserTable[col]["high_IQR_Limit"]:
                greater_outlier.append(col)
    
        return lesser_outlier,greater_outlier

    def lesser_capping(UserTable,dataset,lesser_outlier):
        for column in lesser_outlier:
            l_limit=UserTable[column]["Low_IQR_Limit"]
            dataset.loc[dataset[column] < l_limit, column] = l_limit
        return dataset

    def greater_capping(UserTable,dataset,greater_outlier):
        for column in greater_outlier:
            h_limit=UserTable[column]["high_IQR_Limit"]
            dataset.loc[dataset[column] > h_limit, column] = h_limit
        return dataset

    def get_frequency(dataset,colName):
        index_count=int(dataset[colName].value_counts().count())
        freq_table=pd.DataFrame(columns=["Index","Frequency","Relative_Frequency","CumSum"])
        freq_table["Index"]=dataset[colName].value_counts().index.sort_values()
        freq_table["Frequency"]=dataset[colName].value_counts().values
        freq_table["Relative_Frequency"]=freq_table["Frequency"]/index_count
        freq_table["CumSum"] = freq_table["Frequency"].cumsum()
        return freq_table