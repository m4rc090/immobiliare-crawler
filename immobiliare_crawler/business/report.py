import os
from typing import List
from datetime import datetime
import pandas as pd

from immobiliare_crawler.dao.daos import ImmobiliareCaseDao
from immobiliare_crawler.model.models import CasaImmobiliare


class ReportGenerator:
    def __init__(self, prezzo_minimo: int, prezzo_massimo: int, superficie_minima: int,
                 superficie_massima: int, zone: List[str],
                 dao_case: ImmobiliareCaseDao = ImmobiliareCaseDao(collection="case_collection_1")):
        self.prezzo_minimo = str(prezzo_minimo)
        self.prezzo_massimo = str(prezzo_massimo)
        self.superficie_minima = str(superficie_minima)
        self.superficie_massima = str(superficie_massima)
        self.nomi_zone = zone
        self.dao = dao_case

    def dayly_case(self) -> List[CasaImmobiliare]:
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        for case in self.dao.all_case_by_date(dt):
            yield case

    def all_case(self) -> List[CasaImmobiliare]:
        for case in self.dao.all_case():
            yield case

    def generate(self, report_folder: str):
        today = datetime.today().date()
        l = sorted(list(self.dayly_case()), key=lambda x: x.prezzo, reverse=True)
        # l = sorted(list(self.all_case()), key=lambda x: x.prezzo, reverse=True)

        print("-- inizio scrittura file")
        file_name = os.path.join(report_folder, "report_case_" + str(today)) + ".xlsx"
        df_case = pd.DataFrame([vars(s) for s in l], columns=['_id_immobiliare', '_link', '_titolo', '_prezzo', '_stanze', '_mq', '_bagni', '_piano'])

        ricerca = {'prezzo_minimo':  [self.prezzo_minimo],
                   'prezzo_massimo': [self.prezzo_massimo],
                   'superficie_minima': [self.superficie_minima],
                   'superficie_massima': [self.superficie_massima],
                   'zone': "|".join(self.nomi_zone)}

        df_ricerca = pd.DataFrame(ricerca, columns=['prezzo_minimo', 'prezzo_massimo',
                                                    'superficie_minima', 'superficie_massima', 'zone'])

        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

        # Write each dataframe to a different worksheet.
        df_case.to_excel(writer, index=False, sheet_name='Case')
        df_ricerca.to_excel(writer, index=False, sheet_name='Ricerca')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

        print("-- fine scrittura file")