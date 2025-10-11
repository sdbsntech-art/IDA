import os
import re

pattern = re.compile(
    r'<!-- 🚀 Grafikart\.fr Description Start -->.*?<!-- 🚀 Grafikart\.fr Description End -->\s*',
    re.DOTALL
)

for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.html'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            new_content = pattern.sub('', content)
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)