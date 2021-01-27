import decimal


def result_set_to_dict(cursor):
    result_list = []
    col_names = [col.name for col in cursor.description]
    for week in cursor.fetchall():
        result = {}
        for i, val in enumerate(week):
            if type(val) == decimal.Decimal:
                val = float(val)
            result[col_names[i]] = val

        result_list.append(result)

    return result_list
