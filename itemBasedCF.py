import numpy as np
import math
from DB import MyDB

class ItemBasedCF:
    def __init__(self,train_file,test_file):
        self.train_file = train_file
        self.test_file = test_file
        self.readData()

    def readData(self):
        mydb=MyDB()
        res=mydb.getAllScore()
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
        return self.W

    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=3,N=10):
        rank = dict()
        action_item = self.train[user]     #用户user产生过行为的item和评分
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
                # rank[i] += wuv * rvi
                # rank[I] = rank[I] / sim_sum
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])

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
    itemBasedCF=ItemBasedCF('train.data','test.data')
    itemBasedCF.ItemSimilarity()
    print(itemBasedCF.Recommend(6))
    # print(itemBasedCF.RecallAndPrecision())
    # print(itemBasedCF.Coverage())
    # print(itemBasedCF.Popularity())