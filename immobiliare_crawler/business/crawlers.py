import json
from typing import List

import requests
from bs4 import BeautifulSoup

from immobiliare_crawler.model.models import CasaImmobiliare, Zona


class Crawler:
    def __init__(self):
        pass


class ImmobiliareCrawler(Crawler):
    def __init__(self):
        self.base_url_case = "https://www.immobiliare.it/en/vendita-appartamenti/roma/?criterio=rilevanza&noAste=1"
        self.base_url_zone = "https://www.immobiliare.it/services/geography/getGeography.php?action=getMacrozoneComune&idComune=6737"
        self.comune = None
        self.id2name = dict()
        self.__parse_url(self.base_url_zone)

    def __parse_url(self, base_url: str):

        response = json.loads(requests.get(base_url).content.decode())
        if "info" in response and "nome" in response["info"]:
            self.comune = response["info"]["nome"]

        if "result" in response:
            macrozone = response["result"]
            for mz in macrozone:
                if "macrozona_idMacrozona" in mz and "macrozona_nome_sn" in mz:
                    self.id2name[mz["macrozona_idMacrozona"]] = mz["macrozona_nome_sn"]

    def all_zone(self) -> List[Zona]:
        for k, v in self.id2name.items():
            yield Zona(id_zona=k, nome_zona=v, comune=self.comune)

    def get_zona_by_id(self, id_zona: str) -> Zona:
        nome = self.id2name.get(id_zona)
        return Zona(id_zona=id_zona, nome_zona=nome, comune=self.comune)

    def get_zona_by_nome(self, nome_zona: str) -> Zona:
        ids = [k for k, v in self.id2name.items() if v == nome_zona]
        if len(ids) == 1:
            return Zona(id_zona=ids[0], nome_zona=nome_zona, comune=self.comune)
        raise Exception("Zona {} not found".format(nome_zona))

    def crawl(self, prezzo_minimo: int, prezzo_massimo: int, superficie_minima: int,
              superficie_massima: int, zone: List[str]) -> List[CasaImmobiliare]:

        id_zone = [self.get_zona_by_nome(nomi).id_zona for nomi in zone]

        self.base_url_case += "&prezzoMinimo=" + str(prezzo_minimo)

        self.base_url_case += "&prezzoMassimo=" + str(prezzo_massimo)

        self.base_url_case += "&superficieMinima=" + str(superficie_minima)

        self.base_url_case += "&superficieMassima=" + str(superficie_massima)

        for zona in id_zone:
            self.base_url_case += "&idMZona[]=" + str(zona)

        response = requests.get(self.base_url_case)
        if response.status_code != 200: raise Exception("Bad base url")
        text_html_page = response.content.decode()
        bs_page = BeautifulSoup(text_html_page, features="html.parser")
        for casa in self.parse_case_in_pagina(bs_page): yield casa

        # faccio la get sulla successive pagine
        errore = False
        page_number = 2
        while not errore:
            try:
                url_paginated = self.base_url_case + "&pag=" + str(page_number)
                response = requests.get(url_paginated)
                if response.status_code != 200: raise Exception("No more pages")
                text_html_page = response.content.decode()
                bs_page = BeautifulSoup(text_html_page, features="html.parser")
                for casa in self.parse_case_in_pagina(bs_page): yield casa
                page_number += 1
            except Exception as e:
                print("Pagine finite? ", e)
                errore = True

    def parse_case_in_pagina(self, bs_page: BeautifulSoup) -> List[CasaImmobiliare]:

        annunci_list = bs_page.find(name="ul", attrs={"class": "annunci-list"})
        if annunci_list:
            case = annunci_list.find_all(name="li", attrs={"class": "listing-item"})
            for casa in case:
                id = casa.get("data-id")
                casa_body = casa.find(name="div", attrs={"class": "listing-item_body--content"})

                if casa_body:
                    casa_obj = CasaImmobiliare(id_sorgente=id)
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