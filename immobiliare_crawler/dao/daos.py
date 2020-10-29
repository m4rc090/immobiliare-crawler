from datetime import datetime, date
from typing import List

from ds4biz_storage.dao.mongo_dao import MongoDAO

from immobiliare_crawler.model.models import CasaImmobiliare


class ImmobiliareCaseDao(MongoDAO):

    def __init__(self, collection: str, host: str = "immobiliare_mongo", port: int = 37017, db: str = "imm_case_db"):
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


if __name__ == '__main__':
    dao = ImmobiliareCaseDao(collection="case_collection_1")
    # dt = datetime.now()
    # dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    # print(dt)
    # print(list(dao.all_case_by_date(dt)))
    # dao.delete_case()
    # print(list(dao.all_case()))
