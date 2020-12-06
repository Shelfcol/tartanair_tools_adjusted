
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


if __name__ == "__main__":
    filename="pose_gt.txt"
    writeTimeStamp2PoseGt(filename)

