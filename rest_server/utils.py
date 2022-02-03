def model2str(model, model_name=None, fields=None):
    if model_name is None:
        model_name = model.__class__.__name__
    field_value_strs = []

    if fields is None:
        fields = model._meta.fields

    for field in fields:
        if isinstance(field, str):
            field_name = field
        elif hasattr(field, 'name'):
            field_name = field.name
        else:
            raise RuntimeError('Unexpected filed types')
        v = getattr(model, field_name)
        v_str = f'"{v}"' if isinstance(v, str) else v
        field_value_strs.append(f'{field_name}: {v_str}')

    return f'{model_name} ({", ".join(field_value_strs)})'