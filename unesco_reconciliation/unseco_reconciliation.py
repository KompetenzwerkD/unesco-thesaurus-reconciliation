import requests
from Levenshtein import ratio

class UnescoReconciliationService:
    """
    API wrapper for the UNESCO thesaurus search api
    """
    
    API = "http://vocabularies.unesco.org/browser/rest/v1/search?query=*{q}*&vocab=thesaurus&lang=en&labellang=en"
    
    def __init__(self):
        pass

    def _query(self, q):
        rsp = requests.get(self.API.format(q=q))
        data = rsp.json()

        results = []
        for entry in data["results"][:5]:
            match = False
            score = ratio(q.lower(), entry["prefLabel"].lower())
            if score == 1:
                match = True
            results.append({
                "id": entry["uri"],
                "name": entry["prefLabel"],
                "type": [ "http://www.w3.org/2004/02/skos/core#Concept" ],
                "score": score,
                "match": match
            })

        return results

    def query_batch(self, queries):

        results = {}
        for key, query in queries.items():
            print(key)
            print(query)
            results[key] = {
                "result": self._query(query["query"])
            }
        print(results)
        return results
    