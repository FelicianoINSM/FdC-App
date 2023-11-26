def get_config(keyword):
    with open('./server/server.config', 'r') as file:
        for line in file:
            if not (line.startswith('//') or line.isspace()):
                try:
                    key, val = line.split('=')
                    key = key.strip()
                    val = val.strip()
                    if key == keyword:
                        return val
                except ValueError:
                    pass
