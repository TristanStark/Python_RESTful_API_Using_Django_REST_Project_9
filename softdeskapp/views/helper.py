
def is_project_member(user, project):
    return (
        project.author_user == user
        or project.contributors.filter(id=user.id).exists()
    )
