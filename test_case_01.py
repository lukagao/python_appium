#encoding=utf-8
from BaseTest import BaseTest
from BaseTest import BaseRun
import time


class test_case_01(BaseTest):
    platformName='Android'
    platformVersion='6.0'
    deviceName='DWH9X17718W01627'
    appPackage='com.android.calculator2'
    appActivity='.Calculator'
    
    @BaseRun
    def test(self):
        driver = self.getDriver()       
        print driver
        time.sleep(1)
        #raise Exception('hhh')
    def test01(self):
        print 'test01'
    
    def tearDown(self):
        
        self.down()
    
   