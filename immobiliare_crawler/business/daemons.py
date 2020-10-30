import os
from datetime import datetime
from typing import List

import pandas as pd

from immobiliare_crawler.business.crawlers import ImmobiliareCrawler
from immobiliare_crawler.dao.daos import ImmobiliareCaseDao, ZoneRomaDao
from immobiliare_crawler.model.models import CasaImmobiliare


class JobCralwer:
    def __init__(self, prezzo_minimo: int, prezzo_massimo: int, superficie_minima: int, superficie_massima: int,
                 zone: List[str], crawler: ImmobiliareCrawler = ImmobiliareCrawler(),
                 dao_case: ImmobiliareCaseDao = ImmobiliareCaseDao(collection="case_collection_1"),
                 dao_zone: ZoneRomaDao = ZoneRomaDao()):
        self.crawler = crawler
        self.dao = dao_case
        self.dao_zone = dao_zone
        self.prezzo_minimo = prezzo_minimo
        self.prezzo_massimo = prezzo_massimo
        self.superficie_minima = superficie_minima
        self.superficie_massima = superficie_massima
        self.zone = zone
        self.crawler.prezzo_minimo = prezzo_minimo
        self.crawler.prezzo_massimo = prezzo_massimo
        self.crawler.superficie_minima = superficie_minima
        self.crawler.superficie_massima = superficie_massima
        self.crawler.zone = zone

    def run_crawler(self):
        for i, casa in enumerate(self.crawler.crawl()):
            # print("#", i, casa.__dict__)
            self.dao.save_case(casa=casa)
