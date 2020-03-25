import requests
from Levenshtein import ratio

class UnescoReconciliationService:
    """
    API wrapper for the UNESCO thesaurus search api
    """
    
    API = "http://vocabularies.unesco.org/browser/rest/v1/search?query=*{q}*&vocab=thesaurus&lang=en&labellang=en"
    
    ENTRY_API = "http://vocabularies.unesco.org/browser/rest/v1/thesaurus/data?uri=http%3A%2F%2Fvocabularies.unesco.org%2Fthesaurus%2F{concept_id}&format=application/ld%2Bjson"


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
                "id": entry["uri"].split("/")[-1],
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


    def preview(self, concept_id):
        rsp = requests.get(self.ENTRY_API.format(concept_id=concept_id))
        data = rsp.json()

        for entry in data["graph"]:
            if entry["uri"].endswith(concept_id):
                preview_content = "<h3>"+concept_id+"</h3><div><ul>"
                for label in entry["prefLabel"]:
                    preview_content += "<li>{} ({})</li>".format(
                        label["value"], label["lang"]
                    )
                preview_content += "</ul></div>"

                break

        return preview_content