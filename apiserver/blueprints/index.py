from flask import Blueprint, render_template, current_app
import re

index = Blueprint('index', __name__)


@index.route('/')
def show_index():
    ui_urls = []
    uire = re.compile(r'/ui/$')  # Define the regex pattern that matches UI's
    title = 'Index'
    all_urls = current_app.url_map  # This iterable object knows all registered urls
    for current_url in all_urls.iter_rules():
        if uire.findall(current_url.rule):  # Check against the pattern
            ui_urls.append(current_url.rule)  # On match, we add this url to our ui url list
    return render_template('index.j2.html', title=title, ui_urls=ui_urls)
