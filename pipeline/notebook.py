#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd


# In[22]:


url ='https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz'


# In[23]:


df = pd.read_csv(url)


# In[24]:


df


# In[25]:


df["store_and_fwd_flag"]


# In[26]:


df.describe()


# In[27]:


df.info()


# In[28]:


df.isnull().sum()


# In[29]:


df.head()


# In[30]:


df.tail()


# In[31]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    #prefix + 'yellow_tripdata_2021-01.csv.gz',
    url,
    #nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[32]:


df.head()


# In[33]:


get_ipython().system('uv add psycopg2-binary')


# In[34]:


get_ipython().system('uv add sqlalchemy')


# In[35]:


get_ipython().system('uv add psycopg2')


# In[39]:


#SQLAlchemy is a Python library that acts as a translator and bridge between your Python code and a relational database (like PostgreSQL, MySQL, or SQLite).
from sqlalchemy import create_engine
from tqdm.auto import tqdm

engine = create_engine('postgresql://root:root@localhost:5433/ny_taxi')


# In[44]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[41]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[42]:


df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(
        name='yellow_taxi_data',
        con=engine,
        if_exists='append'
    )


# In[ ]:





# In[ ]:




