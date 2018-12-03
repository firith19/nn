# -*- coding: utf-8 -*-
from selenium import webdriver
from datetime import timedelta, date

'''
Parses the page source to take out the document URLs
'''
def extractDocumentUrlsFromPageSource(source, url_template, f):
    source_lines = source.split('\n')
    for line in source_lines:
        if url_template in line:
            url = line.split('https://')[1].split('\' class')[0]
            print >> f, 'https://' + url

'''
Iterates through dates, queries and then iterates through subpages of the query to get all the document links
'''
def searchByDate(start_date, end_date, f):
    for n in range(int ((end_date - start_date).days)):
        temp_date = (start_date + timedelta(n)).strftime("%d.%m.%Y")
        print(temp_date)
        # get first page
        driver.get('https://eojn.nn.hr/SPIN/application/ipn/PreglediFrm.aspx?method=ReducedObjavljeniDokumenti')
        js = 'document.getElementById(\'uiFilter_Calendar_DatumObjave_textBox\').value=\'' + temp_date + '\';document.getElementById(\'uiFilterSearch\').click();'
        result = driver.execute_script(js)
        extractDocumentUrlsFromPageSource(driver.page_source,'https://eojn.nn.hr/SPIN/APPLICATION/IPN/DocumentManagement/DokumentPodaciFrm.aspx?', f)
        for i in range(2,20):
            js = "__doPostBack('uiView$gridResults$ctl14$ctl" + str(i).zfill(2) + "','')".replace("document.write",
                                                                                                  "return ")
            result = driver.execute_script(js)
            extractDocumentUrlsFromPageSource(driver.page_source,
                                              'https://eojn.nn.hr/SPIN/APPLICATION/IPN/DocumentManagement/DokumentPodaciFrm.aspx?', f)


options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path='C:/Users/ematdin/Downloads/chromedriver.exe' , chrome_options=options)

f = open('links.txt', 'w')

#searchByDate(date(2008,1,4), date(2018,11,22), f)
searchByDate(date(2012,11,19), date(2018,11,22), f)

driver.quit()
