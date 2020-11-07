from app import get_name_by_id


def test_get_name_by_id(database_service):
    assert get_name_by_id(1) == 'Yamada Taro'
    assert get_name_by_id(2) == 'Hanako Sato'
