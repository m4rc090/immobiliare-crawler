from datetime import datetime
from typing import List

from bson import ObjectId
from pymongo import DESCENDING, MongoClient

from immobiliare_crawler.config.app_config import MONGO_HOST, MONGO_PORT, MONGO_DB
from immobiliare_crawler.config.app_constants import collection_utenti, collection_case, collection_utenti2case
from immobiliare_crawler.model.models import CasaImmobiliare, Utente, Utente2Casa


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

    def getbycondition(self, collection, condition_dict):
        coll = self.__getcoll(collection)
        el = coll.find_one(condition_dict)
        if not el:
            raise Exception(f"Element not found")
        el["_id"] = str(el["_id"])
        return el

    def findandupdate(self, collection, condition_dict, update_dict):
        self.__getcoll(collection).find_one_and_update(filter=condition_dict, update={"$set": update_dict}, upsert=True)

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

    def __init__(self, collection: str = collection_case, host: str = MONGO_HOST, port: int = MONGO_PORT, db: str = MONGO_DB):
        super().__init__(host=host, port=port, db=db)
        self.collection = collection

    def get_casa_by_id_sorgente(self, id_sorgente: str):
        resp = list(self.query(collection=self.collection, q={"_id_sorgente": id_sorgente}))
        if len(resp) > 0:
            return CasaImmobiliare.from_dict(resp[0])
        else:
            raise Exception("Casa with id_sorgente {} not found".format(id_sorgente))

    def save_case(self, casa: CasaImmobiliare):
        resp = list(self.query(collection=self.collection, q={"_id_sorgente": casa.id_sorgente}))
        if len(resp) == 0:
            self.save(collection=self.collection, obj=casa.__dict__)
            print("Save di casa {}".format(casa.id_sorgente))
            return self.get_casa_by_id_sorgente(casa.id_sorgente)
        elif len(resp) > 0:
            item = resp[0]
            if item["_prezzo"] != casa.prezzo:
                casa.id = item["_id"]
                self.save(collection=self.collection, obj=casa.__dict__)
                print("Save di casa {}".format(casa.id_sorgente))
                return self.get_casa_by_id_sorgente(casa.id_sorgente)
            else:
                print("Casa {} con stesso prezzo già salvato".format(casa.id_sorgente))
                return None

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


class UtentiDao(MongoDAO):
    def __init__(self, collection: str = collection_utenti, host: str = MONGO_HOST,
                 port: int = MONGO_PORT, db: str = MONGO_DB):
        super().__init__(host=host, port=port, db=db)
        self.collection = collection

    def save_utente(self, utente: Utente):
        self.findandupdate(collection=self.collection,
                           condition_dict={"_nome": utente.nome}, update_dict=utente.__dict__)

    def delete_utenti_collection(self):
        self.drop(self.collection)

    def all_utenti(self) -> List[Utente]:

        tot_num = self.count(self.collection)
        rows = 500
        start = 0
        while start <= tot_num:
            for u in self.all(self.collection, start, rows):
                yield Utente.from_dict(u)
            start += rows


class Utenti2CaseDao(MongoDAO):
    def __init__(self, collection: str = collection_utenti2case, host: str = MONGO_HOST,
                 port: int = MONGO_PORT, db: str = MONGO_DB):
        super().__init__(host=host, port=port, db=db)
        self.collection = collection

    def get_case_by_utente(self, id_utente: str):
        resp = list(
            self.query(collection=self.collection,
                       q={"_id_utente": id_utente}))
        return [utente2casa["_id_casa"] for utente2casa in resp]

    def save_utente2casa(self, utente2casa: Utente2Casa):
        resp = list(
            self.query(collection=self.collection, q={"_id_utente": utente2casa.id_utente, "_id_casa": utente2casa.id_casa}))
        if len(resp) == 0:
            self.save(collection=self.collection, obj=utente2casa.__dict__)

    def delete_utente2case_collection(self):
        self.drop(self.collection)

    def delete_utenti2case(self, id_casa: str):
        self.delete_by_conditiondict(collection=self.collection, condition_dict={"_id_casa": id_casa})

    def delete_utente2case(self, id_utente: str, id_casa: str):
        self.delete_by_conditiondict(collection=self.collection, condition_dict={"_id_utente": id_utente,
                                                                                 "_id_casa": id_casa})

    def all_utenti2case(self) -> List[Utente]:

        tot_num = self.count(self.collection)
        rows = 500
        start = 0
        while start <= tot_num:
            for u2c in self.all(self.collection, start, rows):
                yield Utente2Casa.from_dict(u2c)
            start += rows