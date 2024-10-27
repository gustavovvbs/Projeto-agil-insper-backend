ROLE_PERMISSIONS = {
    'estudante': {
        'can_view_projects': True,
        'can_apply_for_projects': True,
        'can_manage_projects': False
    },
    'professor': {
        'can_view_projects': True,
        'can_apply_for_projects': False,
        'can_manage_projects': True
    },
    'coordenador': {
        'can_view_projects': True,
        'can_apply_for_projects': False,
        'can_manage_projects': True,
        'can_manage_users': True,
        'can_manage_processo_seletivo': True,
        'can_manage_professores': True,
    }
}

def get_permissions(role):
    return ROLE_PERMISSIONS.get(role, {})