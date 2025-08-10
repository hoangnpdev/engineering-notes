from mini_cross.cross_engine import MiniCross


def test_create_table():
    column_list = ['abc', 'def']
    MiniCross.create_postgres_table('table', column_list)
    loaded_column_list = MiniCross.load_postgres_table('table').columns()
    for col in loaded_column_list:
        print(col)
    assert len(loaded_column_list) == len(column_list)
    assert all([x == y for x, y in zip(loaded_column_list, column_list)])
    MiniCross.destroy()


def test_insert_one_row():
    column_list = ['name', 'address']
    MiniCross.create_postgres_table('table', column_list)
    table = MiniCross.load_postgres_table('table')
    table.insert([{
        'name': 'Leo',
        'address': "Hanoi"
    }])
    assert table.rows()[0]['name'] == 'Leo'
    assert table.rows()[0]['address'] == 'Hanoi'
    MiniCross.destroy()


def test_hash_aggregate():
    column_list = ['name', 'address']
    MiniCross.create_postgres_table('table', column_list)
    table = MiniCross.load_postgres_table('table')
    table.insert([
        {
            'name': 'Leo',
            'address': "Hanoi"
        },
        {
            'name': 'Harry',
            'address': "Hanoi"
        },
        {
            'name': 'Messi',
            'address': 'Hochiminh'
        }
    ])
    count_by_address_list = MiniCross.load_table_ref('table').hash_aggregate(['address'])
    for e in count_by_address_list:
        if e['address'] == 'Hanoi':
            assert e['count'] == 2
        if e['address'] == 'Hochiminh':
            assert e['count'] == 1

