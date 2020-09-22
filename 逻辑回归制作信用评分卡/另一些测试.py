import pandas as pd
import numpy as np
#计算WOE和BAD RATE
#BAD RATE与bad%不是一个东西
#BAD RATE是一个箱中，坏的样本所占箱子中总样本的比例 (bad/total)
#而bad%是一个箱中的坏样本占整个特征中的坏样本的比例

def get_woe(num_bins):
    # 通过 num_bins 数据计算 woe
    columns = ["min","max","count_0","count_1"]
    df = pd.DataFrame(num_bins,columns=columns)

    df["total"] = df.count_0 + df.count_1#一个箱子当中所有的样本数
    df["percentage"] = df.total / df.total.sum()#一个箱子里的样本数，占所有样本的比例
    df["bad_rate"] = df.count_1 / df.total#一个箱子坏样本的数量占一个箱子里边所有样本数的比例
    df["good%"] = df.count_0/df.count_0.sum()
    df["bad%"] = df.count_1/df.count_1.sum()
    df["woe"] = np.log(df["good%"] / df["bad%"])
    return df

#计算IV值
def get_iv(df):
    rate = df["good%"] - df["bad%"]
    iv = np.sum(rate * df.woe)
    return iv
num_bins = [(21.0, 28.0, 4243, 7524),
 (28.0, 31.0, 3571, 5901),
 (31.0, 34.0, 4075, 6756),
 (34.0, 36.0, 2908, 4609),
 (36.0, 39.0, 5182, 7518),
 (39.0, 41.0, 3956, 5852),
 (41.0, 43.0, 4002, 5672),
 (43.0, 45.0, 4389, 5984),
 (45.0, 46.0, 2419, 3295),
 (46.0, 48.0, 4813, 6153),
 (48.0, 50.0, 4900, 6239),
 (50.0, 52.0, 4728, 5802),
 (52.0, 54.0, 4681, 5003),
 (54.0, 56.0, 4677, 4014),
 (56.0, 58.0, 4483, 3443),
 (58.0, 61.0, 6583, 4770),
 (61.0, 64.0, 6968, 3189),
 (64.0, 68.0, 6623, 2284),
 (68.0, 74.0, 6753, 1919),
 (74.0, 107.0, 7737, 1390)]

num_bins_ = num_bins.copy() #不希望覆盖原有数据

import matplotlib.pyplot as plt
import scipy.stats

IV = []
axisx = []

while len(num_bins_) > 2:  #大于 设置的最低分箱个数
    pvs = []
    #获取 num_bins_两两之间的卡方检验的置信度（或卡方值）
    for i in range(len(num_bins_)-1):
        x1 = num_bins_[i][2:]
        x2 = num_bins_[i+1][2: ]
        # 0 返回 chi2 值，1 返回 p 值。

        try:
            scipy.stats.chi2_contingency([x1, x2])[1]
        except ValueError:
            pv = [0.1,0.1]
        else:
            pv = scipy.stats.chi2_contingency([x1, x2])[1]
            pvs.append(pv)
        # chi2 = scipy.stats.chi2_contingency([x1,x2])[0]#计算卡方值


    # 通过 p 值进行处理。合并 p 值最大的两组
    i = pvs.index(max(pvs))
    num_bins_[i:i+2] = [(
            num_bins_[i][0],
            num_bins_[i+1][1],
            num_bins_[i][2]+num_bins_[i+1][2],
            num_bins_[i][3]+num_bins_[i+1][3])]

    bins_df = get_woe(num_bins_)
    axisx.append(len(num_bins_))
    IV.append(get_iv(bins_df))

plt.figure()
plt.plot(axisx,IV)
plt.xticks(axisx)
plt.xlabel("number of box")
plt.ylabel("IV")
plt.show()
#选择转折点处，也就是下坠最快的折线点，所以这里对于age来说选择箱数为6