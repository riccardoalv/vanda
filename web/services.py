import requests
import logging
import os
from Bio import Entrez
from dotenv import load_dotenv

load_dotenv()

Entrez.email = os.getenv("EMAIL")


def search_snp(query):
    url = f"https://clinicaltables.nlm.nih.gov/api/snps/v3/search?terms={query}&maxList=500"
    response = requests.get(url)

    r = []
    if response.status_code == 200:
        r = response.json()
    else:
        logging.error(
            f"Resonse code on services.search_snp: {response.status_code}")

    return r[3]


class SnpData:
    def __init__(self, snpid):
        self.snpid = snpid

        result = ''

        with Entrez.esummary(db="snp", id=snpid) as handle:
            result = Entrez.read(handle)

        self.data = result

    def get_snp_hgvs(self):
        hgvs = self.data["DocumentSummarySet"]['DocumentSummary'][0]['DOCSUM'][5:].split("|")[
            0].split(',')

        return hgvs


def get_abstracts_by_snp(snpid):
    article_ids = []

    with Entrez.elink(dbfrom="snp", db="pubmed", id=snpid, retmode="xml") as handle:
        article_ids = Entrez.read(handle)

    articles = []
    with Entrez.efetch(db="pubmed", id=article_ids, retmode="xml") as handle:
        articles = Entrez.read(handle)

    abstracts = []

    for article in articles['PubmedArticle']:
        if "Abstract" in article["MedlineCitation"]["Article"]:
            abstracts.append({
                str(article["MedlineCitation"]["PMID"]): [
                    article["MedlineCitation"]["Article"]["ArticleTitle"],
                    str(article["MedlineCitation"]["Article"]
                        ["Abstract"]["AbstractText"][0])
                ]
            })

    return abstracts
