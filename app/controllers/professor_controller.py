from models.professor import Professor 

def get_by_id(id: str):
    professor = Professor.get_by_id(id)
    if not professor:
        return {"message": "Professor not found"}, 404

    return professor.dict(), 200

def get_all():
    professores = Professor.get_all()
    if not professores:
        return {"message": "No professors found"}, 404
    professores = [professor.dict() for professor in professores]
    return professores