from myapp.apis.user import get_name_by_id


def test_get_name_by_id(database_service):
    assert get_name_by_id(1).name == 'ed'
    assert get_name_by_id(2).name == 'wendy'
    assert get_name_by_id(3).name == 'mary'
    assert get_name_by_id(4).name == 'fred'
