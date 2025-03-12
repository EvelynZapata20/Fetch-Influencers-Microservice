def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def dict_keys_to_camel(d):
    return {snake_to_camel(k): v for k, v in d.items()}

def influencers_to_camel(influencers):
    return [dict_keys_to_camel(inf.dict()) for inf in influencers]
