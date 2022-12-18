from math import floor

class analysisGenerator:
    def __init__(self,lifeNum):
        self.lifeNum = lifeNum

    def analysis(self):
        lifeNumSum = floor(self.lifeNum/10)+int(self.lifeNum%10)
        nine_pesonality = ["執行者","邏輯家","花蝴蝶","家裡蹲","組織者",
        "慈善家","冒險家","生意人","理想家"]
        print(lifeNumSum)
        for i in range(9):
            if lifeNumSum==i:
                comment = "你的生命靈數是{lifeNum},你是一個{pesonality}".format(lifeNum=lifeNumSum,pesonality=nine_pesonality[i-1])
        return comment

if __name__=="__main__":
    print(analysisGenerator.analysis(32))