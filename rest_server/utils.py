def model2str(model, model_name=None):
    if model_name is None:
        model_name = model.__class__.__name__
    field_value_strs = []

    for field in model._meta.fields:
        v = getattr(model, field.name)
        v_str = f'"{v}"' if isinstance(v, str) else v
        field_value_strs.append(f'{field.name}: {v_str}')

    return f'{model_name} ({", ".join(field_value_strs)})'