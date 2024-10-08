json_file = "./Feb142024/data/FormbookExtracted"
#json_file = '/media/matt/Data/data/Maze'
import os
import json
#you need to add you path here
with open(os.path.join(json_file, 'e58db2a0ff5965c97eeb52a3342e5a4ec06ff9d6beafbd7007e14368c5af64a4.json'), 'r',
          encoding='utf-8') as f1:
    ll = [line for line in f1.readlines()]

    #this is the total length size of the json file
    print(len(ll))

    
    size_of_the_split=200000
    total = len(ll) // size_of_the_split

    #in here you will get the Number of splits
    print(total+1)

    for i in range(len(ll)):
        if i % size_of_the_split ==0:
            if i != 0:
                file.close()
            file = open(json_file+"1M"+str(i+1)+".json",'w')
        file.write(str(ll[i]))
    file.close()
