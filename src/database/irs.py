class IRS:
    def __init__(self) -> None:
        pass

    def get_values_from_field(self, user_data, field):
        return user_data.get_info_from_fields([field])[field]

    def get_projects_from_query(self, query, user_data):
        # TODO Aqui hay que hacer un IRS
        projects = self.get_projects_from_user(user_data)
        return projects

    def get_projects_from_user(self, user_data, projects_field="projects"):
        return user_data.get_info_from_fields([projects_field])[projects_field]


irs = IRS()
