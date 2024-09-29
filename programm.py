class Extract:
    def __init__(self,l,l1):
        self.l = l
        self.l1 = l1

    def display(self):
        d = dict(zip(self.l,self.l1))
        return d


s = Extract(["Abhaya","Srikant"],[10,20])
result = s.display()
print(result)