import io


def generate_csv(items, fields, delimiter=','):
    return '\n'.join(map(lambda item: f"{delimiter.join(list(map(lambda x: str(getattr(item, x, '')) or '', fields)))}\n", items))