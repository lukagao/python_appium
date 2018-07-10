#encoding=utf-8
from appium import webdriver  
from inspect import isfunction
from openpyxl import Workbook
import datetime
import threading
import time
class BaseTest(object):
    platformName=None
    platformVersion=None
    deviceName=None
    appPackage=None
    appActivity=None
    noReset='true'
    server_url='http://localhost:4723/wd/hub'
    def __init__(self):
        self.desired_caps = {} 
        if getattr(self,'platformName'):
            self.desired_caps['platformName']=self.platformName
        else:
            raise ValueError("%s must have a platformName" % type(self).__name__)
        if getattr(self,'platformVersion'):
            self.desired_caps['platformVersion']=self.platformVersion
        else:
            raise ValueError("%s must have a platformVersion" % type(self).__name__)
        if getattr(self,'deviceName'):
            self.desired_caps['deviceName']=self.deviceName
        else:
            raise ValueError("%s must have a deviceName" % type(self).__name__)
        if getattr(self,'appPackage'):
            self.desired_caps['appPackage']=self.appPackage
        else:
            raise ValueError("%s must have a appPackage" % type(self).__name__)
        if getattr(self,'appActivity'):
            self.desired_caps['appActivity']=self.appActivity
        else:
            raise ValueError("%s must have a appActivity" % type(self).__name__)
        self.desired_caps['noReset']=self.noReset
        self.driver = webdriver.Remote(self.server_url, self.desired_caps) 
        print BaseTest.__subclasses__()
    
    def getDriver(self):
        return self.driver
    
    def down(self):
        print 'down'
        self.driver.quit()


def BaseRun(func):
    def inner(self):
        print 'start:'
        func(self)
    return inner


def runLoop(caseNum,caseList,loop,globalLoop,sheet):
    testCase=caseList[caseNum]
    tc=testCase()
    caseID=testCase.__name__
    appPackage=testCase.appPackage
    platformName=testCase.platformName
    platformVersion=testCase.platformVersion
    failTimes=0
    failReason=''
    for i in range(loop):  
        loops=i   
        for item in testCase.__dict__.values():
            if isfunction(item):
                if item.__name__!='tearDown':
                    try:
                        item(tc)
                    except Exception as e:
                        failTimes+=1
                        failReason+=str(e)
                        tc.tearDown()
                        tc.__init__()
    tc.tearDown()
    result=[caseID,appPackage,platformName,platformVersion,(loops+1)*globalLoop,failTimes,failReason]
    for x in range(len(result)):
        if result[x]==failTimes:
            originFailTimes=sheet.cell(row=caseNum+2,column=x+1).value
            if(originFailTimes):
                originFailTimes=int(originFailTimes)
            else:
                originFailTimes=0
                
            sheet.cell(row=caseNum+2,column=x+1,value=result[x]+originFailTimes)   
        else:
            sheet.cell(row=caseNum+2,column=x+1,value=result[x])      
    
def runTest(caseList,loop=2,globalLoop=2,multiRun=False): 
    colum=['caseID','appPackage','platformName','platformVersion','loops','failTimes','failReason']
    try:
        wb=Workbook()
        filename=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")+'.xlsx'
        sheet=wb.active
        sheet.title='result'
        for x in range(len(colum)):
            sheet.cell(row=1,column=x+1,value=colum[x])
        for n in range(globalLoop):
            for caseNum in range(len(caseList)):        
                if(not multiRun):
                    runLoop(caseNum,caseList,loop,n+1,sheet)
                else:
                    print "start thread %s" % str(caseNum)
                    t=threading.Thread(target=runLoop,args=(caseNum,caseList,loop,n+1,sheet))
                    t.start()
                    #time.sleep(20)
                    #t.join()
            if(multiRun):
                for t in threading.enumerate():
                    if type(t)==threading.Thread:
                        t.join(60)
    except Exception as e:
        print e
    finally:  
        wb.save(filename)