#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020 Carnegie Mellon University, Wenshan Wang <wenshanw@andrew.cmu.edu>
# For License information please see the LICENSE file in the root directory.
import math
import numpy as np
from evaluator_base import ATEEvaluator, RPEEvaluator, KittiEvaluator, transform_trajs, quats2SEs
from os.path import isdir, isfile
from data_prepare import writeTimeStamp2PoseGt,get_sr,get_match_list,get_match_pose,get_gt_est_file,get_gt_timeLength,get_est_file_timelength

# from trajectory_transform import timestamp_associate

class TartanAirEvaluator:
    def __init__(self, scale = False, round=1):
        self.ate_eval = ATEEvaluator()
        self.rpe_eval = RPEEvaluator()
        self.kitti_eval = KittiEvaluator()
        
    def evaluate_one_trajectory(self, gt_traj_name, est_traj_name, scale=False):
        """
        scale = True: calculate a global scale
        """
        # load trajectories
        gt_traj = np.loadtxt(gt_traj_name)
        est_traj = np.loadtxt(est_traj_name)

        if gt_traj.shape[0] != est_traj.shape[0]:
            raise Exception("POSEFILE_LENGTH_ILLEGAL")
        if gt_traj.shape[1] != 7 or est_traj.shape[1] != 7:
            raise Exception("POSEFILE_FORMAT_ILLEGAL")

        # transform and scale
        gt_traj_trans, est_traj_trans, s = transform_trajs(gt_traj, est_traj, scale)
        gt_SEs, est_SEs = quats2SEs(gt_traj_trans, est_traj_trans)

        ate_score, gt_ate_aligned, est_ate_aligned = self.ate_eval.evaluate(gt_traj, est_traj, scale)
        rpe_score = self.rpe_eval.evaluate(gt_SEs, est_SEs)#(rot_error_mean, trans_error_mean)
        kitti_score = self.kitti_eval.evaluate(gt_SEs, est_SEs)#np.mean(rot), np.mean(tra)

        return {'ate_score': ate_score, 
                'rpe_score': rpe_score, 
                'kitti_score': kitti_score}

if __name__ == "__main__":
    
    # scale = True for monocular track, scale = False for stereo track
    aicrowd_evaluator = TartanAirEvaluator()
    groundtruthFile,estimateFileList= get_gt_est_file()#estimateFileList是一个数组，有5个文件
    #groundtruthFile='pose_left.txt'
    #输入的是tartanair(有或)没有时间戳的pose_left.txt文件，和tum格式(time tx ty tz qx qy qz qw)的estimate_traj文件
    writeTimeStamp2PoseGt(groundtruthFile)#为groundtruth写时间戳
    #SR=get_sr(groundtruthFile,estimateFile)#利用两个的时间戳计算sr
    gt_time_length= get_gt_timeLength(groundtruthFile)
    result_dict_list=[]
    for estimateFile in estimateFileList:
        est_time_length=get_gt_timeLength(estimateFile)
        if abs(est_time_length-0.0)<0.01:#完全没有跟上的
            continue
        gt_pose_file,est_pose_file=get_match_pose(groundtruthFile,estimateFile)#将gt和est文件生成pose_gt.txt,pose_est.txt，并且里面的位姿一一对应
        result = aicrowd_evaluator.evaluate_one_trajectory(gt_pose_file, est_pose_file, scale=True)
        result['sr']=est_time_length/gt_time_length
        with open('result.txt',"a+") as f:
            f.write(estimateFile)
            f.write('\n')
            for key in result:
                f.write(str(key)+": "+str(result[key])+'\n')#如果一个score有两个数据，则前者表示旋转平均误差，后者表示平移平均误差
            f.write('\n\n\n')
        #print(result)
        result_dict_list.append(result)
    kitti_score_rot=0.0
    kitti_score_trans=0.0
    rpe_score_rot=0.0
    rpe_score_trans=0.0
    ate_score=0.0
    sr=0.0
    nan_time=0#无效数据的个数
    with open('result.txt',"a+") as f:#将所有的值都计算一个平均值
        for result in result_dict_list:
            for key in result:
                if str(key)=="kitti_score":
                    if math.isnan(float(list(result[key])[0])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break
                    if math.isnan(float(list(result[key])[1])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break
                if str(key)=="rpe_score":
                    if math.isnan(float(list(result[key])[0])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break
                    if math.isnan(float(list(result[key])[1])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break
  
                if str(key)=="ate_score":
                    if math.isnan(float(result[key])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break
                if str(key)=="sr":
                    if math.isnan(float(result[key])):
                        nan_time+=1
                        print("HAVE AN NAN DATA")
                        break

                if str(key)=="kitti_score":
                    kitti_score_rot=kitti_score_rot+float(list(result[key])[0])
                    kitti_score_trans=kitti_score_trans+float(list(result[key])[1])
                if str(key)=="rpe_score":
                    rpe_score_rot=rpe_score_rot+float(list(result[key])[0])
                    rpe_score_trans=rpe_score_trans+float(list(result[key])[1])
                if str(key)=="ate_score":
                    ate_score=ate_score+float(result[key])
                if str(key)=="sr":
                    sr=sr+float(result[key])

        kitti_score_rot=kitti_score_rot/(len(result_dict_list)-nan_time)
        kitti_score_trans=kitti_score_trans/(len(result_dict_list)-nan_time)
        rpe_score_rot=rpe_score_rot/(len(result_dict_list)-nan_time)
        rpe_score_trans=rpe_score_trans/(len(result_dict_list)-nan_time)
        ate_score=ate_score/(len(result_dict_list)-nan_time)
        sr=sr/(len(result_dict_list)-nan_time)

        av_kitti_score=[kitti_score_rot,kitti_score_trans]
        av_rpe_score=[rpe_score_rot,rpe_score_trans]
        av_ate_score=ate_score
        
        new_result={}
        new_result["average_kitti_score"]=av_kitti_score
        new_result["average_rpe_score"]=av_rpe_score
        new_result["average_ate_score"]=av_ate_score
        new_result["average_sr"]=sr

        with open('result.txt',"a+") as f:
            f.write('\n\n')
            f.write("average score:\n")
            for key in new_result:
                f.write(str(key)+": "+str(new_result[key])+'\n')#如果一个score有两个数据，则前者表示旋转平均误差，后者表示平移平均误差
        print(new_result)
            
     

            

