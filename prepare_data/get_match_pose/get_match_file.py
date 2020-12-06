#!/usr/bin/env python
# -*- coding:utf-8 -*-

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
    
    for i in range(len(est_list_order_num)):
        print(gt_list_order_num[i],est_list_order_num[i])

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

    NewGtfilePath="pose_gt.txt"
    NewEstfilePath="pose_est.txt"

    with open(NewGtfilePath,"a+") as f:
        f.write(new_Gt_data)
            

    with open(NewEstfilePath,"a+") as f:
        f.write(new_Est_data)

if __name__ == "__main__":
    GtfilePath="stamped_groundtruth.txt"
    EstfilePath="stamped_traj_estimate.txt"
    get_match_pose(GtfilePath,EstfilePath)

