#!/usr/bin/env python
# -*- coding:utf-8 -*-

#输入的是有时间戳的真值和估计值，根据时间戳的比值估计真值
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


if __name__ == "__main__":
    groundtruthFile="stamped_groundtruth.txt"
    estimateFile="stamped_traj_estimate.txt"
    sr=get_sr(groundtruthFile,estimateFile)
    
