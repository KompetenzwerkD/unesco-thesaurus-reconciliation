import requests



class UnescoReconciliationService:
    """
    API wrapper for the UNESCO thesaurus search api
    """
    
    API = "http://vocabularies.unesco.org/browser/rest/v1/search?query=*{q}*&vocab=thesaurus&lang=&labellang="
    
    def __init__(self):
        pass

    def query(self, q):
        """
        Query the UNESCO thesaurus api and returns a reconciliation result set
        """

        rsp = requests.get(self.API.format(q=q))
        data = rsp.json()

        return data

    