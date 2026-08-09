import re

with open('requirements-dev.txt', 'r') as f:
    content = f.read()

content = content.replace("tenacity==9.0.0", "pyjwt>=2.13.0\ntenacity==9.0.0")

with open('requirements-dev.txt', 'w') as f:
    f.write(content)
