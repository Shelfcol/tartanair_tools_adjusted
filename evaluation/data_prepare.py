#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

#函数输出groundtruthFile和estimateFileList的名字，这里groundtruthFile的名字必须为pose_gt.txt,里面有5个估计轨迹，1个真实轨迹
def get_gt_est_file():
    path=os.getcwd()#获取执行命令的文件夹位置
    groundtruthFile='pose_left.txt'
    files= os.listdir(path) #得到文件夹下的所有文件名称
    has_gt_file=False
    for file in files:
        if file==groundtruthFile:
            has_gt_file=True
    if has_gt_file==False:
        print("has no pose_left.txt")
        exit()
    
    #找出其他的txt文件，如果文件夹没有两个txt文件，输出false
    txt_num=0
    txt_file_list=[]
    for  file in files:
        file_list=file.split('.')
        if file_list[-1]=='txt':
            txt_num=txt_num+1
            txt_file_list.append(file)

    if txt_num!=6:
        print('not have 6 txt file')
        exit()
    estimateFileList=[]
    for file in txt_file_list:
        if file!=groundtruthFile:
            #print(file)
            estimateFileList.append(file)
    if len(estimateFileList)!=5:
        print("not have 5 estimate file")
        exit()

    return groundtruthFile,estimateFileList





#给tartanair数据集的真值加时间戳,如果已经有时间戳，就不会加
#input pose_gt.txt includes:      tx ty tz qx qy qz qw
#output                      time tx ty tz qx qy qz qw
def writeTimeStamp2PoseGt(filename):
    with open(filename, "r") as f_read:
        content=f_read.readlines()
    split_list=content[0].split(' ')

    if len(split_list)==8:
        return
    time_now=0.0
    deltaT=0.1
    fileData=""
    for line in content:
        timeStr=str(time_now)
        time_now=time_now+deltaT
        fileData=fileData+timeStr+" "+line
    with open(filename,"w") as f:
        f.write(fileData)

#输入的是有时间戳的真值和估计值，根据时间戳的比值估计真值，这个是原始的轨迹文件，还没有进行对应的匹配
def get_sr(groundtruthFile,estimateFile):
    with open(groundtruthFile, "r") as f_read:
        content_gt=f_read.readlines()
    with open(estimateFile, "r") as f_read:
        content_est=f_read.readlines()    

    gt_list_start=content_gt[0].split(' ')
    gt_list_end=content_gt[-1].split(' ')
    if len(gt_list_start)!=8:
        print("not right ")
        return
    gt_start=float(gt_list_start[0])
    gt_end=float(gt_list_end[0])

    est_list_start=content_est[0].split(' ')
    est_list_end=content_est[-1].split(' ')
    if len(est_list_start)!=8:
        print("not right ")
        return
    est_start=float(est_list_start[0])
    est_end=float(est_list_end[0])
    #print(gt_start,gt_end,est_start,est_end)
    sr=(est_end-est_start)/(gt_end-gt_start)
    print(sr)
    return sr

#获取文件的time长度,这是的file是加了时间戳的
def get_time_length(file):
    with open(file, "r") as f_read:
        content_gt=f_read.readlines()
    list_start=content_gt[0].split(' ')
    list_end=content_gt[-1].split(' ')
    if len(list_start)!=8:
        print("not right ")
        exit()
    start=float(list_start[0])
    end=float(list_end[0])
    time_length=end-start
   
    print(time_length)
    return time_length


#输入的是有时间戳的真值和估计值，根据时间戳的比值估计真值，这个是原始的轨迹文件，还没有进行对应的匹配
def get_gt_timeLength(groundtruthFile):
    with open(groundtruthFile, "r") as f_read:
        content_gt=f_read.readlines()
    if len(content_gt)==0:
        return 0.0

    gt_list_start=content_gt[0].split(' ')
    gt_list_end=content_gt[-1].split(' ')
    if len(gt_list_start)!=8:
        print("not right ")
        return
    gt_start=float(gt_list_start[0])
    gt_end=float(gt_list_end[0])

    return gt_end-gt_start

