from typing import List

from immobiliare_crawler.business.crawlers import ImmobiliareCrawler
from immobiliare_crawler.dao.daos import ImmobiliareCaseDao, ZoneRomaDao


class JobCralwer:
    def __init__(self, crawler: ImmobiliareCrawler = ImmobiliareCrawler(),
                 dao_case: ImmobiliareCaseDao = ImmobiliareCaseDao(collection="case_collection_1"),
                 dao_zone: ZoneRomaDao = ZoneRomaDao()):
        self.crawler = crawler
        self.dao = dao_case
        self.dao_zone = dao_zone

    def run_crawler(self, prezzo_minimo: int, prezzo_massimo: int, superficie_minima: int,
                    superficie_massima: int, zone: List[str]):
        for i, casa in enumerate(self.crawler.crawl(prezzo_minimo=prezzo_minimo,
                                                    prezzo_massimo=prezzo_massimo,
                                                    superficie_minima=superficie_minima,
                                                    superficie_massima=superficie_massima,
                                                    zone=zone)):
            self.dao.save_case(casa=casa)
