from models.estudante import Estudante

def get_by_id(id: str):
    estudante = Estudante.get_by_id(id)
    if not estudante:
        return {"message": "Estudante not found"}, 404

    return estudante.dict(), 200