#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

#函数输出groundtruthFile和estimateFile
def get_gt_est_file():
    path=os.getcwd()#获取执行命令的文件夹位置
    groundtruthFile='pose_gt.txt'
    estimateFile=[]
    files= os.listdir(path) #得到文件夹下的所有文件名称
    has_gt_file=False
    for file in files:
        if file==groundtruthFile:
            has_gt_file=True
    if has_gt_file==False:
        print("has no pose_gt.txt")
        exit()
    
    #找出其他的txt文件，如果文件夹没有两个txt文件，输出false
    txt_num=0
    txt_file_list=[]
    for  file in files:
        file_list=file.split('.')
        if file_list[-1]=='txt':
            txt_num=txt_num+1
            txt_file_list.append(file)

    if txt_num!=2:
        print('not have 2 txt file')
        exit()
    if txt_file_list[0]==groundtruthFile:
        estimateFile=txt_file_list[1]
    else:
        estimateFile=txt_file_list[0]
    
    return groundtruthFile,estimateFile

    

    
    

if __name__ == "__main__":
    gt,est=get_gt_est_file()
    print(gt,est)
