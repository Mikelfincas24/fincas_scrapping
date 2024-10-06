from bs4 import BeautifulSoup
import asyncio
import httpx
import re
import mechanicalsoup
import pandas as pd
from bs4 import BeautifulSoup
import json
import time
import streamlit as st








data_json = {}


def insert_valores_json(row):
    try:
        
        if pd.isna(row["EMAIL"]) == True:
            return data_json[str(row["Indice"])]
        else:
            return row["EMAIL"]
    except:
        pass

class AsyncSpiderFunctions:

    def analizar(self,link,company):
        try:

            data_link = link.get("href")
            if data_link.startswith("http"):
                return data_link

            else:
                return "No hay valores"
            
        except:
            return "No hay valores"



    async def fetch_httpx_html(self, value,browser,company,indice,client):


        browser.open("https://www.bing.com")

        browser.select_form('form[action="/search"]')

        browser["q"] = value

        browser.submit_selected()
        # ---------------------------------------------------

        html_content = browser.page.prettify()

    

        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_content)

        if emails:
            for email in emails:
                data_json[str(indice)] = email
                print(email,value)
                return email

        # --------------------------------------
        else:
            try:

                xpl =  [self.analizar(link,company) for link in browser.page.find_all('a')]
                if list(filter(lambda x: "empresite.eleconomista.es" in x,xpl)):
                    url_email = list(filter(lambda x: "empresite.eleconomista.es" in x,xpl))[0]
                else:
                    url_email = list(filter(lambda x: x.startswith("http"),xpl))[0]
                
                soup_data = await client.get(url_email)
                
                email_page = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup_data.text)
                data_json[str(indice)] = email_page[0]
                
                print(email_page[0],"---------",value)
            except Exception as e:
                print(f"Error: {e}")


    async def httpx_http(self,dataframe):
        df = pd.read_excel(dataframe)

        df_final = df.copy()

        df = df.loc[(df["SITUACIO"] == "EXERCENT") & (df["PHONE"].isna()==False)]

        df["PHONE"] = df["PHONE"].astype(str)
        df_final["PHONE"] = df_final["PHONE"].astype(str)

        values = df["PHONE"].values
        company_names = df["NOM_COMERCIAL"].values
        indice_valores = df.index


        async with httpx.AsyncClient() as client:


            browser = mechanicalsoup.StatefulBrowser()

            browser.session.headers.update(({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "es-ES,es;q=0.9",
                "Connection": "keep-alive",
                "Referrer-Policy": "origin-when-cross-origin"
            }))

            
            tasks = [self.fetch_httpx_html(value,browser,company,indice,client) for value,company,indice in zip(values,company_names,indice_valores)]
            results = await asyncio.gather(*tasks)

            other_value = sorted(data_json.items(),key=lambda x: int(x[0]))
            values_xp = dict(list(filter(lambda x: "axesor" not in x[1] and "einforma" not in x[1] ,other_value)))
            df_final["Indice"] = list(range(0,df_final.shape[0]))
            df_final["Indice"] = df_final["Indice"].astype(str)
            df_final["New_email"] = df_final.apply(insert_valores_json,axis=1)
            df_final.drop(columns=["EMAIL","Indice"],inplace=True)
            print(data_json)

            return df_final

            # return data_json
            # return results


          


# values = ["666 360 898","936994304"]



# if __name__ == "__main__":
#     start = time.perf_counter()
#     spider = AsyncSpiderFunctions()
#     valores = asyncio.run(spider.httpx_http(values))
#     print(valores)
    # with open(r"C:\Users\Cash\Proyectos\092024\Multiples administradores fincas web scrapping\values.json","w") as j:
    #     json.dump(data_json,j)
    

