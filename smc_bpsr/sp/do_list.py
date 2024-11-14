import os

def generate_index(directory):
    with open(os.path.join(directory, 'index.html'), 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head><title>Directory Listing</title></head>\n<body>\n')
        f.write('<h1>Directory Listing</h1>\n<ul>\n')
        
        for item in os.listdir(directory):
            if item == 'index.html':
                continue
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                f.write(f'<li><a href="{item}/">{item}/</a></li>\n')
            else:
                f.write(f'<li><a href="{item}">{item}</a></li>\n')
        
        f.write('</ul>\n</body>\n</html>')

# Run the script in the current directory
generate_index('.')

