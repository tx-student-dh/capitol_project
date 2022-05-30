import requests
import time
import os
import pandas as pd

def main():

        os.chdir("..")
        os.chdir("..")
        os.chdir(r"C:\Users\amyes\Box\TxDH\capitol_project\data")

        name = input("Enter filename without the .csv extension: ")
        filename = name + ".csv"
        df = pd.read_csv(filename)

        df['encoded_name'] = df['first_name'] + "%20" + df['last_name']
        df['encoded_name'] = df['encoded_name'].str.replace(' ','%20')
        df['nationality'] = " "
        df['nationality_prob']= " "
        df['ethnicity'] = " "
        df['ethnicity_prob']= " "
        
        outname = name + "_output.csv"
        name_prism("nat", df)
        name_prism("eth", df)
        df.to_csv(outname)
        print(outname + " is complete and uploaded to the working directory.")


def name_prism(search, dataframe):
        
        for index, row in dataframe.iterrows():
                searchname = row['encoded_name']
                if (pd.isna(searchname) == True):
                	searchname = row['last_name']

                url = "http://www.name-prism.com/api_token/" + search + "/json/[API TOKEN]/" + searchname
                response = requests.get(url)
                responselist = response.json()
                result = max(responselist, key=responselist.get)
                result_prob = max(responselist.values())

                if search == "nat":
                        varname = 'nationality'
                else:
                        varname = 'ethnicity'
                var_prob = varname + "_prob"
                dataframe.at[index, varname] = result
                dataframe.at[index, var_prob] = result_prob
                print("Index " + str(index) + " " + varname + " has been added.")
                time.sleep(1)

main()
