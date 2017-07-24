
# coding: utf-8

# In[1]:

from PIL import Image

from resizeimage import resizeimage


# In[ ]:




# In[4]:

import os
rootdir = 'C:\\Users\\trini\\image_testing'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        
        img = Image.open(subdir+'\\'+ file)
        img = resizeimage.resize_thumbnail(img, [200, 200])
        img.save(subdir+'\\'+ file,img.format)
        img.close()
        


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



