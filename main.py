from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
from pprint import pprint
import collections
from dotenv import load_dotenv
load_dotenv()

excel_data_df = pandas.read_excel('wine3.xlsx', na_values='None', keep_default_na=False)

categories = excel_data_df['Категория'].tolist
wines = excel_data_df.to_dict(orient='records')


creation_year = 1920
today_year = datetime.date.today().year
age = today_year - creation_year

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

wine_categories = collections.defaultdict(list)
for wine in wines:
  wine_categories[wine['Категория']].append(wine)

sorted_wine_categories = sorted(wine_categories.items())


template = env.get_template('template.html')

rendered_page = template.render(
  age=age,
  wine_categories=wine_categories
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
