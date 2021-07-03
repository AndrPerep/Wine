from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
from dotenv import load_dotenv
load_dotenv()

excel_file = 'wine.xlsx'

def age():
	creation_year = 1920
	today_year = datetime.date.today().year
	age = today_year - creation_year
	return age

def render_page(sorted_assortment, env):
	template = env.get_template('template.html')

	rendered_page = template.render(
	  age=age(),
	  sorted_assortment=sorted_assortment
	)

	with open('index.html', 'w', encoding="utf8") as file:
	    file.write(rendered_page)

def main():
	excel_data_df = pandas.read_excel(excel_file, na_values='None', keep_default_na=False)

	categories = excel_data_df['Категория'].tolist
	wines = excel_data_df.to_dict(orient='records')

	env = Environment(
	    loader=FileSystemLoader('.'),
	    autoescape=select_autoescape(['html', 'xml'])
	)

	assortment = collections.defaultdict(list)
	for wine in wines:
	  assortment[wine['Категория']].append(wine)

	sorted_assortment = sorted(assortment.items())

	render_page(sorted_assortment, env)
	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()

