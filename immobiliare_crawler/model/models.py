from datetime import datetime
from typing import Dict, List


class CasaImmobiliare:
    def __init__(self, id_immobiliare: str):
        self._id_immobiliare = id_immobiliare
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

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @staticmethod
    def from_dict(casa_dict: Dict):

        casa = CasaImmobiliare(id_immobiliare=casa_dict["_id_immobiliare"])
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

        if "_id" in casa_dict:
            casa.id = casa_dict["_id"]

        return casa


class Zona:
    def __init__(self, id_zona: str, nome_zona: str, comune: str):
        self.id_zona = id_zona
        self.nome_zona = nome_zona
        self.comune = comune


class Utente:
    def __init__(self, emails: List[str],
                 prezzo_minimo: int = None,
                 prezzo_massimo: int = None,
                 superficie_minima: int = None,
                 superficie_massima: int = None,
                 zone_text: List[str] = None):
        self._emails = emails
        self._prezzo_minimo = prezzo_minimo
        self._prezzo_massimo = prezzo_massimo
        self._superficie_minima = superficie_minima
        self._superficie_massima = superficie_massima
        self._zone_text = zone_text

    @property
    def emails(self):
        return self._emails

    @emails.setter
    def emails(self, emails: List[str]):
        self._emails = emails

    @property
    def zone_text(self):
        return self._zone_text

    @zone_text.setter
    def zone_text(self, zone_text: List[str]):
        self._zone_text = zone_text

    @property
    def prezzo_minimo(self):
        return self._prezzo_minimo

    @prezzo_minimo.setter
    def prezzo_minimo(self, prezzo_minimo: str):
        self._prezzo_minimo = prezzo_minimo

    @property
    def prezzo_massimo(self):
        return self._prezzo_massimo

    @prezzo_massimo.setter
    def prezzo_massimo(self, prezzo_massimo: str):
        self._prezzo_massimo = prezzo_massimo

    @property
    def superficie_minima(self):
        return self._superficie_minima

    @superficie_minima.setter
    def superficie_minima(self, superficie_minima: str):
        self._superficie_minima = superficie_minima

    @property
    def superficie_massima(self):
        return self._superficie_massima

    @superficie_massima.setter
    def superficie_massima(self, superficie_massima: str):
        self._superficie_massima = superficie_massima

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @staticmethod
    def from_dict(utente_dict: Dict):

        utente = Utente(emails=utente_dict["_emails"])

        if "_prezzo_minimo" in utente_dict:
            utente.prezzo_minimo = utente_dict["_prezzo_minimo"]

        if "_prezzo_massimo" in utente_dict:
            utente.prezzo_massimo = utente_dict["_prezzo_massimo"]

        if "_superficie_minima" in utente_dict:
            utente.superficie_minima = utente_dict["_superficie_minima"]

        if "_superficie_massima" in utente_dict:
            utente.superficie_massima = utente_dict["_superficie_massima"]

        if "_zone_text" in utente_dict:
            utente.zone_text = utente_dict["_zone_text"]

        if "_id" in utente_dict:
            utente.id = utente_dict["_id"]

        return utente


class Utente2Casa:
    def __init__(self, id_utente: str, id_casa: str, send_date: datetime):
        self._id_utente = id_utente
        self._id_casa = id_casa
        self._send_date = send_date

    @property
    def id_utente(self):
        return self._id_utente

    @id_utente.setter
    def id_utente(self, id_utente: str):
        self._id_utente = id_utente

    @property
    def id_casa(self):
        return self._id_casa

    @id_casa.setter
    def id_casa(self, id_casa: str):
        self._id_casa = id_casa

    @property
    def send_date(self):
        return self._send_date

    @send_date.setter
    def send_date(self, send_date: datetime):
        self._send_date = send_date

    @staticmethod
    def from_dict(utente2casa_dict: Dict):
        u2c = Utente2Casa(id_utente=utente2casa_dict["_id_utente"], id_casa=utente2casa_dict["_id_casa"],
                          send_date=utente2casa_dict["_send_date"])
        return u2c
