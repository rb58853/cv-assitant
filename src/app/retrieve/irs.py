from data.projects import projects


class IRS:
    def __init__(self) -> None:
        self.documents = None
        self.set_ducuments()

    def set_ducuments(self):
        self.documents = projects.values()

    def get_documents_from_query(self, query):
        # TODO Aqui hay que hacer un IRS
        return self.documents
