#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Copyright (c) 2020 Carnegie Mellon University, Wenshan Wang <wenshanw@andrew.cmu.edu>
# For License information please see the LICENSE file in the root directory.

import numpy as np
from evaluator_base import ATEEvaluator, RPEEvaluator, KittiEvaluator, transform_trajs, quats2SEs
from os.path import isdir, isfile
from data_prepare import writeTimeStamp2PoseGt,get_sr,get_match_list,get_match_pose,get_gt_est_file

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
    groundtruthFile,estimateFile= get_gt_est_file()
    #groundtruthFile='pose_left.txt'
    #输入的是tartanair(有或)没有时间戳的pose_left.txt文件，和tum格式(time tx ty tz qx qy qz qw)的estimate_traj文件
    writeTimeStamp2PoseGt(groundtruthFile)#为groundtruth写时间戳
    SR=get_sr(groundtruthFile,estimateFile)#利用两个的时间戳计算sr
    get_match_pose(groundtruthFile,estimateFile)#将gt和est文件生成pose_gt.txt,pose_est.txt，并且里面的位姿一一对应
    result = aicrowd_evaluator.evaluate_one_trajectory('pose_gt.txt', 'pose_est.txt', scale=True)
    result['sr']=SR
    with open('result.txt',"a+") as f:
        for key in result:
            f.write(str(key)+": "+str(result[key])+'\n')#如果一个score有两个数据，则前者表示旋转平均误差，后者表示平移平均误差
    print(result)
