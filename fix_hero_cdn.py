with open('templates/pages/home.html', encoding='utf-8') as f:
    content = f.read()
content = content.replace(
    "url('/static/images/hero-group.jpg')",
    "url('PASTE_CLOUDINARY_URL_HERE')"
).replace(
    "url('/static/images/hero-outreach.jpg')",
    "url('PASTE_CLOUDINARY_URL_HERE')"
).replace(
    "url('/static/images/hero-clinic.jpg')",
    "url('PASTE_CLOUDINARY_URL_HERE')"
)
with open('templates/pages/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
