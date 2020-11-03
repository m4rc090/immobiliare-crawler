import os
from datetime import datetime
import pandas as pd

from immobiliare_crawler.dao.daos import ImmobiliareCaseDao, Utenti2CaseDao
from immobiliare_crawler.model.models import Utente, Utente2Casa


class ReportGenerator:
    def __init__(self, dao_case: ImmobiliareCaseDao = ImmobiliareCaseDao(),
                 dao_utenti2case: Utenti2CaseDao = Utenti2CaseDao()):
        self.dao = dao_case
        self.dao_utenti2case = dao_utenti2case

    def generate(self, user: Utente, report_folder: str) -> str:

        # mi prendo le case gia inviate per questo utente
        case_inviate = self.dao_utenti2case.get_case_by_utente(user.id)

        try:
            case_da_inviare = []

            for casa in self.dao.all_case():
                if casa.id not in case_inviate:
                    case_da_inviare.append(casa)
                    self.dao_utenti2case.save_utente2casa(Utente2Casa(id_utente=user.id, id_casa=casa.id,
                                                                      send_date=datetime.today()))
            l = sorted(case_da_inviare, key=lambda x: x.prezzo, reverse=True)

            file_name = os.path.join(report_folder, "report_case_" + datetime.today().strftime("%d-%m-%Y") + ".xlsx")
            df_case = pd.DataFrame([vars(s) for s in l], columns=['_id_sorgente', '_link', '_titolo', '_prezzo', '_stanze', '_mq', '_bagni', '_piano'])

            ricerca = {'prezzo_minimo':  [str(user.prezzo_minimo)],
                       'prezzo_massimo': [str(user.prezzo_massimo)],
                       'superficie_minima': [str(user.superficie_minima)],
                       'superficie_massima': [str(user.superficie_massima)],
                       'zone': "|".join(user.zone_text)}

            df_ricerca = pd.DataFrame(ricerca, columns=['prezzo_minimo', 'prezzo_massimo',
                                                        'superficie_minima', 'superficie_massima', 'zone'])

            writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

            # Write each dataframe to a different worksheet.
            df_case.to_excel(writer, index=False, sheet_name='Case')
            df_ricerca.to_excel(writer, index=False, sheet_name='Ricerca')

            # Close the Pandas Excel writer and output the Excel file.
            writer.save()
            return file_name
        except Exception as e:
            for id_casa in case_inviate:
                self.dao_utenti2case.delete_utente2case(id_utente=user.id, id_casa=id_casa)
            raise e