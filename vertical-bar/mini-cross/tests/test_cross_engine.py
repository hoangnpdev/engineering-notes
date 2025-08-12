from mini_cross.cross_engine import MiniCross

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