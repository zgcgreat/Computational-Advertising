
class enumCounter:
    _abc={}
    _name=''

    def __init__(self,name):
        self._abc={}
        self._name=name
    def count(self,enum):
        if enum=='': return
        if self._abc.get(str(enum)) == None:
            self._abc[enum]=1
        else:
            self._abc[enum]+=1


    def showCount(self):

        print('{0} : {1}'.format(self._name,len(self._abc)))
        # for k in self._abc:
        #     print('{0} : {1}'.format(k,self._abc[k]))

    def getDetail(self):
        for k in self._abc:
            print('{0} : {1}'.format(k,self._abc[k]))



