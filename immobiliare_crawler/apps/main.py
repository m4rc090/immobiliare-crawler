from immobiliare_crawler.business.daemons import JobCralwer
from immobiliare_crawler.business.report import ReportGenerator
from immobiliare_crawler.dao.daos import ZoneRomaDao, ImmobiliareCaseDao


def app(run_crawler: bool):
    zone_text = ["Eur, Torrino, Tintoretto", "Garbatella, Navigatori, Ostiense",
                       "Marconi, San Paolo", "Appia Pignatelli, Ardeatino, Montagnola"]

    zone_dao = ZoneRomaDao()
    params = {"prezzo_minimo": 160000, "prezzo_massimo": 280000, "superficie_minima": 40, "superficie_massima": 100,
              "zone": [zone_dao.get_zona_by_nome(nomi).id_zona for nomi in zone_text]}

    print(params["zone"])

    dao_case = ImmobiliareCaseDao(collection="case_collection_1")
    if run_crawler:
        job_crawler = JobCralwer(dao_case=dao_case, dao_zone=zone_dao)
        job_crawler.run_crawler(**params)

    params["zone"] = zone_text
    report_generator = ReportGenerator(**params, dao_case=dao_case)
    report_generator.generate("/home/marco/Documents/MarcoDocs/my-projects/immobiliare-crawler")


if __name__ == '__main__':
    app(True)