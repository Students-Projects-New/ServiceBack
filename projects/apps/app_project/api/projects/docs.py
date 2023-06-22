import coreapi

class ProjectDocs():
    def get_fieldsCustom():
        return [
            coreapi.Field('id_user'),
            coreapi.Field('context'),
            coreapi.Field('port_container'),
            coreapi.Field('url'),
            coreapi.Field('static_path'),
        ] 

class DeployProjectDocs():
    def get_fieldsCustom():
        return [
            coreapi.Field('id_user'),
            coreapi.Field('id_project'),
        ]

class DeleteWorkspaceProjectDocs():
    def get_fieldsCustom():
        return [
            coreapi.Field('id_user'),
            coreapi.Field('id_project'),
        ] 