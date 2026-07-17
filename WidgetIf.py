# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'WidgetIf.py'
# Bytecode version: 3.9.0beta5 (3425)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import *
from PyQt6.QtWidgets import QApplication
from Ui_mainWindow import Ui_MainWindow
import traceback
import json
import sqlite3
from qthreadServer import ThreadServerQT
from languages import *
from manageLabels import *
import time
try:
    myappid = 'vne.tool.version1'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except:
    pass
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
class WidgetIf(QWidget, Ui_MainWindow):
    inserito = 0
    dovuto = 0
    resto = 0
    idPayment = '0'
    operatoreCurrent = ''
    isPagamento = False
    totRefill = 0
    idCurrent = 1
    def getDbData(self, property):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT VALORE FROM PROPERTIES WHERE NOME=\'' + str(property) + '\''
        c.execute(query)
        row = c.fetchone()
        conn.close()
        return row[0]
    def setDbData(self, property, value):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE PROPERTIES SET VALORE=\'' + str(value) + '\' WHERE NOME=\'' + str(property) + '\''
        c.execute(query)
        conn.commit()
        conn.close()
    def getDbCoins(self, moneta):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT NUMERO FROM CONTENT_COINS WHERE VALORE=' + str(moneta)
        c.execute(query)
        row = c.fetchone()
        conn.close()
        return row[0]
    def setDbCoins(self, moneta, valore):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE CONTENT_COINS SET NUMERO=' + str(valore) + ' WHERE VALORE=' + str(moneta)
        c.execute(query)
        conn.commit()
        conn.close()
    def aumentaDbCoins(self, moneta):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE CONTENT_COINS SET NUMERO=NUMERO+1 WHERE VALORE=' + str(moneta)
        c.execute(query)
        conn.commit()
        conn.close()
    def diminuisciDbCoins(self, moneta):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE CONTENT_COINS SET NUMERO=NUMERO-1 WHERE VALORE=' + str(moneta)
        c.execute(query)
        conn.commit()
        conn.close()
    def resetDbCoins(self, isFull=True):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        totale = 0
        if isFull:
            query = 'SELECT SUM(VALORE*NUMERO) FROM CONTENT_COINS WHERE 1'
            c.execute(query)
            row = c.fetchone()
            totale = int(row[0])
            query = 'UPDATE CONTENT_COINS SET NUMERO=0 WHERE 1'
            c.execute(query)
            conn.commit()
            conn.close()
        else:
            query = 'SELECT SUM(VALORE*(NUMERO-FONDOCASSA)) FROM CONTENT_COINS WHERE NUMERO>FONDOCASSA'
            c.execute(query)
            row = c.fetchone()
            if len(row) > 0:
                try:
                    totale = int(row[0])
                except:
                    pass
            query = 'UPDATE CONTENT_COINS SET NUMERO=FONDOCASSA WHERE NUMERO>FONDOCASSA'
            c.execute(query)
            conn.commit()
            conn.close()
        return totale
    def getRiciclaMonete(self, valore):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT ACCETTA FROM CONTENT_COINS WHERE VALORE=' + str(valore)
        c.execute(query)
        row = c.fetchone()
        conn.close()
        if int(row[0]) == 0:
            return False
        else:
            return True
    def getDbRecycler(self, cassetta):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT VALORE,NUMERO FROM CONTENT_RECYCLER WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
        c.execute(query)
        row = c.fetchone()
        conn.close()
        return [row[0], row[1]]
    def setDbRecycler(self, cassetta, valore):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE CONTENT_RECYCLER SET NUMERO=' + str(valore) + ' WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
        c.execute(query)
        conn.commit()
        conn.close()
    def aumentaDbRecycler(self, banconota):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT USED,CASSETTA,NUMERO,MAX_LEVEL FROM CONTENT_RECYCLER WHERE VALORE=' + str(banconota)
        c.execute(query)
        row = c.fetchone()
        if row!= None and len(row) > 0 and (int(row[0]) == 1) and (int(row[2]) < int(row[3])):
            cass = int(row[1])
            query = 'UPDATE CONTENT_RECYCLER SET NUMERO=NUMERO+1 WHERE VALORE=' + str(banconota) + ' AND USED=1 AND CASSETTA=' + str(cass)
            c.execute(query)
            conn.commit()
            conn.close()
        else:
            query = 'UPDATE STACKER_CONTENT SET NUMERO=NUMERO+1 WHERE DENOM=' + str(banconota)
            c.execute(query)
            conn.commit()
            conn.close()
            return 0
        return 1
    def diminuisciDbRecycler(self, banconota):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE CONTENT_RECYCLER SET NUMERO=NUMERO-1 WHERE VALORE=' + str(banconota) + ' AND USED=1'
        c.execute(query)
        conn.commit()
        conn.close()
    def resetDbNotes(self, isFull=True):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        totale = 0
        if isFull:
            query = 'SELECT SUM(VALORE*NUMERO) FROM CONTENT_RECYCLER WHERE USED=1'
            c.execute(query)
            row = c.fetchone()
            totale = int(row[0])
            query = 'SELECT VALORE,NUMERO FROM CONTENT_RECYCLER WHERE USED=1'
            c.execute(query)
            rows = c.fetchall()
            for elem in rows:
                query = 'UPDATE STACKER_CONTENT SET NUMERO=NUMERO+' + str(elem[1]) + ' WHERE DENOM=' + str(elem[0])
                c.execute(query)
                conn.commit()
            query = 'UPDATE CONTENT_RECYCLER SET NUMERO=0 WHERE USED=1'
            c.execute(query)
            conn.commit()
        else:
            query = 'SELECT SUM(VALORE*(NUMERO-FONDOCASSA)) FROM CONTENT_RECYCLER WHERE NUMERO>FONDOCASSA AND USED=1'
            c.execute(query)
            row = c.fetchone()
            print(row)
            if len(row) > 0:
                try:
                    totale = int(row[0])
                except:
                    pass
            query = 'SELECT VALORE,NUMERO-FONDOCASSA FROM CONTENT_RECYCLER WHERE USED=1'
            c.execute(query)
            rows = c.fetchall()
            for elem in rows:
                numStacker = int(elem[1])
                if numStacker < 0:
                    numStacker = 0
                query = 'UPDATE STACKER_CONTENT SET NUMERO=NUMERO+' + str(numStacker) + ' WHERE DENOM=' + str(elem[0])
                c.execute(query)
                conn.commit()
            query = 'UPDATE CONTENT_RECYCLER SET NUMERO=FONDOCASSA WHERE NUMERO>FONDOCASSA AND USED=1'
            c.execute(query)
            conn.commit()
        conn.close()
        return totale
    def getResult(self):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT RESP FROM WAIT_RESULT WHERE 1'
        c.execute(query)
        row = c.fetchone()
        conn.close()
        return row[0]
    def setResult(self, valore):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE WAIT_RESULT SET RESP=\'' + valore + '\' WHERE 1'
        c.execute(query)
        conn.commit()
        conn.close()
    def updateOpDone(self, tipo, valore):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT VALORE FROM REFILL WHERE TIPO=\'' + str(tipo) + '\''
        c.execute(query)
        row = c.fetchone()
        if row == None:
            query = 'INSERT INTO REFILL (TIPO,VALORE) VALUES(\'' + tipo + '\',' + str(valore) + ')'
        else:
            query = 'UPDATE REFILL SET VALORE=VALORE+' + str(valore) + ' WHERE TIPO=\'' + str(tipo) + '\''
        c.execute(query)
        conn.commit()
        conn.close()
    def cleanPayments(self):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'DELETE FROM PAGAMENTO WHERE 1'
        c.execute(query)
        conn.commit()
        query = 'UPDATE REFILL SET VALORE=0 WHERE 1'
        c.execute(query)
        conn.commit()
        conn.close()
    def getCashContent(self):
        arrayResult = []
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT VALORE,NUMERO FROM CONTENT_RECYCLER WHERE NUMERO>0 AND USED=1'
        c.execute(query)
        rows = c.fetchall()
        for elem in rows:
            arrayResult.append([elem[0], elem[1]])
        query = 'SELECT VALORE,NUMERO FROM CONTENT_COINS WHERE NUMERO>0 AND RICICLA=1'
        c.execute(query)
        rows = c.fetchall()
        for elem in rows:
            arrayResult.append([elem[0], elem[1]])
        conn.close()
        return arrayResult
    def getRestoPagamento(self, id):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT RESTO FROM PAGAMENTO WHERE ID=\'' + id + '\''
        c.execute(query)
        row = c.fetchone()
        conn.close()
        return int(row[0])
    def setJCMUsed(self, num):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        if num == 4:
            query = 'UPDATE CONTENT_RECYCLER SET USED=1 WHERE 1'
        else:
            query = 'UPDATE CONTENT_RECYCLER SET USED=0 WHERE (CASSETTA=3 OR CASSETTA=4)'
        c.execute(query)
        conn.commit()
        conn.close()
    def getArrayRecycler(self):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'SELECT DISTINCT VALORE FROM CONTENT_RECYCLER WHERE USED=1'
        c.execute(query)
        rows = c.fetchall()
        conn.close()
        array = []
        for elem in rows:
            array.append(elem[0])
        return array
    def setRimborso(self, id, isDone, refunded=0):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        if isDone:
            query = 'UPDATE PAGAMENTO SET REFUND=' + str(refunded) + ',REFUND_ON=0 WHERE ID=\'' + id + '\''
        else:
            query = 'UPDATE PAGAMENTO SET REFUND_ON=1 WHERE ID=\'' + id + '\''
        c.execute(query)
        conn.commit()
        conn.close()
    def __init__(self, parent=None):
        """\n        Constructor\n        """
        QWidget.__init__(self, parent)
        self.setupUi(self)
        # Ported: 'lang\ita' is a Windows path; on macOS the backslash is just a
        # filename character, so the file is never found. '/' works on both.
        self.lang = Languages('lang/' + str(self.getDbData('LANG')))
        currentLang = self.getDbData('LANG')
        self.labelVersione.setText('AC simulator\nversion ' + self.getDbData('VERSION'))
        setLabelLanguage(self, self.lang, currentLang)
        self.setWindowTitle('AC simulator')
        self.setWindowIcon(QIcon('pics/vnerosa.jpg'))
        self.opened = False
        self.frameMain.setVisible(True)
        self.frameImpostazioni.move(1700, 0)
        self.frameVendita.move(1200, 10)
        self.comboBoxLingua.clear()
        self.comboBoxLingua.addItem('italiano')
        self.comboBoxLingua.addItem('english')
        self.comboBoxLingua.addItem('español')
        self.comboBoxLingua.currentIndexChanged.connect(self.langChanged)
        if currentLang == 'ita':
            self.comboBoxLingua.setCurrentIndex(0)
        else:
            if currentLang == 'esp':
                self.comboBoxLingua.setCurrentIndex(2)
            else:
                self.comboBoxLingua.setCurrentIndex(1)
        self.comboBoxJCM.clear()
        self.comboBoxJCM.addItem('4')
        self.comboBoxJCM.addItem('2')
        self.comboBoxJCM.currentIndexChanged.connect(self.JCMChanged)
        if int(self.getDbData('JCM')) == 4:
            self.comboBoxJCM.setCurrentIndex(0)
        else:
            self.comboBoxJCM.setCurrentIndex(1)
        self.pushButtonImpostazioniAdmin.move(480, 170)
        self.serverThread = ThreadServerQT().getInstance()
        self.serverThread.signal1.connect(self.requestReceived)
        self.serverThread.start()
    def on_pushButtonImpostazioniAdmin_released(self):
        self.frameImpostazioni.move(170, 0)
        self.frameMain.move(1700, 0)
    def on_pushButtonClean_released(self):
        self.cleanPayments()
        # Ported: unbuffered text mode (buffering=0) raises ValueError on Python 3.
        file = open('log/log.txt', 'w')
        print('', file=file)
        file.close()
        self.labelMess.setText(self.lang.get('PULIZIA_DONE'))
        QApplication.processEvents()
        time.sleep(5)
        self.labelMess.setText('')
    def on_pushButtonEsciImpostazioni_released(self):
        self.frameImpostazioni.move(1700, 0)
        self.frameMain.move(170, 0)
    def JCMChanged(self):
        if self.comboBoxJCM.currentIndex() == 0:
            self.setDbData('JCM', '4')
            self.setJCMUsed(4)
        else:
            self.setDbData('JCM', '2')
            self.setJCMUsed(2)
    def langChanged(self):
        currentLang = self.getDbData('LANG')
        if self.comboBoxLingua.currentIndex() == 0:
            if currentLang == 'ita':
                pass
            else:
                self.setDbData('LANG', 'ita')
                self.lang.change('lang/ita')
                setLabelLanguage(self, self.lang, 'ita')
        else:
            if self.comboBoxLingua.currentIndex() == 1:
                if currentLang == 'eng':
                    pass
                else:
                    self.setDbData('LANG', 'eng')
                    self.lang.change('lang/eng')
                    setLabelLanguage(self, self.lang, 'eng')
            else:
                if self.comboBoxLingua.currentIndex() == 2:
                    if currentLang == 'esp':
                        pass
                    else:
                        self.setDbData('LANG', 'esp')
                        self.lang.change('lang/esp')
                        setLabelLanguage(self, self.lang, 'esp')
    def on_pushButtonPlus1_released(self):
        self.aumentaDbCoins(1)
        if self.isPagamento:
            self.updateInseritoPagamento(1)
        else:
            self.refillAdded(1)
    def on_pushButtonPlus2_released(self):
        self.aumentaDbCoins(2)
        if self.isPagamento:
            self.updateInseritoPagamento(2)
        else:
            self.refillAdded(2)
    def on_pushButtonPlus5_released(self):
        self.aumentaDbCoins(5)
        if self.isPagamento:
            self.updateInseritoPagamento(5)
        else:
            self.refillAdded(5)
    def on_pushButtonPlus10_released(self):
        self.aumentaDbCoins(10)
        if self.isPagamento:
            self.updateInseritoPagamento(10)
        else:
            self.refillAdded(10)
    def on_pushButtonPlus20_released(self):
        self.aumentaDbCoins(20)
        if self.isPagamento:
            self.updateInseritoPagamento(20)
        else:
            self.refillAdded(20)
    def on_pushButtonPlus50_released(self):
        self.aumentaDbCoins(50)
        if self.isPagamento:
            self.updateInseritoPagamento(50)
        else:
            self.refillAdded(50)
    def on_pushButtonPlus100_released(self):
        self.aumentaDbCoins(100)
        if self.isPagamento:
            self.updateInseritoPagamento(100)
        else:
            self.refillAdded(100)
    def on_pushButtonPlus200_released(self):
        self.aumentaDbCoins(200)
        if self.isPagamento:
            self.updateInseritoPagamento(200)
        else:
            self.refillAdded(200)
    def on_pushButtonPlus500_released(self):
        if self.aumentaDbRecycler(500) == 0:
            stackerAttuale = int(self.getDbData('CASSA_BANCONOTE'))
            self.setDbData('CASSA_BANCONOTE', str(stackerAttuale + 500))
        if self.isPagamento:
            self.updateInseritoPagamento(500)
        else:
            self.refillAdded(500)
    def on_pushButtonPlus1000_released(self):
        if self.aumentaDbRecycler(1000) == 0:
            stackerAttuale = int(self.getDbData('CASSA_BANCONOTE'))
            self.setDbData('CASSA_BANCONOTE', str(stackerAttuale + 1000))
        if self.isPagamento:
            self.updateInseritoPagamento(1000)
        else:
            self.refillAdded(1000)
    def on_pushButtonPlus2000_released(self):
        if self.aumentaDbRecycler(2000) == 0:
            stackerAttuale = int(self.getDbData('CASSA_BANCONOTE'))
            self.setDbData('CASSA_BANCONOTE', str(stackerAttuale + 2000))
        if self.isPagamento:
            self.updateInseritoPagamento(2000)
        else:
            self.refillAdded(2000)
    def on_pushButtonPlus5000_released(self):
        if self.aumentaDbRecycler(5000) == 0:
            stackerAttuale = int(self.getDbData('CASSA_BANCONOTE'))
            self.setDbData('CASSA_BANCONOTE', str(stackerAttuale + 5000))
        if self.isPagamento:
            self.updateInseritoPagamento(5000)
        else:
            self.refillAdded(5000)
    def on_pushButtonPlus10000_released(self):
        if self.aumentaDbRecycler(10000) == 0:
            stackerAttuale = int(self.getDbData('CASSA_BANCONOTE'))
            self.setDbData('CASSA_BANCONOTE', str(stackerAttuale + 10000))
        if self.isPagamento:
            self.updateInseritoPagamento(10000)
        else:
            self.refillAdded(10000)
    def erogaImporto(self, value):
        try:
            print('erogazione importo ' + str(value))
            daErogare = int(value)
            arrayCash = self.getCashContent()
            arrayCash.sort()
            arrayCash.reverse()
            print(arrayCash)
            for elem in arrayCash:
                valore = int(elem[0])
                qty = int(elem[1])
                while valore <= daErogare and qty > 0:
                    print('erogo ' + str(valore))
                    daErogare -= valore
                    qty -= 1
                    if valore >= 500:
                        self.diminuisciDbRecycler(valore)
                    else:
                        self.diminuisciDbCoins(valore)
            print('residuo ' + str(daErogare))
            return daErogare
        except:
            print(traceback.format_exc())
    def erogaImportoCond(self, value, taglio, isSim=False):
        try:
            print('erogazione importo ' + str(value))
            daErogare = int(value)
            arrayCash = self.getCashContent()
            arrayCash.sort()
            arrayCash.reverse()
            for elem in arrayCash:
                valore = int(elem[0])
                if taglio == 0:
                    if valore > 200:
                        continue
                else:
                    if valore!= taglio:
                        continue
                qty = int(elem[1])
                while valore <= daErogare and qty > 0:
                    daErogare -= valore
                    qty -= 1
                    if not isSim:
                        if valore >= 500:
                            self.diminuisciDbRecycler(valore)
                        else:
                            self.diminuisciDbCoins(valore)
            print('residuo ' + str(daErogare))
            return daErogare
        except:
            print(traceback.format_exc())
    def refillAdded(self, valore):
        self.totRefill += valore
        self.labelRefill.setText(self.lang.get('REFILL_IN_CORSO') % (float(self.totRefill) / 100))
    def updateInseritoPagamento(self, valore):
        try:
            try:
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                print('aggiunto ' + str(valore))
                self.inserito += valore
                self.lineEditInserito.setText('%0.2f' % (float(self.inserito) / 100))
                if self.inserito == self.dovuto:
                    query = 'UPDATE PAGAMENTO SET INSERITO=' + str(self.inserito) + ", STATO=1 WHERE ID='" + str(self.idPayment) + "'"
                    c.execute(query)
                    conn.commit()
                    self.frameVendita.setEnabled(False)
                    self.labelVenditaMess.setText(self.lang.get('PAGAMENTO_COMPLETATO'))
                    QApplication.processEvents()
                    time.sleep(5)
                    self.frameVendita.move(1200, 10)
                    self.frameMain.move(170, 0)
                    self.idPayment = '0'
                    self.dovuto = 0
                    self.inserito = 0
                elif self.inserito > self.dovuto:
                    query = 'UPDATE PAGAMENTO SET INSERITO=' + str(self.inserito) + " WHERE ID='" + str(self.idPayment) + "'"
                    c.execute(query)
                    conn.commit()
                    self.resto = self.inserito - self.dovuto
                    self.frameVendita.setEnabled(False)
                    self.lineEditResto.setText('%0.2f' % (float(self.resto) / 100))
                    self.labelVenditaMess.setText(self.lang.get('EROG_RESTO'))
                    QApplication.processEvents()
                    residuo = self.erogaImporto(self.resto)
                    time.sleep(5)
                    if residuo == 0:
                        query = 'UPDATE PAGAMENTO SET RESTO=' + str(self.resto) + ", STATO=1 WHERE ID='" + str(self.idPayment) + "'"
                        c.execute(query)
                        conn.commit()
                        self.labelVenditaMess.setText(self.lang.get('PAGAMENTO_COMPLETATO'))
                        QApplication.processEvents()
                        time.sleep(5)
                        self.frameVendita.move(1200, 10)
                        self.frameMain.move(170, 0)
                        self.idPayment = '0'
                        self.dovuto = 0
                        self.inserito = 0
                        self.resto = 0
                    else:
                        query = 'UPDATE PAGAMENTO SET RESTO=' + str(self.resto - residuo) + ", STATO=5 WHERE ID='" + str(self.idPayment) + "'"
                        c.execute(query)
                        conn.commit()
                        self.labelVenditaMess.setText(self.lang.get('NO_RESTO') % (float(residuo) / 100))
                        self.frameVendita.setEnabled(True)
                        if residuo != self.resto:
                            self.pushButtonPlusRestituisci.setVisible(False)
                else:
                    query = 'UPDATE PAGAMENTO SET INSERITO=' + str(self.inserito) + " WHERE ID='" + str(self.idPayment) + "'"
                    c.execute(query)
                    conn.commit()
            except:
                pass
        finally:
            conn.close()

    def on_pushButtonPlusAccParziale_released(self):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        query = 'UPDATE PAGAMENTO SET STATO=3, ANNULLATO=\'' + self.operatoreCurrent + '\' WHERE ID=\'' + str(self.idPayment) + '\''
        c.execute(query)
        conn.commit()
        conn.close()
        self.frameVendita.setEnabled(False)
        self.labelVenditaMess.setText(self.lang.get('PAGAMENTO_COMPLETATO'))
        QApplication.processEvents()
        time.sleep(5)
        self.frameVendita.move(1200, 10)
        self.frameMain.move(170, 0)
        self.idPayment = '0'
        self.dovuto = 0
        self.inserito = 0
    def on_pushButtonPlusRestituisci_released(self):
        conn = sqlite3.connect('db.s3db')
        c = conn.cursor()
        self.frameVendita.setEnabled(False)
        self.labelVenditaMess.setText(self.lang.get('EROG_RESTO'))
        QApplication.processEvents()
        residuo = self.erogaImporto(self.inserito)
        query = 'UPDATE PAGAMENTO SET RESTO=' + str(residuo) + ', ANNULLATO=\'' + self.operatoreCurrent + '\', STATO=2 WHERE ID=\'' + str(self.idPayment) + '\''
        c.execute(query)
        conn.commit()
        conn.close()
        time.sleep(2)
        self.frameVendita.setEnabled(False)
        self.labelVenditaMess.setText(self.lang.get('PAGAMENTO_COMPLETATO'))
        QApplication.processEvents()
        time.sleep(2)
        self.frameVendita.move(1200, 10)
        self.frameMain.move(170, 0)
        self.idPayment = '0'
        self.dovuto = 0
        self.inserito = 0
    def requestReceived(self, stringCommand):
        try:
            # irreducible cflow, using cdg fallback
            print('ricevuta richiesta ' + str(stringCommand))
            args = stringCommand.split('#')
            if args[0] == 'reqPayment':
                if self.idPayment!= '0':
                    jsonDict = {}
                    jsonDict['req_status'] = 2
                    jsonDict['mess'] = 105
                    jsonDict['tipo'] = 1
                    self.setResult(json.dumps(jsonDict))
                    return
                else:
                    self.pushButtonPlus500.setVisible(True)
                    self.pushButtonPlus1000.setVisible(True)
                    self.pushButtonPlus2000.setVisible(True)
                    self.pushButtonPlus5000.setVisible(True)
                    self.pushButtonPlus10000.setVisible(True)
                    self.pushButtonPlus1.setVisible(True)
                    self.pushButtonPlus2.setVisible(True)
                    self.pushButtonPlus5.setVisible(True)
                    self.pushButtonPlus10.setVisible(True)
                    self.pushButtonPlus20.setVisible(True)
                    self.pushButtonPlus50.setVisible(True)
                    self.pushButtonPlus100.setVisible(True)
                    self.pushButtonPlus200.setVisible(True)
                    if not self.getRiciclaMonete(1):
                        self.pushButtonPlus1.setVisible(False)
                    if not self.getRiciclaMonete(2):
                        self.pushButtonPlus2.setVisible(False)
                    if not self.getRiciclaMonete(5):
                        self.pushButtonPlus5.setVisible(False)
                    if not self.getRiciclaMonete(10):
                        self.pushButtonPlus10.setVisible(False)
                    if not self.getRiciclaMonete(20):
                        self.pushButtonPlus20.setVisible(False)
                    if not self.getRiciclaMonete(50):
                        self.pushButtonPlus50.setVisible(False)
                    if not self.getRiciclaMonete(100):
                        self.pushButtonPlus100.setVisible(False)
                    if not self.getRiciclaMonete(200):
                        self.pushButtonPlus200.setVisible(False)
                    self.operatoreCurrent = str(args[2])
                    conn = sqlite3.connect('db.s3db')
                    c = conn.cursor()
                    now = str(int(time.time()))
                    self.idPayment = now + '%03d' % self.idCurrent
                    self.idCurrent += 1
                    self.dovuto = int(args[1])
                    operatore = args[2]
                    refundable = (-2)
                    if int(args[3]) == 1:
                        refundable = (-1)
                    query = 'INSERT INTO PAGAMENTO(TIMESTAMP,ID,DOVUTO,INSERITO,STATO,RESTO,OPERATORE,REFUND)'
                    query += ' VALUES(\'' + now + '\',\'' + str(self.idPayment) + '\',' + str(self.dovuto) + ',0,0,0,\'' + operatore + '\',' + str(refundable) + ')'
                    c.execute(query)
                    conn.commit()
                    conn.close()
                    self.frameMain.move(170, 0)
                    self.frameVendita.move(120, 10)
                    self.frameVendita.setEnabled(True)
                    self.lineEditRichiesto.setText('%0.2f' % (float(self.dovuto) / 100))
                    self.lineEditInserito.setText('%0.2f' % 0)
                    self.lineEditResto.setText('%0.2f' % 0)
                    self.labelVenditaMess.setText('')
                    self.isPagamento = True
                    self.pushButtonPlus10000.setVisible(True)
                    self.frameVenditaInCorso.setVisible(True)
                    self.pushButtonPlusAccParziale.setVisible(True)
                    self.pushButtonPlusRestituisci.setVisible(True)
                    self.labelRefill.setVisible(False)
                    jsonDict = {}
                    jsonDict['req_status'] = 1
                    jsonDict['tipo'] = 1
                    jsonDict['importo'] = self.dovuto
                    jsonDict['id'] = str(self.idPayment)
                    self.setResult(json.dumps(jsonDict))
            elif args[0] == 'deletePayment':
                self.operatoreCurrent = args[3]
                tipoAnnullamento = args[2]
                id = args[1]
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 3
                if str(self.idPayment) == str(id):
                    jsonDict['payment_status'] = 2
                    self.setResult(json.dumps(jsonDict))
                    if int(tipoAnnullamento) == 1:
                        self.on_pushButtonPlusAccParziale_released()
                    else:
                        if self.getRestoPagamento(id) > 0:
                            jsonDict = {}
                            jsonDict['req_status'] = 2
                            jsonDict['tipo'] = 3
                            jsonDict['mess'] = 104
                            self.setResult(json.dumps(jsonDict))
                        else:
                            self.on_pushButtonPlusRestituisci_released()
                else:
                    jsonDict['payment_status'] = 1
                    self.setResult(json.dumps(jsonDict))
            elif args[0] == 'reqPrel':
                amount = args[1]
                taglio = args[3]
                idPrel = str(int(time.time()))
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 10
                jsonDict['id'] = idPrel
                jsonDict['importo'] = amount
                try:
                    amount = int(amount)
                    if taglio == 'monete':
                        test = self.erogaImportoCond(amount, 0, isSim=True)
                        if test > 0:
                            jsonDict = {}
                            jsonDict['req_status'] = 2
                            jsonDict['mess'] = 106
                            jsonDict['tipo'] = 10
                            self.setResult(json.dumps(jsonDict))
                            return
                        residuo = self.erogaImportoCond(amount, 0)
                        paid = amount - residuo
                    elif taglio[0:7] == 'monete_':
                        moneta = int(taglio.split('_')[1])
                        test = self.erogaImportoCond(amount, moneta, isSim=True)
                        if test > 0:
                            jsonDict = {}
                            jsonDict['req_status'] = 2
                            jsonDict['mess'] = 106
                            jsonDict['tipo'] = 10
                            self.setResult(json.dumps(jsonDict))
                            return
                        residuo = self.erogaImportoCond(amount, moneta)
                        paid = amount - residuo
                    elif taglio[0:9] == 'banconota':
                        banconota = int(taglio.split('_')[1])
                        test = self.erogaImportoCond(amount, banconota, isSim=True)
                        if test > 0:
                            jsonDict = {}
                            jsonDict['req_status'] = 2
                            jsonDict['mess'] = 106
                            jsonDict['tipo'] = 10
                            self.setResult(json.dumps(jsonDict))
                            return
                        residuo = self.erogaImportoCond(amount, banconota)
                        paid = amount - residuo
                    elif taglio == 'all':
                        residuo = self.erogaImporto(amount)
                        paid = amount - residuo
                    else:
                        raise Exception
                except:
                    jsonDict = {}
                    jsonDict['req_status'] = 2
                    jsonDict['mess'] = 103
                    jsonDict['tipo'] = 10
                    self.setResult(json.dumps(jsonDict))
                    return

                self.setResult(json.dumps(jsonDict))
                self.setDbData('PRELIEVO', '1')
                self.labelMess.setText(self.lang.get('PREL_IN_CORSO'))
                QApplication.processEvents()
                time.sleep(5)
                self.setDbData('PRELIEVO', '2*' + str(amount) + '*' + str(paid))
                self.labelMess.setText(self.lang.get('PREL_DONE') % (float(paid) / 100))
                self.updateOpDone('PRELIEVO', paid)
                QApplication.processEvents()
                time.sleep(5)
                self.labelMess.setText('')
            elif args[0] == 'refillStart':
                acceptAll = int(args[1])
                self.isPagamento = False
                self.frameMain.move(170, 0)
                self.frameVendita.move(120, 10)
                self.frameVendita.setEnabled(True)
                self.setDbData('REFILL', '1')
                arrayTagliRecycler = self.getArrayRecycler()
                if acceptAll == 1:
                    self.pushButtonPlus500.setVisible(True)
                    self.pushButtonPlus1000.setVisible(True)
                    self.pushButtonPlus2000.setVisible(True)
                    self.pushButtonPlus5000.setVisible(True)
                    self.pushButtonPlus10000.setVisible(True)
                else:
                    if 500 in arrayTagliRecycler:
                        self.pushButtonPlus500.setVisible(True)
                    else:
                        self.pushButtonPlus500.setVisible(False)
                    if 1000 in arrayTagliRecycler:
                        self.pushButtonPlus1000.setVisible(True)
                    else:
                        self.pushButtonPlus1000.setVisible(False)
                    if 2000 in arrayTagliRecycler:
                        self.pushButtonPlus2000.setVisible(True)
                    else:
                        self.pushButtonPlus2000.setVisible(False)
                    if 5000 in arrayTagliRecycler:
                        self.pushButtonPlus5000.setVisible(True)
                    else:
                        self.pushButtonPlus5000.setVisible(False)
                    if 10000 in arrayTagliRecycler:
                        self.pushButtonPlus10000.setVisible(True)
                    else:
                        self.pushButtonPlus10000.setVisible(False)
                self.pushButtonPlus1.setVisible(True)
                self.pushButtonPlus2.setVisible(True)
                self.pushButtonPlus5.setVisible(True)
                self.pushButtonPlus10.setVisible(True)
                self.pushButtonPlus20.setVisible(True)
                self.pushButtonPlus50.setVisible(True)
                self.pushButtonPlus100.setVisible(True)
                self.pushButtonPlus200.setVisible(True)
                if not self.getRiciclaMonete(1):
                    self.pushButtonPlus1.setVisible(False)
                if not self.getRiciclaMonete(2):
                    self.pushButtonPlus2.setVisible(False)
                if not self.getRiciclaMonete(5):
                    self.pushButtonPlus5.setVisible(False)
                if not self.getRiciclaMonete(10):
                    self.pushButtonPlus10.setVisible(False)
                if not self.getRiciclaMonete(20):
                    self.pushButtonPlus20.setVisible(False)
                if not self.getRiciclaMonete(50):
                    self.pushButtonPlus50.setVisible(False)
                if not self.getRiciclaMonete(100):
                    self.pushButtonPlus100.setVisible(False)
                if not self.getRiciclaMonete(200):
                    self.pushButtonPlus200.setVisible(False)
                self.frameVenditaInCorso.setVisible(False)
                self.pushButtonPlusAccParziale.setVisible(False)
                self.pushButtonPlusRestituisci.setVisible(False)
                self.labelRefill.setVisible(True)
                self.refillAdded(0)
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 30
                self.setResult(json.dumps(jsonDict))
            elif args[0] == 'refillEnd':
                self.isPagamento = False
                self.frameMain.move(170, 0)
                self.frameVendita.move(1200, 10)
                self.setDbData('REFILL', '0')
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 31
                self.setResult(json.dumps(jsonDict))
                self.labelMess.setText(self.lang.get('REFILL_DONE') % (float(self.totRefill) / 100))
                self.updateOpDone('REFILL', self.totRefill)
                QApplication.processEvents()
                time.sleep(5)
                self.labelMess.setText('')
                self.totRefill = 0
            elif args[0] == 'refillPoll':
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 33
                jsonDict['refillOn'] = self.getDbData('REFILL')
                jsonDict['amountRefill'] = self.totRefill
                self.setResult(json.dumps(jsonDict))
            elif args[0] == 'svuotaMonete':
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 50
                self.setResult(json.dumps(jsonDict))
                self.setDbData('SVUOTAMENTO', '1')
                self.labelMess.setText(self.lang.get('EMPTY_COINS_IN_CORSO'))
                QApplication.processEvents()
                time.sleep(10)
                if args[1] == '0':
                    totaleSvuotato = self.resetDbCoins()
                else:
                    totaleSvuotato = self.resetDbCoins(isFull=False)
                self.setDbData('SVUOTAMENTO', '0')
                self.labelMess.setText(self.lang.get('EMPTY_COINS_DONE') % (float(totaleSvuotato) / 100))
                stackerMonete = int(self.getDbData('CASSA_MONETE'))
                self.setDbData('CASSA_MONETE', str(stackerMonete + totaleSvuotato))
                QApplication.processEvents()
                time.sleep(5)
                self.labelMess.setText('')
            elif args[0] == 'svuotaBanconote':
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 51
                self.setResult(json.dumps(jsonDict))
                self.setDbData('SVUOTAMENTO', '1')
                self.labelMess.setText(self.lang.get('EMPTY_NOTES_IN_CORSO'))
                QApplication.processEvents()
                time.sleep(10)
                if args[1] == '0':
                    totaleSvuotato = self.resetDbNotes()
                else:
                    totaleSvuotato = self.resetDbNotes(isFull=False)
                self.setDbData('SVUOTAMENTO', '0')
                self.labelMess.setText(self.lang.get('EMPTY_NOTES_DONE') % (float(totaleSvuotato) / 100))
                stackerBanconote = int(self.getDbData('CASSA_BANCONOTE'))
                self.setDbData('CASSA_BANCONOTE', str(stackerBanconote + totaleSvuotato))
                QApplication.processEvents()
                time.sleep(5)
                self.labelMess.setText('')
            elif args[0] == 'refund':
                jsonDict = {}
                jsonDict['req_status'] = 1
                jsonDict['tipo'] = 65
                self.setResult(json.dumps(jsonDict))
                idPagamento = str(args[1])
                self.setRimborso(idPagamento, False, 0)
                dovuto = int(args[2])
                rimborsato = int(args[3])
                self.labelMess.setText(self.lang.get('EROG_REFUND'))
                QApplication.processEvents()
                daPagare = dovuto - rimborsato
                residuo = self.erogaImporto(daPagare)
                refunded = daPagare - residuo
                time.sleep(5)
                self.labelMess.setText(self.lang.get('REFUND_DONE') % (float(refunded) / 100))
                self.setRimborso(idPagamento, True, rimborsato + refunded)
                QApplication.processEvents()
                time.sleep(5)
                self.labelMess.setText('')
        except:
            print(traceback.format_exc())
            self.serverThread.myHdl.result = 'NONE'

