from mini_cross.cross_engine import MiniCross


def test_clickhouse_table_creation():
    columns = ['name', 'address']
    keys = ['address']
    MiniCross.create_clickhouse_table('table', columns=columns, keys=keys)
    table = MiniCross.load_clickhouse_table('table')
    assert len(table.columns()) == len(columns)
    assert all([x == y for x, y in zip(table.columns(), columns)])


def test_clickhouse_table_insert():
    columns = ['name', 'address']
    keys = ['address']
    MiniCross.create_clickhouse_table('table', columns=columns, keys=keys)
    table = MiniCross.load_clickhouse_table('table')
    table.insert([{
        'name': 'Leo',
        'address': "Hanoi"
    }])
    assert table.rows()[0]['name'] == 'Leo'
    assert table.rows()[0]['address'] == 'Hanoi'