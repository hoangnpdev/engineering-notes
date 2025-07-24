from mini_posgres.postgres_database import MiniPostgres
from mini_posgres.postgres_file import FileManager


def test_create_table():
    column_list = ['abc', 'def']
    MiniPostgres.create_table('table', column_list)
    loaded_column_list = MiniPostgres.load_table('table').columns()
    for col in loaded_column_list:
        print(col)
    assert len(loaded_column_list) == len(column_list)
    assert all([x == y for x, y in zip(loaded_column_list, column_list)])
    FileManager.destroy()


def test_insert_one_row():
    column_list = ['name', 'address']
    MiniPostgres.create_table('table', column_list)
    table = MiniPostgres.load_table('table')
    table.insert([{
        'name': 'Leo',
        'address': "Hanoi"
    }])
    assert table.rows()[0]['name'] == 'Leo'
    assert table.rows()[0]['address'] == 'Hanoi'