#获取sr_evaluate/文件夹里面的5个文件的timelength的平均值
def get_est_file_timelength():
    path=os.getcwd()#获取执行命令的文件夹位置
    files= os.listdir(path+"/sr_evaluate/") #得到文件夹下的所有文件名称
    
    #找出其他的txt文件，如果文件夹没有两个txt文件，输出false
    txt_num=0
    txt_file_list=[]
    for  file in files:
        file_list=file.split('.')
        if file_list[-1]=='txt':
            txt_num=txt_num+1
            txt_file_list.append(file)

    if txt_num!=5:
        print('not have 5 txt file')
        exit()
    time=0.0
    num=0
    for txt_file in txt_file_list:
        time=time+get_time_length(txt_file)
        num=num+1
    average_time=time/num
    return average_time


def get_match_list(groundtruthFile,estimateFile):
    with open(groundtruthFile, "r") as f_read:
        content_gt=f_read.readlines()
    with open(estimateFile, "r") as f_read:
        content_est=f_read.readlines()    
    #判断数据格式是否合法
    gt_list=content_gt[0].split(' ')
    if len(gt_list)!=8:
        print("not right ")
        return
    est_list=content_est[0].split(' ')
    if len(est_list)!=8:
        print("not right ")
        return

    gt_time_list=[]
    est_time_list=[]
    for line in content_gt:
        gt_time_list.append(float(line.split(' ')[0]))

    for line in content_est:
        est_time_list.append(float(line.split(' ')[0]))

    #为每个est的time在gt的time找一个最接近的时间
    gt_list_order_num=[]
    est_list_order_num=[]
    gt_start=0
    for est_i in range(0,len(est_time_list)):
        min_time_dist=1000
        min_time_order_num=0
        for gt_i in range(gt_start,len(gt_time_list)):
            if abs(gt_time_list[gt_i]-est_time_list[est_i])<min_time_dist:
                min_time_dist=abs(gt_time_list[gt_i]-est_time_list[est_i])
                min_time_order_num=gt_i
        if min_time_dist<0.1:
            gt_list_order_num.append(min_time_order_num)
            est_list_order_num.append(est_i)
    
    #for i in range(len(est_list_order_num)):
        #print(gt_list_order_num[i],est_list_order_num[i])

    return est_list_order_num,gt_list_order_num



# two output file:  tx ty tz qx qy qz qw
def get_match_pose(groundtruthFile,estimateFile):
    #matchList序号从0开始

    gt_list=[]#groundtruth.txt在match中匹配上的序列号
    est_list=[]#stamped_traj_estimate.txt在match中匹配上的序列号

    est_list, gt_list=get_match_list(groundtruthFile,estimateFile)


    with open(groundtruthFile, "r") as f_read:
        Gt_content=f_read.readlines()    

    with open(estimateFile, "r") as f_read:
        Est_content=f_read.readlines() 

    new_Gt_data=""
    new_Est_data=""

    for i in gt_list:
        new_line=Gt_content[i].split()
        for i in range(len(new_line)):
            if i==0:
                continue
            if i<len(new_line)-1:
                new_Gt_data=new_Gt_data+new_line[i]+" "
            else:
                new_Gt_data=new_Gt_data+new_line[i]+'\n'
    #print(len(Gt_content[0].split()))
    for i in est_list:
        new_line=Est_content[i].split()
        for i in range(len(new_line)):
            if i==0:
                continue
            if i<len(new_line)-1:
                new_Est_data=new_Est_data+new_line[i]+" "
            else:
                new_Est_data=new_Est_data+new_line[i]+'\n'

    est_file_list=estimateFile.split('.')

    #print(est_file_list[0])
    NewGtfilePath=est_file_list[0]+"pose_gt.txt"
    NewEstfilePath=est_file_list[0]+"_pose_est.txt"

    with open(NewGtfilePath,"a+") as f:
        f.write(new_Gt_data)
            
    with open(NewEstfilePath,"a+") as f:
        f.write(new_Est_data)
    return NewGtfilePath,NewEstfilePath
