from django.test import TestCase, Client
from django.test.client import resolve
from django.urls import reverse
import entrez.services as ncbi

default_snp = "268"
snp_response = ['rs268', '8', '19956017', 'A/G', 'LPL']
hgvs_snp_response = ['NC_000008.11:g.19956018A>G',
                     'NC_000008.10:g.19813529A>G',
                     'NG_008855.2:g.59302A>G',
                     'NM_000237.3:c.953A>G',
                     'NM_000237.2:c.953A>G',
                     'NP_000228.1:p.Asn318Ser'
                     ]

snp = ncbi.SnpData(default_snp)


class ServicesTestCase(TestCase):

    def test_get_by_name(self):
        response = ncbi.search_snp("rs" + default_snp)

        self.assertListEqual(response["data"][0], snp_response)

    def test_get_snp_hgvs(self):
        self.assertListEqual(snp.get_snp_hgvs(), hgvs_snp_response)


class ViewTestCase(TestCase):

    def test_homepage(self):
        client = Client()

        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        client = Client()

        response = client.get('/search', {"q": default_snp})
        self.assertEqual(response.status_code, 200)

    def test_no_items_found(self):
        client = Client()

        response = client.get(
            '/search', {"q": "Lorem ipsum dolor sit amet, qui minim labore adipisicing minim sint cillum sint consectetur cupidatat."})
        self.assertEqual(response.status_code, 200)

    def test_snp(self):
        client = Client()

        response = client.get('/api/snp/' + default_snp + '/hgvs')
        self.assertEqual(response.status_code, 200)

    def test_snp_abstracts(self):
        client = Client()

        response = client.get('/api/snp/' + default_snp + '/abstracts')
        self.assertEqual(response.status_code, 200)

    def test_gene_abstracts(self):
        client = Client()

        response = client.get('/api/gene/' + default_snp + '/abstracts')
        self.assertEqual(response.status_code, 200)
