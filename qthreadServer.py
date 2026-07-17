# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'qthreadServer.py'
# Bytecode version: 3.9.0beta5 (3425)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

from PyQt6.QtCore import QThread, pyqtSignal
import time
import sqlite3
import http.server
import ssl
import json
from io import BytesIO
import threading
import socketserver
import sys
import traceback
import datetime

# Server listener config. The original hardcoded HTTPS on 443; launcher.py may
# override these before the UI is built (the server thread reads them when it
# starts, from WidgetIf.__init__).
PORT = 443
USE_TLS = True


class ThreadServerQT(QThread):
    __instance = None
    class __ThreadServerQT(QThread):
        myHdl = None
        signal1 = pyqtSignal(str)
        class myHandler(http.server.BaseHTTPRequestHandler):
            objectEmit = None
            filePrint = None
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
                query = 'SELECT NUMERO,FONDOCASSA,MAX_LEVEL,ACCETTA,RICICLA FROM CONTENT_COINS WHERE VALORE=' + str(moneta)
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return row
            def getDbRecycler(self, cassetta):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT VALORE,NUMERO FROM CONTENT_RECYCLER WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return [row[0], row[1]]
            def getResult(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT RESP FROM WAIT_RESULT WHERE 1'
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return str(row[0])
            def setResult(self, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE WAIT_RESULT SET RESP=\'' + valore + '\' WHERE 1'
                c.execute(query)
                conn.commit()
                conn.close()
            def getStatusPayment(self, id):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT STATO,DOVUTO,INSERITO,RESTO,OPERATORE FROM PAGAMENTO WHERE ID=\'' + id + '\''
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return row
            def getPendingPayment(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT ID,DOVUTO FROM PAGAMENTO WHERE STATO=0'
                c.execute(query)
                rows = c.fetchall()
                conn.close()
                return rows
            def getAllPayments(self, dateStart, dateEnd):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT TIMESTAMP,ID,STATO,DOVUTO,INSERITO,RESTO,OPERATORE,ANNULLATO,REFUND FROM PAGAMENTO WHERE                 (TIMESTAMP <= ' + str(dateEnd) + ' AND TIMESTAMP > ' + str(dateStart) + ')'
                c.execute(query)
                rows = c.fetchall()
                conn.close()
                return rows
            def getRimborso(self, id):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT STATO,DOVUTO,REFUND FROM PAGAMENTO WHERE ID=\'' + str(id) + '\''
                c.execute(query)
                rows = c.fetchone()
                conn.close()
                return rows
            def getRefundStatus(self, id):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT DOVUTO,REFUND,REFUND_ON FROM PAGAMENTO WHERE ID=\'' + str(id) + '\''
                c.execute(query)
                rows = c.fetchone()
                conn.close()
                return rows
            def setLivelliMonete(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_COINS SET NUMERO=' + str(valore) + ' WHERE VALORE=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def setLivelliBanconote(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_RECYCLER SET NUMERO=' + str(valore) + ' WHERE CASSETTA=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def getLivelliMinimiMonete(self, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT FONDOCASSA FROM CONTENT_COINS WHERE VALORE=' + str(valore)
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return int(row[0])
            def setLivelliMinimiMonete(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_COINS SET FONDOCASSA=' + str(valore) + ' WHERE VALORE=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def setLivelliMassimiMonete(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_COINS SET MAX_LEVEL=' + str(valore) + ' WHERE VALORE=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def setAccettaMonete(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_COINS SET ACCETTA=' + str(valore) + ' WHERE VALORE=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def setRiciclaMonete(self, taglio, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_COINS SET RICICLA=' + str(valore) + ' WHERE VALORE=' + str(taglio)
                c.execute(query)
                conn.commit()
                conn.close()
            def getLivelliMinimiBanconote(self, cassetta):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT FONDOCASSA FROM CONTENT_RECYCLER WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return int(row[0])
            def setLivelliMinimiBanconote(self, cassetta, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_RECYCLER SET FONDOCASSA=' + str(valore) + ' WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
                c.execute(query)
                conn.commit()
                conn.close()
            def getLivelliMassimiBanconote(self, cassetta):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT MAX_LEVEL FROM CONTENT_RECYCLER WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
                c.execute(query)
                row = c.fetchone()
                conn.close()
                return int(row[0])
            def setLivelliMassimiBanconote(self, cassetta, valore):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_RECYCLER SET MAX_LEVEL=' + str(valore) + ' WHERE CASSETTA=' + str(cassetta) + ' AND USED=1'
                c.execute(query)
                conn.commit()
                conn.close()
            def setCassetteDenom(self, cassette, denom):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'UPDATE CONTENT_RECYCLER SET VALORE=' + str(denom) + ' WHERE CASSETTA=' + str(cassette) + ' AND USED=1'
                c.execute(query)
                conn.commit()
                conn.close()
            def getTotalPayments(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT SUM(DOVUTO),SUM(INSERITO),SUM(RESTO) FROM PAGAMENTO'
                c.execute(query)
                row = c.fetchone()
                if row[0] == None:
                    return [0, 0, 0]
                conn.close()
                return row
            def resetTotalPayments(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'DELETE FROM PAGAMENTO WHERE 1'
                c.execute(query)
                c.execute('commit')
            def getTotalContent(self):
                totale = 0
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT SUM(VALORE*NUMERO) FROM CONTENT_COINS WHERE 1'
                c.execute(query)
                row = c.fetchone()
                totale += int(row[0])
                query = 'SELECT SUM(VALORE*NUMERO) FROM CONTENT_RECYCLER WHERE USED=1'
                c.execute(query)
                row = c.fetchone()
                totale += int(row[0])
                conn.close()
                return totale
            def getTotalIn(self):
                totale = 0
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT SUM(VALORE) FROM REFILL WHERE TIPO=\'REFILL\''
                c.execute(query)
                row = c.fetchone()
                print(row)
                if row[0] == None:
                    return 0
                totale += int(row[0])
                return totale
            def getTotalOut(self):
                totale = 0
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'SELECT SUM(VALORE) FROM REFILL WHERE TIPO=\'SVUOTA\' OR TIPO=\'PRELIEVO\''
                c.execute(query)
                row = c.fetchone()
                if row[0] == None:
                    return 0
                totale += int(row[0])
                return totale
            def resetTotalInOut(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                query = 'DELETE FROM REFILL WHERE 1'
                c.execute(query)
                c.execute('commit')
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
            def getStackerDetails(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                dict = {}
                for elem in [500, 1000, 2000, 5000, 10000]:
                    query = 'SELECT NUMERO FROM STACKER_CONTENT WHERE DENOM=' + str(elem)
                    c.execute(query)
                    row = c.fetchone()
                    dict[elem] = int(row[0])
                conn.close()
                return dict
            def resetContentStacker(self):
                conn = sqlite3.connect('db.s3db')
                c = conn.cursor()
                for elem in [500, 1000, 2000, 5000, 10000]:
                    query = 'UPDATE STACKER_CONTENT SET NUMERO=0 WHERE DENOM=' + str(elem)
                    c.execute(query)
                    conn.commit()
                conn.close()
                return 1
            def do_POST(self):
                tipo = 0
                try:
                    try:
                        self.filePrint = open('log/log.txt', 'a')
                        content_length = int(self.headers['Content-Length'])
                        body = self.rfile.read(content_length)
                        jsonBody = json.loads(body)
                        tipo = int(jsonBody['tipo'])
                        print('request tipo ' + str(tipo))
                        print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f') + ' RECEIVED: ' + str(jsonBody), file=self.filePrint)
                        self.setResult('WAITING_RESP')
                        respMacchina = 'WAITING_RESP'
                        if tipo == 1:
                            importo = jsonBody['importo']
                            if jsonBody.get('opName')!= None:
                                opName = jsonBody['opName']
                            else:
                                opName = 'none'
                            operatore = opName.replace('/\\s+/', '%20')
                            if jsonBody.get('refundable')!= None:
                                refundable = int(jsonBody['refundable'])
                            else:
                                refundable = 1
                            if jsonBody.get('credit_card')!= None:
                                usePos = jsonBody['credit_card']
                            else:
                                usePos = 0
                            if jsonBody.get('payToken')!= None:
                                payToken = jsonBody['payToken']
                            else:
                                payToken = 0
                            stringCommand = 'reqPayment#' + str(importo) + '#' + operatore + '#' + str(refundable) + '#' + str(usePos) + '#' + str(payToken) + '#'
                        elif tipo == 2:
                            jsonDict = {}
                            jsonDict['tipo'] = tipo
                            id = jsonBody['id']
                            jsonDict['id'] = str(id)
                            pollRes = self.getStatusPayment(id)
                            if pollRes == None:
                                jsonDict['req_status'] = 1
                                jsonDict['mess'] = 104
                                respMacchina = json.dumps(jsonDict)
                            else:
                                jsonDict['req_status'] = 1
                                if pollRes[0] == 0:
                                    payment_status = 2
                                    respStatus = 'pending'
                                else:
                                    if pollRes[0] == 5:
                                        payment_status = 2
                                        respStatus = 'notCompleted'
                                    else:
                                        payment_status = 1
                                        if pollRes[0] == 1:
                                            respStatus = 'completed'
                                        else:
                                            if pollRes[0] == 2:
                                                respStatus = 'returned'
                                            else:
                                                if pollRes[0] == 3:
                                                    respStatus = 'partial'
                                                else:
                                                    if pollRes[0] == 4:
                                                        respStatus = 'deleted'
                                jsonDict['payment_status'] = payment_status
                                jsonDict['payment_details'] = {'amount': int(pollRes[1]), 'inserted': int(pollRes[2]), 'rest': int(pollRes[3]), 'status': respStatus}
                                respMacchina = json.dumps(jsonDict)
                        elif tipo == 3:
                            id = jsonBody['id']
                            tipo_ann = jsonBody['tipo_annullamento']
                            if jsonBody.get('opName')!= None:
                                opName = jsonBody['opName']
                            else:
                                opName = 'none'
                            operatore = opName.replace('/\\s+/', '%20')
                            stringCommand = 'deletePayment#' + str(id) + '#' + str(tipo_ann) + '#' + operatore + '#'
                        elif tipo == 5 or tipo == 6:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            rows = self.getPendingPayment()
                            jsonDict['list_length'] = len(rows)
                            if len(rows) > 0:
                                dictPending = {}
                                index = 0
                                for elem in rows:
                                    if tipo == 6:
                                        dictPending['id_' + str(index)] = [str(elem[0]), str(elem[1])]
                                    else:
                                        dictPending['id_' + str(index)] = str(elem[0])
                                    index += 1
                                jsonDict['pending_list'] = dictPending
                            print('ENDING ' + str(jsonDict))
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 10:
                            importo = jsonBody['importo']
                            if jsonBody.get('opName')!= None:
                                opName = jsonBody['opName']
                            else:
                                opName = 'none'
                            operatore = opName.replace('/\\s+/', '%20')
                            if jsonBody.get('taglio')!= None:
                                taglio = jsonBody['taglio']
                            else:
                                taglio = '0'
                            stringCommand = 'reqPrel#' + str(importo) + '#' + operatore + '#' + str(taglio) + '#'
                        elif tipo == 11:
                            id = jsonBody['id']
                            jsonDict = {}
                            prelInCorso = str(self.getDbData('PRELIEVO')).split('*')
                            if prelInCorso[0] == '0':
                                jsonDict['req_status'] = 2
                                jsonDict['tipo'] = 11
                                jsonDict['mess'] = 104
                                respMacchina = json.dumps(jsonDict)
                            else:
                                if prelInCorso[0] == '1':
                                    jsonDict['req_status'] = 1
                                    jsonDict['tipo'] = 11
                                    jsonDict['id'] = id
                                    jsonDict['withdraw_status'] = 2
                                    respMacchina = json.dumps(jsonDict)
                                else:
                                    amount = int(prelInCorso[1])
                                    paid = int(prelInCorso[2])
                                    jsonDict['req_status'] = 1
                                    jsonDict['tipo'] = 11
                                    jsonDict['id'] = id
                                    jsonDict['withdraw_status'] = 1
                                    jsonDict['payment_details'] = {'amount': amount, 'withdrawed': paid}
                                    respMacchina = json.dumps(jsonDict)
                                    self.setDbData('PRELIEVO', '0')
                        elif tipo == 20:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            dictHopper = {}
                            dictHopper['error'] = 0
                            dictHopper['mess'] = 'OK'
                            dictHopper['stacker'] = int(self.getDbData('CASSA_MONETE'))
                            totHopper = 0
                            for i in [1, 2, 5, 10, 20, 50, 100, 200]:
                                qty = int(self.getDbCoins(i)[0])
                                totHopper += qty * i
                                dictHopper['moneta_' + str(i)] = qty
                                if qty < 20:
                                    dictHopper['moneta_' + str(i) + '_alert'] = 1
                                else:
                                    dictHopper['moneta_' + str(i) + '_alert'] = 0
                                dictHopper['moneta_' + str(i) + '_accept'] = int(self.getDbCoins(i)[3])
                                dictHopper['moneta_' + str(i) + '_recycle'] = int(self.getDbCoins(i)[4])
                                dictHopper['moneta_' + str(i) + '_min_level'] = int(self.getDbCoins(i)[1])
                                dictHopper['moneta_' + str(i) + '_max_level'] = int(self.getDbCoins(i)[2])
                            dictHopper['totalInRecycle'] = totHopper
                            dictRecycler = {}
                            dictRecycler['error'] = 0
                            dictRecycler['mess'] = 'OK'
                            dictRecycler['stacker'] = int(self.getDbData('CASSA_BANCONOTE'))
                            dictRecycler['detailNotesStacker'] = self.getStackerDetails()
                            totRecycler = 0
                            numCass = int(self.getDbData('JCM')) + 1
                            for i in range(1, numCass):
                                valoreCassetta = int(self.getDbRecycler(i)[0])
                                qty = int(self.getDbRecycler(i)[1])
                                totRecycler += qty * valoreCassetta
                                tempDict = {}
                                tempDict['valore'] = valoreCassetta
                                tempDict['quantita'] = qty
                                if qty == 0:
                                    tempDict['alert'] = 2
                                else:
                                    if qty < 6:
                                        tempDict['alert'] = 1
                                    else:
                                        tempDict['alert'] = 0
                                tempDict['min_level'] = self.getLivelliMinimiBanconote(i)
                                tempDict['max_level'] = self.getLivelliMassimiBanconote(i)
                                dictRecycler['banconota_' + str(i)] = tempDict
                            dictRecycler['totalInRecycle'] = totRecycler
                            jsonDict['recycler'] = dictRecycler
                            jsonDict['hopper'] = dictHopper
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 23:
                            jsonDict = {}
                            jsonDict['tipo'] = 23
                            jsonDict['req_status'] = 1
                            jsonDict['recyclerUsed'] = 'JCM'
                            total_payments = 0
                            total_in = 0
                            total_out = 0
                            resp = self.getTotalPayments()
                            if resp!= None and len(resp) > 0 and (resp[0]!= None):
                                        total_payments = int(resp[0])
                                        total_in = int(resp[1])
                                        total_out = int(resp[2])
                            currentContent = self.getTotalContent() + int(self.getDbData('CASSA_MONETE')) + int(self.getDbData('CASSA_BANCONOTE'))
                            jsonDict['summary'] = ['1585304437', currentContent, total_payments, 0, total_payments, total_in, 0, 0, self.getTotalIn(), self.getTotalOut()]
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 30:
                            acceptAll = str(jsonBody['acceptAll'])
                            stringCommand = 'refillStart#' + acceptAll
                        elif tipo == 31:
                            stringCommand = 'refillEnd#'
                        elif tipo == 32:
                            print(jsonBody)
                            if int(self.getDbData('JCM')) == 2:
                                for i in [1, 2]:
                                    if jsonBody.get('refill').get('cassette_refill_' + str(i))!= None:
                                        numNotes = int(jsonBody.get('refill').get('cassette_refill_' + str(i)))
                                        self.setLivelliBanconote(i, numNotes)
                            for i in [1, 2, 5, 10, 20, 50, 100, 200]:
                                if jsonBody.get('refill').get('hopper_refill_' + str(i))!= None:
                                    numCoins = int(jsonBody.get('refill').get('hopper_refill_' + str(i)))
                                    self.setLivelliMonete(i, numCoins)
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 33:
                            stringCommand = 'refillPoll#'
                        elif tipo == 50:
                            tipo = jsonBody['full']
                            stringCommand = 'svuotaMonete#' + str(tipo)
                        elif tipo == 51:
                            tipo = jsonBody['full']
                            stringCommand = 'svuotaBanconote#' + str(tipo)
                        elif tipo == 52:
                            perif = int(jsonBody['peripheral'])
                            totaleSvuotato = 0
                            if perif == 0:
                                totaleSvuotato += int(self.getDbData('CASSA_MONETE'))
                                self.setDbData('CASSA_MONETE', '0')
                            else:
                                if perif == 1:
                                    totaleSvuotato += int(self.getDbData('CASSA_BANCONOTE'))
                                    self.setDbData('CASSA_BANCONOTE', '0')
                                    self.resetContentStacker()
                                else:
                                    if perif == 2:
                                        totaleSvuotato += int(self.getDbData('CASSA_MONETE'))
                                        totaleSvuotato += int(self.getDbData('CASSA_BANCONOTE'))
                                        self.setDbData('CASSA_MONETE', '0')
                                        self.setDbData('CASSA_BANCONOTE', '0')
                                        self.resetContentStacker()
                            self.updateOpDone('SVUOTA', totaleSvuotato)
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 53:
                            svuotamentoInCorso = int(self.getDbData('SVUOTAMENTO'))
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = 53
                            jsonDict['empty_status'] = svuotamentoInCorso
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 60:
                            total_payments = 0
                            total_in = 0
                            total_out = 0
                            resp = self.getTotalPayments()
                            if resp!= None and len(resp) > 0 and (resp[0]!= None):
                                        total_payments = int(resp[0])
                                        total_in = int(resp[1])
                                        total_out = int(resp[2])
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = 60
                            jsonDict['date'] = int(time.time())
                            jsonDict['start_date'] = self.getDbData('LAST_CHIUSURA')
                            self.setDbData('LAST_CHIUSURA', jsonDict['date'])
                            jsonDict['total_in'] = total_in
                            jsonDict['total_out'] = total_out
                            jsonDict['total_payments'] = total_payments
                            jsonDict['total_operator_in'] = self.getTotalIn()
                            jsonDict['total_operator_out'] = self.getTotalOut()
                            jsonDict['total_content'] = self.getTotalContent() + int(self.getDbData('CASSA_MONETE')) + int(self.getDbData('CASSA_BANCONOTE'))
                            self.resetTotalPayments()
                            self.resetTotalInOut()
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 65:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = 60
                            jsonDict['date'] = int(time.time())
                            id = jsonBody['id']
                            rimborso = self.getRimborso(id)
                            refundable = int(rimborso[2])
                            dovuto = int(rimborso[1])
                            stato = int(rimborso[0])
                            if stato!= 1 and stato!= 3 or refundable == (-2) or refundable == dovuto:
                                jsonDict['req_status'] = 2
                                jsonDict['mess'] = 165
                                respMacchina = json.dumps(jsonDict)
                            else:
                                if refundable < 0:
                                    refundable = 0
                                stringCommand = 'refund#' + str(id) + '#' + str(dovuto) + '#' + str(refundable)
                        elif tipo == 66:
                            id = jsonBody['id']
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = 66
                            jsonDict['id'] = id
                            result = self.getRefundStatus(id)
                            dovuto = int(result[0])
                            refund = int(result[1])
                            if refund < 0:
                                refund = 0
                            toRefund = dovuto - refund
                            if toRefund == 0:
                                toRefund = dovuto
                            jsonDict['toRefund'] = toRefund
                            jsonDict['refunded'] = refund
                            if int(result[2]) == 0:
                                jsonDict['refund_status'] = 'completed'
                            else:
                                jsonDict['refund_status'] = 'pending'
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 67:
                            data = jsonBody['refundDay']
                            s = data + ' 00:00:00'
                            startDate = int(time.mktime(datetime.datetime.strptime(s, '%d/%m/%Y %H:%M:%S').timetuple()))
                            s = data + ' 23:59:59'
                            endDate = int(time.mktime(datetime.datetime.strptime(s, '%d/%m/%Y %H:%M:%S').timetuple()))
                            allPayments = self.getAllPayments(startDate, endDate)
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = 65
                            arrayPayments = []
                            for elem in allPayments:
                                stato = int(elem[2])
                                refundable = int(elem[8])
                                dovuto = int(elem[3])
                                inserted = int(elem[4])
                                if stato!= 1 and stato!= 3 or refundable == (-2) or refundable == dovuto:
                                    pass
                                else:
                                    if refundable < 0:
                                        refundable = 0
                                    dict = {}
                                    dict['amount'] = dovuto
                                    dict['code'] = str(elem[1])
                                    dict['refunded'] = refundable
                                    dict['inserted'] = inserted
                                    arrayPayments.append(dict)
                            jsonDict['refund_list'] = arrayPayments
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 70:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            arrayWithdrawals = []
                            arrayWithdrawals.append({'date': 1499266246, 'value': 5000, 'operator': 'op1'})
                            arrayWithdrawals.append({'date': 1599266246, 'value': 2000, 'operator': 'op2'})
                            jsonDict['tipo'] = 70
                            jsonDict['withdrawals'] = arrayWithdrawals
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 71:
                            dateStart = jsonBody['start_date']
                            dateEnd = jsonBody['end_date']
                            allPayments = self.getAllPayments(dateStart, dateEnd)
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            arrayPayments = []
                            for elem in allPayments:
                                pollRes = int(elem[2])
                                if pollRes == 0:
                                    respStatus = 'pending'
                                else:
                                    if pollRes == 5:
                                        respStatus = 'notCompleted'
                                    else:
                                        if pollRes == 1:
                                            respStatus = 'completed'
                                        else:
                                            if pollRes == 2:
                                                respStatus = 'returned'
                                            else:
                                                if pollRes == 3:
                                                    respStatus = 'partial'
                                                else:
                                                    if pollRes == 4:
                                                        respStatus = 'deleted'
                                refunded = int(elem[8])
                                if refunded < 0:
                                    refunded = 0
                                arrayPayments.append({'date': str(elem[0]), 'id': str(elem[1]), 'status': respStatus, 'amount': int(elem[3]), 'inserted': int(elem[4]), 'rest': int(elem[5]), 'refund': refunded, 'operator': str(elem[6]), 'cancelled_by': str(elem[7])})
                            jsonDict['tipo'] = 71
                            jsonDict['payments'] = arrayPayments
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 72:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            arrayOpenings = []
                            arrayOpenings.append({'date': 1499266246, 'type': 0, 'operator': 'op1'})
                            arrayOpenings.append({'date': 1499266246, 'type': 1, 'operator': 'op1'})
                            jsonDict['tipo'] = 72
                            jsonDict['openings'] = arrayOpenings
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 73:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            arrayChiusure = []
                            arrayChiusure.append({'operator': 'op1', 'date': 1499296632, 'start_date': 1499242632, 'total_in': 75000, 'total_out': 11050, 'total_payments': 63950, 'total_operator_in': 10000, 'total_operator_out': 2000, 'total_content': 200000})
                            jsonDict['tipo'] = 73
                            jsonDict['closings'] = arrayChiusure
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 82:
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            jsonDict['version'] = 'SIM v' + self.getDbData('VERSION')
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 90:
                            print(jsonBody)
                            for i in [1, 2, 5, 10, 20, 50, 100, 200]:
                                if jsonBody.get('config').get('hopper_min_level_' + str(i))!= None:
                                    min_level = int(jsonBody.get('config').get('hopper_min_level_' + str(i)))
                                    self.setLivelliMinimiMonete(i, min_level)
                                if jsonBody.get('config').get('hopper_max_level_' + str(i))!= None:
                                    max_level = int(jsonBody.get('config').get('hopper_max_level_' + str(i)))
                                    self.setLivelliMassimiMonete(i, max_level)
                                if jsonBody.get('config').get('hopper_accept_' + str(i))!= None:
                                    accetta = int(jsonBody.get('config').get('hopper_accept_' + str(i)))
                                    self.setAccettaMonete(i, accetta)
                                if jsonBody.get('config').get('hopper_recycle_' + str(i))!= None:
                                    ricicla = int(jsonBody.get('config').get('hopper_recycle_' + str(i)))
                                    self.setRiciclaMonete(i, ricicla)
                            for i in range(1, 5):
                                if jsonBody.get('config').get('cassette_min_level_' + str(i))!= None:
                                    min_level = int(jsonBody.get('config').get('cassette_min_level_' + str(i)))
                                    self.setLivelliMinimiBanconote(i, min_level)
                                if jsonBody.get('config').get('cassette_max_level_' + str(i))!= None:
                                    max_level = int(jsonBody.get('config').get('cassette_max_level_' + str(i)))
                                    self.setLivelliMassimiBanconote(i, max_level)
                                if jsonBody.get('config').get('cassette_denom_' + str(i))!= None:
                                    denom = int(jsonBody.get('config').get('cassette_denom_' + str(i)))
                                    if denom in [500, 1000, 2000, 5000, 10000]:
                                        self.setCassetteDenom(i, denom)
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 91:
                            if jsonBody.get('config').get('single_payment')!= None:
                                print('SINGLE PAYMENT ' + str(jsonBody.get('config').get('single_payment')))
                                self.setDbData('SINGLE_PAYMENT', str(jsonBody.get('config').get('single_payment')))
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            respMacchina = json.dumps(jsonDict)
                        elif tipo == 12 or tipo == 40 or tipo == 41 or (tipo == 55) or (tipo == 81):
                            jsonDict = {}
                            jsonDict['req_status'] = 1
                            jsonDict['tipo'] = tipo
                            respMacchina = json.dumps(jsonDict)
                        else:
                            jsonDict = {}
                            jsonDict['req_status'] = 2
                            jsonDict['mess'] = 101
                            respMacchina = json.dumps(jsonDict)
                        if respMacchina == 'WAITING_RESP':
                            self.objectEmit.signal1.emit(stringCommand)
                            respMacchina = self.getResult()
                            while respMacchina == 'WAITING_RESP':
                                time.sleep(0.05)
                                respMacchina = self.getResult()
                        self.send_response(200)
                        self.end_headers()
                        response = BytesIO()
                        response.write(respMacchina.encode())
                        print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f') + ' RESPONSE: ' + str(respMacchina), file=self.filePrint)
                        self.wfile.write(response.getvalue())
                        self.setResult('0')
                    except:
                        print('ERRORE')
                        print(traceback.format_exc())
                        jsonDict = {}
                        jsonDict['req_status'] = 2
                        jsonDict['tipo'] = tipo
                        jsonDict['mess'] = 100
                        respMacchina = json.dumps(jsonDict)
                        self.send_response(200)
                        self.end_headers()
                        response = BytesIO()
                        response.write(respMacchina.encode())
                        print(datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f') + ' RESPONSE: ' + str(respMacchina), file=self.filePrint)
                        self.wfile.write(response.getvalue())
                        self.setResult('0')
                finally:
                    self.filePrint.close()

        class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
            socketserver.TCPServer.allow_reuse_address = True
            socketserver.TCPServer.request_queue_size = 1024
            def process_request(self, request, client_address):
                """Start a new thread to process the request."""
                num = threading.active_count()
                if num > 50:
                    self.shutdown_request(request)
                else:
                    t = threading.Thread(target=self.process_request_thread, args=(request, client_address))
                    t.daemon = self.daemon_threads
                    t.start()
            def handle_error(self, request, client_address):
                # Ported: sys.exc_clear() is Python 2 only. The override exists to
                # swallow per-request errors instead of logging them.
                pass
        def __init__(self, parent=None):
            QThread.__init__(self, parent)
        def run(self):
            self.myHdl = self.myHandler
            self.myHdl.objectEmit = self
            server = self.ThreadedTCPServer(('0.0.0.0', PORT), self.myHdl)
            if USE_TLS:
                # Ported: ssl.wrap_socket() was removed in Python 3.12.
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                context.load_cert_chain('server.pem')
                server.socket = context.wrap_socket(server.socket, server_side=True)
                print('server https on port ' + str(PORT))
            else:
                print('server http (no TLS) on port ' + str(PORT))
            server.serve_forever()
    def __init__(self):
        if self.__instance is None:
            ThreadServerQT.__instance = ThreadServerQT.__ThreadServerQT()
        self.__dict__['_ThreadServerQT__instance'] = ThreadServerQT.__instance

    def getInstance(self):
        return self.__instance
