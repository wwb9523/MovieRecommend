import numpy as np
import math
from DB import MyDB
import math,pickle
from cluster import Cluster
import pickle,os,sys

class ItemBasedCF:
    def __init__(self):
        pass

    def readData(self):
        mydb=MyDB()
        res=mydb.getAllScore()
        mydb.db.close()
        ce=int(len(res)*3/4)
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        for line in res[:ce]:
            user,item,score = line
            self.train.setdefault(user,{})
            self.train[user][item] = int(score)
        self.test = dict()      #测试集
        for line in res[ce:]:
            user,item,score = line
            self.test.setdefault(user,{})
            self.test[user][item] = int(score)

    def ItemSimilarity(self):
        self.readData()
        #建立物品-物品的共现矩阵
        C = dict()  #物品-物品的共现矩阵
        N = dict()  #物品被多少个不同用户购买
        for user,items in self.train.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i] += 1
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j : continue
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        print(os.path.split(os.path.realpath(__file__))[0])
        pkl='pkl/itemSim.pkl'
        output = open(pkl, 'wb')
        pickle.dump(self, output)
        output.close()
        return self.W

    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=100,N=30):
        cluster=Cluster()
        rank = dict()
        length=dict()
        if user not in self.train:
            res=cluster.recommend()
            return res
        else:
            action_item = self.train[user]  # 用户user产生过行为的item和评分
            for item,score in action_item.items():
                if item > 1000:
                    continue
                cluster_recom = cluster.recommend(item, 10)
                for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[:100]:
                    if j in action_item.keys():
                        continue
                    if j not in cluster_recom:
                        continue
                    rank.setdefault(j,0)
                    rank[j] += score * wj
                    length.setdefault(j,0)
                    length[j]=length[j]+wj
            for item,score in rank.items():
                rank[item]=rank[item]/length[item]
        res=dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[:30])
        return res

    def rmse(self):
        n=m=0
        for user in self.test.keys():
            rank=self.Recommend(user)
            for i,score in rank.items():
                if i in self.test[user]:
                    x=self.test[user][i]-score
                    m=m+math.pow(x,2)
                    n=n+1
        res=math.sqrt(m/n)
        return res

    # 召回率和准确率
    def RecallAndPrecision(self, train=None, test=None, K=3, N=10):
        train = train or self.train
        test = test or self.test
        hit = 0
        recall = 0
        precision = 0
        for user in train.keys():
            tu = test.get(user, {})
            rank = self.Recommend(user, K=K, N=N)
            for i, _ in rank.items():
                if i in tu:
                    hit += 1
            recall += len(tu)
            precision += N
        recall = hit / (recall * 1.0)
        precision = hit / (precision * 1.0)
        return (recall, precision)

    # 覆盖率
    def Coverage(self, train=None, test=None, K=3, N=10):
        train = train or self.train
        recommend_items = set()
        all_items = set()
        for user, items in train.items():
            for i in items.keys():
                all_items.add(i)
            rank = self.Recommend(user, K)
            for i, _ in rank.items():
                recommend_items.add(i)
        return len(recommend_items) / (len(all_items) * 1.0)

    # 新颖度
    def Popularity(self, train=None, test=None, K=3, N=10):
        train = train or self.train
        item_popularity = dict()
        # 计算物品流行度
        for user, items in train.items():
            for i in items.keys():
                item_popularity.setdefault(i, 0)
                item_popularity[i] += 1
        ret = 0  # 新颖度结果
        n = 0  # 推荐的总个数
        for user in train.keys():
            rank = self.Recommend(user, K=K, N=N)  # 获得推荐结果
            for item, _ in rank.items():
                ret += math.log(1 + item_popularity[item])
                n += 1
        ret /= n * 1.0
        return ret

if __name__=='__main__':
    #pkl='pkl/clf1000_4_11309989.1559.pkl'
    itemBasedCF=ItemBasedCF()
    itemBasedCF.ItemSimilarity()
    #print(itemBasedCF.rmse())
    print(itemBasedCF.Recommend(6))
    # print(itemBasedCF.RecallAndPrecision())
    # print(itemBasedCF.Coverage())
    # print(itemBasedCF.Popularity())