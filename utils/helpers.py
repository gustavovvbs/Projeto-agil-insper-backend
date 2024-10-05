def is_coordination(claims):
    return claims.get('role') == 'coordination'

def is_professor(claims):
    return claims.get('role') == 'professor'

def is_student(claims):
    return claims.get('role') == 'student'