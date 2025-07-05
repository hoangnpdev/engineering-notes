from executor.postgres_executor import QueryExecutor


def test_create_table():
    column_list = ['abc', 'def']
    QueryExecutor.create_table('table', column_list)
    loaded_column_list = QueryExecutor.list_column('table')
    assert len(loaded_column_list) == len(column_list)
    assert all([x == y for x, y in zip(loaded_column_list, column_list)])