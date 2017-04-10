import math

#train为训练集合，test为验证集合，给每个用户推荐N个物品

#召回率和准确率
def RecallAndPrecision(self,train=None,test=None,K=3,N=10):
    train = train or self.train
    test = test or self.test
    hit = 0
    recall = 0
    precision = 0
    for user in train.keys():
        tu = test.get(user,{})
        rank = self.Recommend(user,K=K,N=N)
        for i,_ in rank.items():
            if i in tu:
                hit += 1
        recall += len(tu)
        precision += N
    recall = hit / (recall * 1.0)
    precision = hit / (precision * 1.0)
    return (recall,precision)

#覆盖率
def Coverage(self,train=None,test=None,K=3,N=10):
    train = train or self.train
    recommend_items = set()
    all_items = set()
    for user,items in train.items():
        for i in items.keys():
            all_items.add(i)
        rank = self.Recommend(user,K)
        for i,_ in rank.items():
            recommend_items.add(i)
    return len(recommend_items) / (len(all_items) * 1.0)

#新颖度
def Popularity(self,train=None,test=None,K=3,N=10):
    train = train or self.train
    item_popularity = dict()
    #计算物品流行度
    for user,items in train.items():
        for i in items.keys():
            item_popularity.setdefault(i,0)
            item_popularity[i] += 1
    ret = 0     #新颖度结果
    n = 0       #推荐的总个数
    for user in train.keys():
        rank = self.Recommend(user,K=K,N=N)    #获得推荐结果
        for item,_ in rank.items():
            ret += math.log(1 + item_popularity[item])
            n += 1
    ret /= n * 1.0
    return ret