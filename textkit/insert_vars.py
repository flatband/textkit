def insert_vars(template: str, variables: dict, defaults: dict = None) -> str:
    defaults = defaults or {}
    for key in {**defaults, **variables}:
        value = variables.get(key)
        if value is None:
            if key not in defaults or defaults[key] is None:
                raise ValueError(f"No value for '{key}' and no default provided.")
            value = defaults[key]
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template