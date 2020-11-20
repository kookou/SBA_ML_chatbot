#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


df = pd.read_csv("ratings.dat", sep="::", encoding='UTF-8')


# In[3]:

df.head()

# In[4]:


df.columns = ["user_id", "item_id", "rating", "timestamp"]
df.head()


# In[5]:


df.shape


# In[6]:


n_users = df.user_id.unique().shape[0]
n_users


# In[7]:


n_items = df.item_id.unique().shape[0]
n_items


# In[8]:


ratings = np.zeros((n_users, n_items))


# In[9]:


ratings


# In[10]:


ratings.shape


# In[11]:


for row in df.itertuples():
    # if(row[2]-1 < 3706):
        ratings[row[1]-1, row[2]-1] = row[3]


# In[12]:


ratings


# In[13]:


from sklearn.model_selection import train_test_split

ratings_train, ratings_test = train_test_split(ratings, test_size=0.33, random_state=42)


# In[14]:


ratings_train.shape


# In[15]:


from sklearn.metrics.pairwise import cosine_similarity

user_distances = cosine_similarity(ratings_train)
user_distances


# In[16]:


user_pred = user_distances.dot(ratings_train) / np.array([np.abs(user_distances).sum(axis=1)]).T


# In[17]:


from sklearn.metrics import mean_squared_error

def get_mse(pred, actual):
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mean_squared_error(pred, actual)


# In[18]:


np.sqrt(get_mse(user_pred, ratings_train))


# In[19]:


np.sqrt(get_mse(user_pred, ratings_test))


# In[20]:


from sklearn.neighbors import NearestNeighbors

k=5
neigh = NearestNeighbors(n_neighbors=k, metric="cosine")


# In[21]:


neigh.fit(ratings_train)


# In[22]:


top_k_distances, top_k_users = neigh.kneighbors(ratings_train, return_distance=True)


# In[23]:


top_k_users


# In[24]:


top_k_distances


# In[25]:


user_pred_k = np.zeros(ratings_train.shape)


# In[26]:
# 수행시간이 오래 걸림 4046회 수행

for i in range(ratings_train.shape[0]):
    if(i%50==0):
        print("cnt = ", i)
    user_pred_k[i, :] = top_k_distances[i].T.dot(ratings_train[top_k_users][i]) /                         np.array([np.abs(top_k_distances[i].T).sum(axis=0)]).T


# In[27]:


user_pred_k


# In[28]:


np.sqrt(get_mse(user_pred_k, ratings_train))


# In[29]:


np.sqrt(get_mse(user_pred_k, ratings_test))


# In[ ]:




