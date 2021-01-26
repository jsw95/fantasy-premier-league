


def result_set_to_dict(cursor):
    result_list = []
    col_names = [col.name for col in cursor.description]
    for week in cursor.fetchall():
        res = {col_names[i]: val for i, val in enumerate(week)}
        result_list.append(res)

    return result_list
