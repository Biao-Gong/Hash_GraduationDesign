#!/usr/bin/python
import pickle
from datetime import datetime

import numpy as np
import time
import torch
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import sys
sys.path.append('./nets')
import basicnet1
def main():

    basicpath = '/var/www/hash/2018-04-22T08:26:34.688274_easyfinal'
    hashcodesavepath = '/var/www/hash/2018-04-25T05_17_30.698582_lablesandcodes'

    thebasicnet = basicnet1.makebasicnet()
    thebasicnet.load_state_dict(torch.load(basicpath,map_location=lambda storage, loc: storage))

    transform = transforms.Compose([
        transforms.Resize((32,32)),
        transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
     ])

    with open(hashcodesavepath,'rb') as f:
        d=pickle.load(f)
    
    codes=np.array(d['codes'])
    labels=np.array(d['labels'])

    try:
        im=Image.open("./testing/"+sys.argv[1])
        #argv0是文件名 1传入图片名 2传入用户名
    except FileNotFoundError:
        sys.exit(0)
    
    start=time.time()
    #cal code
    inputs=Variable(transform(im))
    inputs=inputs.view(1,inputs.data.shape[0],inputs.data.shape[1],inputs.data.shape[2])
    outputs=torch.sign(thebasicnet(inputs))+1
    outputs=outputs.data.numpy().astype(np.bool)
    #计算哈希码的时间
    print(time.time()-start)  

    #show hashcode
    hashcode=""
    for i in outputs[0]:
        if i:
            hashcode+='1'
        else:
            hashcode+='0'
    #哈希码字符串
    print(hashcode)

    start=time.time()
    distance=np.sum((outputs^codes),axis=1)
    result=labels[np.where(distance==0)]
    #距离比较的时间
    print(time.time()-start)

    count=[0,0,0,0,0,0,0,0,0,0]
    la=['arpln','atmble','bird','cat','deer','dog','frog','horse','ship','truck']
    count[0]=np.where(result==0)[0].shape[0]
    count[1]=np.where(result==1)[0].shape[0]
    count[2]=np.where(result==2)[0].shape[0]
    count[3]=np.where(result==3)[0].shape[0]    
    count[4]=np.where(result==4)[0].shape[0]
    count[5]=np.where(result==5)[0].shape[0]
    count[6]=np.where(result==6)[0].shape[0]
    count[7]=np.where(result==7)[0].shape[0]
    count[8]=np.where(result==8)[0].shape[0]
    count[9]=np.where(result==9)[0].shape[0]
    fig = plt.figure(1)  
    ax  = fig.add_subplot(111) 
    ax.bar(la,count,0.5,color='green',)
    ax.set_title('within Hamming radius 0', bbox={'facecolor':'0.8', 'pad':5})
    ax.set_xlabel('classes')  
    ax.set_ylabel('count')  
    plt.grid(True,linestyle = "--")
    plt.savefig("./result/"+sys.argv[2]+'.jpg')

if __name__ == '__main__':
    main()
