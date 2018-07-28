from test_case_01 import test_case_01
from BaseTest import runTest


caseList=[test_case_01,test_case_01]
cmds=['appium -a 0.0.0.0 -p 4723','appium -a 0.0.0.0 -p 4724','appium -a 0.0.0.0 -p 4725']

        
    
if __name__=='__main__':

    runTest(caseList,multiRun=False)  
    