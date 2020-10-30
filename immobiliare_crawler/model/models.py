from datetime import datetime
from typing import Dict


class CasaImmobiliare:
    def __init__(self, id_immobiliare: str, crawling_date: datetime):
        self._id_immobiliare = id_immobiliare
        self._crawling_date = crawling_date
        self._link = "NA"
        self._titolo = "NA"
        self._prezzo = 0
        self._stanze = "NA"
        self._mq = "NA"
        self._bagni = "NA"
        self._piano = "NA"

    @property
    def id_immobiliare(self):
        return self._id_immobiliare

    @id_immobiliare.setter
    def id_immobiliare(self, id_immobiliare: str):
        self._id_immobiliare = id_immobiliare

    @property
    def crawling_date(self):
        return self._crawling_date

    @crawling_date.setter
    def crawling_date(self, crawling_date: datetime):
        self._crawling_date = crawling_date

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link: str):
        self._link = link

    @property
    def titolo(self):
        return self._titolo

    @titolo.setter
    def titolo(self, titolo: str):
        self._titolo = titolo

    @property
    def prezzo(self):
        return self._prezzo

    @prezzo.setter
    def prezzo(self, prezzo: int):
        self._prezzo = prezzo

    @property
    def stanze(self):
        return self._stanze

    @stanze.setter
    def stanze(self, stanze: str):
        self._stanze = stanze

    @property
    def mq(self):
        return self._mq

    @mq.setter
    def mq(self, mq: str):
        self._mq = mq

    @property
    def bagni(self):
        return self._bagni

    @bagni.setter
    def bagni(self, bagni: str):
        self._bagni = bagni

    @property
    def piano(self):
        return self._piano

    @piano.setter
    def piano(self, piano: str):
        self._piano = piano

    @staticmethod
    def from_dict(casa_dict: Dict):

        casa = CasaImmobiliare(id_immobiliare=casa_dict["_id_immobiliare"], crawling_date=casa_dict["_crawling_date"])
        if "_link" in casa_dict:
            casa.link = casa_dict["_link"]

        if "_titolo" in casa_dict:
            casa.titolo = casa_dict["_titolo"]

        if "_prezzo" in casa_dict:
            casa.prezzo = int(casa_dict["_prezzo"])

        if "_stanze" in casa_dict:
            casa.stanze = casa_dict["_stanze"]

        if "_mq" in casa_dict:
            casa.mq = casa_dict["_mq"]

        if "_bagni" in casa_dict:
            casa.bagni = casa_dict["_bagni"]

        if "_piano" in casa_dict:
            casa.piano = casa_dict["_piano"]

        return casa


class Zona:
    def __init__(self, id_zona: str, nome_zona: str, comune: str):
        self.id_zona = id_zona
        self.nome_zona = nome_zona
        self.comune = comune