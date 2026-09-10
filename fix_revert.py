content = open('templates/pages/home.html', encoding='utf-8').read()
content = content.replace(
    "style=\"background-image:url('{% static \\'images/hero-group.jpg\\' %}'")\"",
    "style=\"background-image:url('/static/images/hero-group.jpg')\""
).replace(
    "style=\"background-image:url('{% static \\'images/hero-outreach.jpg\\' %}'")\"",
    "style=\"background-image:url('/static/images/hero-outreach.jpg')\""
).replace(
    "style=\"background-image:url('{% static \\'images/hero-clinic.jpg\\' %}'")\"",
    "style=\"background-image:url('/static/images/hero-clinic.jpg')\""
)
open('templates/pages/home.html', 'w', encoding='utf-8').write(content)
print('Done')
