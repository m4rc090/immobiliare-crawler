from immobiliare_crawler.business.daemons import JobCralwer

if __name__ == '__main__':
    job = JobCralwer(prezzo_minimo=160000,
                     prezzo_massimo=280000,
                     superficie_minima=40,
                     superficie_massima=100,
                     zone=[10169, 10153, 10154])

    job.run_crawler()
    job.generate_report("/home/marco/Desktop/")