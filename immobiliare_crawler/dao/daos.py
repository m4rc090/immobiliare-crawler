import json
from datetime import datetime
from typing import List

from ds4biz_commons.utils.requests_utils import URLRequest
from ds4biz_storage.dao.mongo_dao import MongoDAO

from immobiliare_crawler.config.app_config import MONGO_HOST, MONGO_PORT, MONGO_DB
from immobiliare_crawler.model.models import CasaImmobiliare, Zona


class ImmobiliareCaseDao(MongoDAO):

    def __init__(self, collection: str, host: str = MONGO_HOST, port: int = MONGO_PORT, db: str = MONGO_DB):
        super().__init__(host=host, port=port, db=db)
        self.collection = collection

    def save_case(self, casa: CasaImmobiliare):
        resp = list(self.query(collection=self.collection, q={"_id_immobiliare": casa.id_immobiliare, "_prezzo": casa.prezzo}))
        if len(resp) == 0:
            self.save(collection=self.collection, obj=casa.__dict__)
            print("Save di casa {}".format(casa.id_immobiliare))
        else:
            print("Casa {} con stesso prezzo già salvato".format(casa.id_immobiliare))

    def delete_case(self):
        self.drop(self.collection)

    def all_case(self) -> List[CasaImmobiliare]:

        tot_num = self.count(self.collection)
        rows = 500
        start = 0
        while start <= tot_num:
            for casa in self.all(self.collection, start, rows):
                yield CasaImmobiliare.from_dict(casa)

            start += rows

    def all_case_by_date(self, date: datetime) -> List[CasaImmobiliare]:

        q = {"_crawling_date": {"$gte": date}}
        for casa in self.query(self.collection, q):
            yield CasaImmobiliare.from_dict(casa)


# qui poi ci facciamo una bella factory per citta'
class ZoneRomaDao:
    def __init__(self, base_url: str = "https://www.immobiliare.it/services/geography/getGeography.php?action=getMacrozoneComune&idComune=6737"):
        self.url_request = URLRequest(base_url, response_converter=lambda response: response.text)
        self.comune = None
        self.id2name = dict()
        self.__parse_url(self.url_request)

    def __parse_url(self, url_req: URLRequest):
        response = json.loads(url_req.get())

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


if __name__ == '__main__':
    # dao = ImmobiliareCaseDao(collection="case_collection_1")
    # dt = datetime.now()
    # dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    # print(dt)
    # print(list(dao.all_case_by_date(dt)))
    # dao.delete_case()
    # print(list(dao.all_case()))

    dao = ZoneRomaDao()