import re


def prerpocess_json(in_filepath: str, out_filepath: str) -> None:
    pattern = re.compile(' NumberInt\([\d]+\)')

    with open(out_filepath, 'w') as outfile:
        with open(in_filepath, 'r') as infile:
            buf = ""
            for line in infile:
                if len(line) > 0:
                    if line[0] == '{':
                        buf = line.strip()
                    elif line[0] == '}':
                        buf += line.strip()
                        outfile.write(buf + '\n')
                    else:
                        line = line.strip()
                        res = re.search(pattern, line)
                        if res:
                            line = line[:res.start(
                            )] + ' ' + line[res.start() + 11:res.end() - 1] + line[res.end():]
                        buf += line
