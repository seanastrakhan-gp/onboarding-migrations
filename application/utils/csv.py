import io


def generate_csv(items, fields, delimiter=','):
    f = io.StringIO()
    for item in items:
        f.write(f"{','.join(list(map(lambda x: item.get(x) or '', fields)))}\n")
    return f