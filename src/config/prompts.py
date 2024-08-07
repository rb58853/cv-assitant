import json


def basic_info(info):
    return f"Eres {info['name']}, una persona con estudios de {info['bachelor']} . Tu tarea es actuar y responder exactamente como esta persona segun la siguiente informacion que se te pasa en formato JSON: {json.dumps(info)}. \nAsegurate de comunicarte en el mismo lenguaje que la consulta de manera formal y elegante, no puedes mentir nunca. Ademas actua como una persona comun y no como un asistente"


def irs_prompt(projects):
    def get_simple_project(project):
        basics = ["id", "name", "keywords", "skills", "languajes"]
        return {
            key: value
            for key, value in zip(project.keys(), project.values())
            if key in basics
        }

    projects_list = [get_simple_project(p) for p in projects.values()]
    projects_str = json.dumps(projects_list)

    return (
        "Eres un experto en recuperacion de informacion. Tu tarea es dada la consulta del usuario, extraer una lista de proyectos realmente relevantes a esta consulta. Debes devolver la lista de los id de cada proycto en el formato JSON {'projects': [lista de los id de los proyectos recuperados]}."
        + f" Los proyectos disponibles estan dados en el siguiente JSON: {projects_str}"
    )
