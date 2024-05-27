from core.db_connection import Table, Connection


if __name__ == "__main__":
    conn = Connection()
    conn.create_connection(db_port=5430, db_user='admin', db_passwd='admin',
                           db_name='lab8')
    conn.drop_all()
    conn.fill_default()
    conn.fill_data()

    args = Table(table_name='Заявки', args={
        'id': "'21'",
        'Name': "'Иванов Иван Иванович'",
        'Phone': "'1234567890'",
        'Receipt': "'1'",
        'Bank': "'Сбербанк'",
        'Account': "'12345678901234567890'",
        'Address': "'ул. Ленина, 1'",
        'District': "'Центральный'",
        'DateStart': "'2024-03-01'",
        'Document': "'Паспорт'",
        'Speed': "'1'",
        'DateStop': 'NULL',
        'Cost': "'10000'",
    })
    conn.add_new_transaction_query(args)

    args = Table(table_name='Выдача', args={
        'id': "'21'",
        'Finish': "'0'",
    })
    conn.add_new_transaction_query(args)

    conn.close_connection()
