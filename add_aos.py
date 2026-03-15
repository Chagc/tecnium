import os
import re

files_to_update = ['index.html', 'team.html', 'entregable1.html', 'entregable2.html']

for filename in files_to_update:
    filepath = os.path.join(r"c:\Users\aleja\OneDrive\Escritorio\Codigo\ITD\4 semestre\TECNIUM\tecnium", filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add CSS before closing </head>
    if 'aos.css' not in content:
        content = content.replace('</head>', '    <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet" />\n</head>')
    
    # 2. Add JS before closing </body>
    if 'aos.js' not in content:
        js_snippet = """
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init({
            duration: 800,
            once: true,
            offset: 100,
        });
    </script>
</body>"""
        # team.html has </body></html> on same line
        content = content.replace('</body>\n</html>', js_snippet + '\n</html>')
        content = content.replace('</body></html>', js_snippet + '</html>')
        if '</body>' in content and 'aos.js' not in content:
            content = content.replace('</body>', js_snippet)
    
    # 3. Add data-aos to header
    header_pattern = re.compile(r'<header([^>]*class="[^"]*sticky[^"]*"[^>]*)>')
    content = header_pattern.sub(r'<header data-aos="fade-down"\1>', content)
    
    # 4. Add data-aos to Hero section
    # Hero in entregables: class="bg-surface-light dark:bg-surface-dark border-b border-border-light ...
    # Hero in index: <section class="relative overflow-hidden pt-12 pb-20 lg:pt-24 lg:pb-12 bg-white">
    # Hero in team: <section class="w-full bg-white dark:bg-neutral-surface-dark py-16 px-6 border-b ...
    
    if filename == 'index.html':
        content = content.replace('<section class="relative overflow-hidden pt-12 pb-20 lg:pt-24 lg:pb-12 bg-white">', 
                                  '<section data-aos="zoom-in" class="relative overflow-hidden pt-12 pb-20 lg:pt-24 lg:pb-12 bg-white">')
        content = content.replace('<section class="py-20 bg-white relative">', 
                                  '<section data-aos="fade-up" class="py-20 bg-white relative">')
    elif filename == 'team.html':
        content = content.replace('<section class="w-full bg-white dark:bg-neutral-surface-dark py-16 px-6 border-b', 
                                  '<section data-aos="zoom-in" class="w-full bg-white dark:bg-neutral-surface-dark py-16 px-6 border-b')
        content = content.replace('<div class="w-full max-w-[960px] mx-auto px-6 py-16 grid grid-cols-2 md:grid-cols-3 gap-12 text-center">', 
                                  '<div data-aos="fade-up" class="w-full max-w-[960px] mx-auto px-6 py-16 grid grid-cols-2 md:grid-cols-3 gap-12 text-center">')
    else:
        # For entregable1 and entregable2
        hero_pattern = re.compile(r'<div\s*class="bg-surface-light dark:bg-surface-dark border-b')
        if 'data-aos="zoom-in"' not in content:
            content = hero_pattern.sub(r'<div data-aos="zoom-in"\n            class="bg-surface-light dark:bg-surface-dark border-b', content, count=1)
        
        # All <section ...> that don't have data-aos. They usually have class="py-12 px-4...
        # Using negative lookahead to prevent double-adding
        section_pattern = re.compile(r'<section(?!\s+data-aos)([\s\S]*?)>')
        content = section_pattern.sub(r'<section data-aos="fade-up"\1>', content)

    # Save content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done updating files")
