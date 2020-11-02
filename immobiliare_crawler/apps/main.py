from datetime import datetime
from typing import List

from immobiliare_crawler.business.daemons import JobCralwer
from immobiliare_crawler.business.report import ReportGenerator
from immobiliare_crawler.business.smtp_manager import SmtpManager
from immobiliare_crawler.dao.daos import ZoneRomaDao, ImmobiliareCaseDao

from immobiliare_crawler.config.app_config import GMAIL_SENDER, GMAIL_RECEIVERS, GMAIL_PASS


class MainWorkFlow:

    def __init__(self):
        pass

    def run(self, run_crawler: bool, zone_text: List[str], prezzo_minimo: int, prezzo_massimo: int,
            superficie_minima: int, superficie_massima: int, receivers: List[str]):

        zone_dao = ZoneRomaDao()
        params = {"prezzo_minimo": prezzo_minimo, "prezzo_massimo": prezzo_massimo,
                  "superficie_minima": superficie_minima, "superficie_massima": superficie_massima,
                  "zone": [zone_dao.get_zona_by_nome(nomi).id_zona for nomi in zone_text]}

        print(params["zone"])

        dao_case = ImmobiliareCaseDao(collection="case_collection_1")
        if run_crawler:
            job_crawler = JobCralwer(dao_case=dao_case, dao_zone=zone_dao)
            job_crawler.run_crawler(**params)

        params["zone"] = zone_text
        dt = datetime.now()
        report_generator = ReportGenerator(**params, dao_case=dao_case)
        print("-- inizio scrittura report")
        report_file_name = report_generator.generate("/home/marco/Documents/MarcoDocs/my-projects/immobiliare-crawler", dt)
        print("-- completata scrittura file {}".format(report_file_name))

        smpt_manager = SmtpManager(sender=GMAIL_SENDER, receivers=receivers, password=GMAIL_PASS)
        smpt_manager.send(dt=dt, attachment_path=report_file_name)
        print("-- completato invio email")


if __name__ == '__main__':
    app = MainWorkFlow()

    params = {"run_crawler": True,
              "prezzo_minimo": 160000,
              "prezzo_massimo": 280000,
              "superficie_minima": 40,
              "superficie_massima": 100,
              "zone_text": ["Eur, Torrino, Tintoretto",
                            "Garbatella, Navigatori, Ostiense",
                            "Marconi, San Paolo",
                            "Appia Pignatelli, Ardeatino, Montagnola"],
              "receivers": GMAIL_RECEIVERS}
    app.run(**params)