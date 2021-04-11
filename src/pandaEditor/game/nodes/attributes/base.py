from utils.functions import GetLowerCamelCase


class Base:
    
    def __init__(
        self,
        label,
        type_=None,
        getFn=None,
        setFn=None,
        srcFn=None,
        getArgs=None,
        setArgs=None,
        srcArgs=None,
        w=True,
        srcComp=None,
        parent=None,
        initDefault=None,
        initName=None,
    ):
        self.label = label
        self.type = type_
        self.getFn = getFn
        self.setFn = setFn
        self.srcFn = srcFn
        self.getArgs = getArgs or []
        self.setArgs = setArgs or []
        self.srcArgs = srcArgs or []
        self.w = w
        
        self.srcComp = srcComp
        self.parent = parent
        
        self.initDefault = initDefault
        self.initName = initName
        
        name = self.label.replace(' ', '')
        self.name = GetLowerCamelCase(name)
        
        if initName is None:
            initName = self.name
        self.initName = initName
        
    def GetSource(self):
        if self.srcFn is None:
            src = self.srcComp
        else:
            args = self.srcArgs[:]
            args.insert(0, self.srcComp)
            src = self.srcFn(*args)
            
        return src
        
    def Get(self):
        args = self.getArgs[:]
        args.insert(0, self.GetSource())
        return self.getFn(*args)
    
    def Set(self, val):
        args = self.setArgs[:]
        args.insert(0, self.GetSource())
        args.append(val)
        return self.setFn(*args)