#!/usr/bin/env python
# -*- coding:utf-8 -*-

GtfilePath="00/stamped_groundtruth.txt"
NewGtfilePath="00/pose_gt.txt"
EstfilePath="00/stamped_traj_estimate.txt"
NewEstfilePath="00/pose_est.txt"
matchList="00/saved_results/traj_est/stamped_est_gt_matches.txt"

# two output file:  tx ty tz qx qy qz qw
def get_match_pose():
    #matchList序号从0开始
    with open(matchList, "r") as f_read:
        match_list=f_read.readlines()

    gt_list=[]#groundtruth.txt在match中匹配上的序列号
    est_list=[]#stamped_traj_estimate.txt在match中匹配上的序列号
    for line in match_list:
        new_line=line.split()
        est_list.append(int(new_line[0]))
        gt_list.append(int(new_line[1]))
    #print(gt_list[1850])
    #print(est_list[1850])

    with open(GtfilePath, "r") as f_read:
        Gt_content=f_read.readlines()    

    with open(EstfilePath, "r") as f_read:
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

    with open(NewGtfilePath,"a+") as f:
        f.write(new_Gt_data)
            

    with open(NewEstfilePath,"a+") as f:
        f.write(new_Est_data)

if __name__ == "__main__":
    get_match_pose()

