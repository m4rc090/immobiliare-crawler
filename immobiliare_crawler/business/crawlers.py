from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from ds4biz_commons.utils.requests_utils import URLRequest

from immobiliare_crawler.model.models import CasaImmobiliare


class Crawler:
    def __init__(self):
        pass


class ImmobiliareCrawler(Crawler):
    def __init__(self, base_url: str ="https://www.immobiliare.it/en/vendita-appartamenti/roma/?criterio=rilevanza&noAste=1"):
        self._base_url = base_url
        self._prezzo_minimo = None
        self._prezzo_massimo = None
        self._superficie_minima = None
        self._superficie_massima = None
        self._zone = None

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str):
        self._base_url = base_url

    @property
    def prezzo_minimo(self):
        return self._prezzo_minimo

    @prezzo_minimo.setter
    def prezzo_minimo(self, prezzo_minimo: int):
        self._prezzo_minimo = prezzo_minimo

    @property
    def prezzo_massimo(self):
        return self._prezzo_massimo

    @prezzo_massimo.setter
    def prezzo_massimo(self, prezzo_massimo: int):
        self._prezzo_massimo = prezzo_massimo

    @property
    def superficie_minima(self):
        return self._superficie_minima

    @superficie_minima.setter
    def superficie_minima(self, superficie_minima: int):
        self._superficie_minima = superficie_minima

    @property
    def superficie_massima(self):
        return self._superficie_massima

    @superficie_massima.setter
    def superficie_massima(self, superficie_massima: int):
        self._superficie_massima = superficie_massima

    @property
    def zone(self):
        return self._zone

    @zone.setter
    def zone(self, zone: List[int]):
        self._zone = zone

    def crawl(self) -> List[CasaImmobiliare]:

        if self.prezzo_minimo:
            self.base_url += "&prezzoMinimo=" + str(self.prezzo_minimo)

        if self.prezzo_massimo:
            self.base_url += "&prezzoMassimo=" + str(self.prezzo_massimo)

        if self.superficie_minima:
            self.base_url += "&superficieMinima=" + str(self.superficie_minima)

        if self.superficie_massima:
            self.base_url += "&superficieMassima=" + str(self.superficie_massima)

        if self.zone:
            for zona in self.zone:
                self.base_url += "&idMZona[]=" + str(zona)

        u = URLRequest(self.base_url, response_converter=lambda response: response.text)

        # faccio la get sulla prima pagina
        text_html_page = u.get()
        bs_page = BeautifulSoup(text_html_page, features="html.parser")
        for casa in self.parse_case_in_pagina(bs_page): yield casa

        # faccio la get sulla successive pagine
        errore = False
        page_number = 2
        while not errore:
            try:
                url_paginated = self.base_url + "&pag=" + str(page_number)
                u = URLRequest(url_paginated, response_converter=lambda response: response.text)
                text_html_page = u.get()
                bs_page = BeautifulSoup(text_html_page, features="html.parser")
                for casa in self.parse_case_in_pagina(bs_page): yield casa
                page_number += 1
            except Exception as e:
                print("Pagine finite? ", e)
                errore = True

    def parse_case_in_pagina(self, bs_page: BeautifulSoup) -> List[CasaImmobiliare]:

        annunci_list = bs_page.find(name="ul", attrs={"class": "annunci-list"})
        case = annunci_list.find_all(name="li", attrs={"class": "listing-item"})
        for casa in case:
            id = casa.get("data-id")
            casa_body = casa.find(name="div", attrs={"class": "listing-item_body--content"})

            if casa_body:
                casa_obj = CasaImmobiliare(id_immobiliare=id, crawling_date=datetime.now())
                link_titolo = casa_body.find(name="p", attrs={"class": "titolo"})
                if link_titolo:
                    link = link_titolo.a.get("href")
                    casa_obj.link = link
                    titolo = link_titolo.a.get("title")
                    casa_obj.titolo = titolo

                casa_features = casa_body.find(name="ul", attrs={"class": "listing-features list-piped"})
                if casa_features:
                    prezzo = casa_features.find(name="li", attrs={"class": "lif__item lif__pricing"})
                    if prezzo:
                        try:
                            casa_obj.prezzo = int(prezzo.get_text().replace("€", "").replace(".", "").strip())
                        except Exception as e:
                            print(e)
                            casa_obj.prezzo = 0
                    features = casa_features.find_all(name="div", attrs={"class": "lif__data"})
                    if features:
                        if len(features) > 0:
                            stanze_span = features[0].find(name="span")
                            if stanze_span:
                                casa_obj.stanze = stanze_span.get_text().strip()
                        if len(features) > 1:
                            mq_span = features[1].find(name="span")
                            if mq_span:
                                casa_obj.mq = mq_span.get_text().strip()
                        if len(features) > 2:
                            bagni_span = features[2].find(name="span")
                            if bagni_span:
                                casa_obj.bagni = bagni_span.get_text().strip()
                        if len(features) > 3:
                            piano_abbr = features[3].find(name="abbr")
                            if piano_abbr:
                                casa_obj.piano = piano_abbr.get_text().strip()

                yield casa_obj