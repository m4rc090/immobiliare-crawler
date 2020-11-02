from immobiliare_crawler.business.daemons import JobCralwer
from immobiliare_crawler.business.report import ReportGenerator
from immobiliare_crawler.business.smtp_manager import SmtpManager
from immobiliare_crawler.dao.daos import ZoneRomaDao, ImmobiliareCaseDao, UtentiDao, Utenti2CaseDao

from immobiliare_crawler.config.app_config import GMAIL_SENDER, GMAIL_PASS
from immobiliare_crawler.model.models import Utente


class MainWorkFlow:

    def run(self, run_crawler: bool, utente: Utente):

        zone_dao = ZoneRomaDao()

        dao_case = ImmobiliareCaseDao()
        dao_utenti2case = Utenti2CaseDao()
        if run_crawler:
            job_crawler = JobCralwer(dao_case=dao_case, dao_zone=zone_dao, dao_utenti2case=dao_utenti2case)
            job_crawler.run_crawler(**{"prezzo_minimo": utente.prezzo_minimo, "prezzo_massimo": utente.prezzo_massimo,
                                       "superficie_minima": utente.superficie_minima,
                                       "superficie_massima": utente.superficie_massima,
                                       "zone": [zone_dao.get_zona_by_nome(nomi).id_zona for nomi in utente.zone_text]})

        report_generator = ReportGenerator(dao_case=dao_case, dao_utenti2case=dao_utenti2case)
        print("-- inizio scrittura report")
        report_file_name = report_generator.generate(
            user=utente, report_folder="/home/marco/Documents/MarcoDocs/my-projects/immobiliare-crawler")
        print("-- completata scrittura file {}".format(report_file_name))

        smpt_manager = SmtpManager(sender=GMAIL_SENDER, receivers=utente.emails, password=GMAIL_PASS)
        smpt_manager.send(attachment_path=report_file_name)
        print("-- completato invio email")


if __name__ == '__main__':
    app = MainWorkFlow()
    utenti_dao = UtentiDao()

    for user in utenti_dao.all_utenti():
        app.run(run_crawler=True, utente=user)