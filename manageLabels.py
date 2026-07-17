# Source Generated with Decompyle++
# File: extract/AC_SIM.exe_extracted/PYZ-00.pyz_extracted/manageLabels.pyc (Python 3.9)

from PyQt6 import QtCore
import traceback

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    
    def _fromUtf8(s):
        return s



def setLabelLanguage(interface, lang, currentLang):
    
    try:
        interface.pushButtonImpostazioniAdmin.setText(lang.get('IMPOSTAZIONI'))
        interface.labelWaiting.setText(lang.get('CASSA_ATTIVA'))
        interface.labelLingua.setText(lang.get('SELECT_LANG'))
        interface.labelJCM.setText(lang.get('TAGLI_JCM'))
        stringaMonete = lang.get('MONETE_WORD').capitalize()
        interface.labelVenditaMonete.setText(stringaMonete)
        stringaBanconote = lang.get('BANCONOTE_WORD').capitalize()
        interface.labelVenditaBanconote.setText(stringaBanconote)
        interface.labelVenditaInCorso.setText(lang.get('STATO_PAGAMENTO'))
        interface.labelVenditaRichiesto.setText(lang.get('PAGO_RICHIESTO'))
        interface.labelVenditaInserito.setText(lang.get('PAGO_INSERITO'))
        interface.labelVenditaResto.setText(lang.get('PAGO_RESTO'))
        interface.pushButtonPlusAccParziale.setText(lang.get('PAGO_ACC'))
        interface.pushButtonPlusRestituisci.setText(lang.get('PAGO_RESTITUISCI'))
        interface.pushButtonClean.setText(lang.get('PULIZIA'))
    except:
        print(traceback.format_exc())


