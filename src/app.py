from models.user import User


# とりあえのロジックね
def get_name_by_id(id):
    name = User.query.filter(User.id == id).first().name
    return name
