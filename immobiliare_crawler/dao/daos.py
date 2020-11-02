import json
from datetime import datetime
from typing import List

import requests
from bson import ObjectId
from pymongo import DESCENDING, MongoClient

from immobiliare_crawler.config.app_config import MONGO_HOST, MONGO_PORT, MONGO_DB
from immobiliare_crawler.model.models import CasaImmobiliare, Zona


class MongoDAO:

    def __init__(self, host="localhost", port=27017, db="database"):
        self.db = db
        self.host = host
        self.port = port
        self.client = MongoClient(host=self.host, port=self.port)

    def save(self, collection, obj):
        coll = self.__getcoll(collection)

        if not type(obj) == list:
            obj = [obj]

        obj_to_insert = [o for o in obj if "_id" not in o]

        obj_to_update = [o for o in obj if "_id" in o]

        # insert on object without "_id" field
        if len(obj_to_insert) > 0:
            coll.insert(obj_to_insert, check_keys=False)

        # update on object with "_id" field
        for o in obj_to_update:
            id_ob = o["_id"]
            del o["_id"]
            try:
                doc = coll.find_one_and_update(
                    {"_id": ObjectId(id_ob)},
                    {"$set": o}, upsert=True)
                if not doc:
                    coll.insert(o, check_keys=False)
            except:
                coll.insert(o, check_keys=False)

    def update_by_id(self, collection, id, update_dict):
        coll = self.__getcoll(collection)
        coll.find_one_and_update({"_id": ObjectId(id)}, {"$set": update_dict}, upsert=True)

    def update_by_conditiondict(self, collection, condition_dict, update_dict):
        coll = self.__getcoll(collection)
        coll.update_one(condition_dict, {"$set": update_dict}, upsert=True)

    def delete(self, collection, id):
        coll = self.__getcoll(collection)
        coll.remove({"_id": ObjectId(id)})

    def delete_by_conditiondict(self, collection, condition_dict):
        coll = self.__getcoll(collection)
        coll.remove(condition_dict, True)

    def all(self, collection, start: int = 0, rows: int = None, selection=None):
        coll = self.__getcoll(collection)
        if rows:
            for el in coll.find(None, selection).skip(start).limit(rows):
                el["_id"] = str(el["_id"])
                yield el
        else:
            for el in coll.find().skip(start):
                el["_id"] = str(el["_id"])
                yield el

    def getbyid(self, collection, id):
        coll = self.__getcoll(collection)
        el = coll.find_one({"_id": ObjectId(id)})
        if not el:
            raise Exception("Element with id " + str(id) + " not found")
        el["_id"] = str(el["_id"])
        return el

    def collections(self):
        return self.client.get_database(self.db).collection_names()

    def drop(self, collection):
        coll = self.__getcoll(collection)
        coll.drop()

    def __getcoll(self, collection):
        return self.client.get_database(self.db).get_collection(collection)

    def sample(self, collection, n):
        coll = self.__getcoll(collection)
        for el in coll.aggregate([{"$sample": {"size": n}}]):
            el["_id"] = str(el["_id"])
            yield el

    def query(self, collection, q):
        coll = self.__getcoll(collection)
        for el in coll.find(q):
            el["_id"] = str(el["_id"])
            yield el

    def copy(self, collection1, collection2):
        coll1 = self.__getcoll(collection1)
        coll2 = self.__getcoll(collection2)
        coll2.remove()
        for el in coll1.find():
            coll2.insert(el)

    def count(self, collection):
        return self.__getcoll(collection).count()

    def get_last(self, collection, q: {} = None):
        coll = self.__getcoll(collection)
        return coll.find_one(q, sort=[('_id', DESCENDING)])


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
        self.base_url = base_url
        self.comune = None
        self.id2name = dict()
        self.__parse_url(self.base_url)

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


if __name__ == '__main__':
    # dao = ImmobiliareCaseDao(collection="case_collection_1")
    # dt = datetime.now()
    # dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    # print(dt)
    # print(list(dao.all_case_by_date(dt)))
    # dao.delete_case()
    # print(list(dao.all_case()))

    dao = ZoneRomaDao()