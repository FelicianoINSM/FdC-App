PATH = './server/server.config'

def get_config(keyword):
    with open(PATH, 'r') as file:
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

def edit_config(keyword, new_value):
    with open(PATH, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if not (line.startswith('//') or line.isspace()):
            try:
                key, _ = line.split('=')
                if key.strip() == keyword:
                    lines[i] = f"{keyword} = {new_value}\n"
                    break
            except ValueError:
                pass
    else:
        lines.append(f"{keyword} = {new_value}\n")

    with open(PATH, 'w') as file:
        file.writelines(lines)
