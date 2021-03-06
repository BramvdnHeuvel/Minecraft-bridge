import os
import config

def rewriter(file_name):
    """Create a decorator that rewrites a file based on given settings."""

    def exec(func):
        """Rewrite a file"""
        new_lines = []

        info_to_remember = {}
        line_no = 0

        with open(file_name, 'r', encoding='utf-8') as open_file:
            for line in open_file:
                line_no += 1
                new_line = func(line, line_no, data=info_to_remember)
                new_lines.append(new_line)
        
        with open(file_name, 'w', encoding='utf-8') as write_file:
            for line in new_lines:
                write_file.write(line)
    return exec

@rewriter('eula.txt')
def confirm_eula(line : str, line_no : int, data):
    """Confirm the Minecraft EULA"""
    if os.getenv('EULA') is None or os.getenv('EULA').lower() != 'true':
        return line
    else:
        return line.replace('eula=false', 'eula=true')

@rewriter('server.properties')
def fill_in_server_settings(line : str, line_no : int, data):
    """Set up the server based on our chosen properties"""
    if line.strip().startswith('#'):
        return line
    
    value = line.split('=')[0]

    if value in config.SERVER_SETTINGS:
        return value + '=' + str(config.SERVER_SETTINGS[value]) + '\n'
    else:
        return line