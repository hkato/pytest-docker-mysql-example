from models.users import Users


# とりあえのロジックね
def get_name_by_id(id):
    name = Users.query.filter(Users.id == id).first().name
    return name
