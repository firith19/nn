# -*- coding: utf-8 -*-
from selenium import webdriver
from time import sleep
from tables import Dokument, Dokument_download, Dokument_dokument, init_db
import tables
from bs4 import BeautifulSoup
from datetime import datetime
import re


def setup_webdriver():
    download_folder = 'C:/Users/ematdin/PycharProjects/nn_javne_nabave/documents'
    '''
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    profile = {"plugins.plugins_list": [{"enabled": False,
                                             "name": "Chrome PDF Viewer"}],
                   "download.default_directory": download_folder,
                   "download.prompt_for_download": False,
                   "pdfjs.disabled": True
               }
    options.add_experimental_option("prefs", profile)
    driver = webdriver.Chrome(executable_path='C:/Users/ematdin/Downloads/downloads/chromedriver.exe' , chrome_options=options)
    '''

    """ Setup Firefox profile preferences and go get em"""
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', download_folder)
    profile.set_preference('browser.download.folderList', 1)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
    profile.set_preference("pdfjs.disabled", True)
    profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    driver = webdriver.Firefox(firefox_profile=profile,executable_path='C:/Users/ematdin/Downloads/downloads/geckodriver.exe')
    return driver

def scrape_document_web_data(url, source, session):
    ime_dokumenta = ''
    soup = BeautifulSoup(source, 'lxml')

    new_document_dictionary = {}
    new_document_dictionary['nn_id'] = int(url.split('=')[1])


    for link in soup.find_all('span'):
        if link.get('id') == 'uiDokumentPodaci_uiBrojObjave':
            new_document_dictionary['oznaka_broj'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiNaslov':
            new_document_dictionary['naziv'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiVrstaObjave':
            new_document_dictionary['vrsta_dokumenta'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiVrstaUgovora':
            new_document_dictionary['vrsta_ugovora'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiCpv':
            new_document_dictionary['cpv'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiVrstaPostupka':
            new_document_dictionary['vrsta_postupka'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiRokZaDostavuVrijeme':
            new_document_dictionary['rok_za_dostavu_ponuda'] = datetime.strptime(link.string,'%d.%m.%Y. %H:%M')
        elif link.get('id') == 'uiDokumentPodaci_uiVerzijaZakona':
            new_document_dictionary['zakon'] = u''.join(link.string).encode('utf-8').strip()
        elif link.get('id') == 'uiDokumentPodaci_uiDatumObjave':
            for link2 in link.find_all('input'):
                if link2.get('name') == 'uiDokumentPodaci$uiDatumObjave$textBox':
                    new_document_dictionary['datum_objave'] = datetime.strptime(link2.get('value'),'%d.%m.%Y.')
        elif link.get('id') == 'uiDokumentPodaci_uiDatumSlanja':
            for link2 in link.find_all('input'):
                if link2.get('name') == 'uiDokumentPodaci$uiDatumSlanja$textBox':
                    new_document_dictionary['datum_slanja'] = datetime.strptime(link2.get('value'),'%d.%m.%Y.')
        elif link.get('id') == 'uiDokumentPodaci_uiVrstaObjave':
            new_document_dictionary['ime_dokumenta'] = u''.join(link.string).encode('utf-8').strip()

    for link in soup.find_all(id=re.compile('uiDokumentPodaci_uiVezaniDokumenti.*HyperLink1')):
        print(link)
        if 'uiDokumentPodaci_uiVezaniDokumenti_ctl' in link.get('id') and '_HyperLink1' in link.get('id'):
            povezani_dokument_id = u''.join(link.get('href').split('=')[1]).encode('utf-8').strip()
            print(povezani_dokument_id)
            if tables.does_dokument_exist({'nn_id': povezani_dokument_id}):
                new_doc_doc_dict = {'dokument1_id': nn_id, 'dokument2_id': povezani_dokument_id}
                new_document_document = Dokument_dokument(**new_doc_doc_dict)
                session.add(new_document_document)
                session.commit()

    new_document = Dokument(**new_document_dictionary)
    session.add(new_document)
    session.commit()
    return new_document_dictionary['nn_id'], new_document_dictionary['ime_dokumenta']

def saveDokumentDownloadInfo(session, nn_id, ime_dokumenta):
    new_document_download_dictionary = {}
    new_document_download_dictionary['nn_id'] = nn_id
    new_document_download_dictionary['ime_dokumenta'] = ime_dokumenta
    new_document_download = Dokument_download(**new_document_download_dictionary)
    session.add(new_document_download)
    session.commit()

driver = setup_webdriver()
session = init_db()

with open('links.txt') as f:
    lines = f.readlines()
    for link in lines:
        driver.get(link)
        # first scrape the web page
        nn_id, ime_dokumenta = scrape_document_web_data(driver.current_url, driver.page_source, session)
        # second download the pdf file
        js = 'WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("uiDokumentPodaci$uiDocumentCtl$uiOpenDocumentPdf","",true,"","",false,true))'
        result = driver.execute_script(js)
        #result = driver.find_element_by_id('uiDokumentPodaci_uiDocumentCtl_uiOpenDocumentPdf').click()
        #print(result)
        saveDokumentDownloadInfo(session, nn_id, ime_dokumenta)
        sleep(1)


driver.quit()
