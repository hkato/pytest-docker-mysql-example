def test_get_name_by_id(database_service):
    # ファイルの頭で import するとSQLAlchemyによりコンテナ起動前に接続される。
    # テストではメソッドの中で使うときに import する。
    from app import get_name_by_id

    assert get_name_by_id(1) == 'ed'
    assert get_name_by_id(2) == 'wendy'
    assert get_name_by_id(3) == 'mary'
    assert get_name_by_id(4) == 'fred'
