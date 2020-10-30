from immobiliare_crawler.business.daemons import JobCralwer
from immobiliare_crawler.business.report import ReportGenerator
from immobiliare_crawler.dao.daos import ZoneRomaDao, ImmobiliareCaseDao


def app(run_crawler: bool):
    params = {"prezzo_minimo": 160000, "prezzo_massimo": 280000, "superficie_minima": 40, "superficie_massima": 100}
    zone = ["Eur, Torrino, Tintoretto", "Garbatella, Navigatori, Ostiense", "Marconi, San Paolo"]
    zone_dao = ZoneRomaDao()

    id_zone = [zone_dao.get_zona_by_nome(nomi).id_zona for nomi in zone]
    print(id_zone)

    dao_case = ImmobiliareCaseDao(collection="case_collection_1")
    if run_crawler:
        job = JobCralwer(**params, zone=id_zone, dao_case=dao_case)
        job.run_crawler()

    report_generator = ReportGenerator(**params, nomi_zone=zone, dao_case=dao_case)
    report_generator.generate("/home/marco/Documents/MarcoDocs/my-projects/immobiliare-crawler")


if __name__ == '__main__':
    app(True)