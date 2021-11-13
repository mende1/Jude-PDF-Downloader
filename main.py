import os
import pathlib
import json
import requests
from PyInquirer import prompt

from examples import custom_style_3


JUDE_URL = 'http://200.128.51.30'


questions = {
	'contest': {
		'type': 'list',
		'name': 'contest',
		'message': 'Selecione o Contest:',
		'choices': []
	},
	'auth_login': {
		'type': 'input',
		'name': 'login',
		'message': 'Login: '
	},
	'auth_passwd': {
		'type': 'password',
		'name': 'password',
		'message': 'Password: '
	},
	'problems': {
		'type': 'checkbox',
		'name': 'problems',
		'message': 'Problemas a serem baixados: ',
		'choices': []
	},
	'path': {
		'type': 'input',
		'name': 'path',
		'message': 'Diretório para Download dos PDFs: ',
	}
}



def main():

	session = requests.Session()

	json_data = session.get(JUDE_URL + "/contest-list").content
	list_contests = json.loads(json_data)["contests"]

	list_contests.sort(key = lambda x : x['start_time'])
	list_contests.sort(key = lambda x : x['end_time'], reverse=True)

	dict_contests = {}

	for contest in list_contests:
		name = contest['name']
		dict_aux = { name: contest }
		dict_contests.update(dict_aux)

	for name, contest in dict_contests.items():
		questions['contest']['choices'].append(contest['name'])

	main_name = prompt(questions['contest'], style=custom_style_3)['contest']

	main_contest = dict_contests[main_name]

	login  = prompt(questions['auth_login'], style=custom_style_3)['login']
	passwd = prompt(questions['auth_passwd'], style=custom_style_3)['password']

	data = {
		"handle": login,
		"password": passwd,
		"contest": main_contest['_id']
	}

	session.post(JUDE_URL + "/api-login", data=data)

	problems = main_contest['problems']

	for problem in problems:
		letter = problem['letter']
		dict_aux = { 'name': letter}
		questions['problems']['choices'].append(dict_aux)

	download_problems = prompt(questions['problems'], style=custom_style_3)

	# PATH CHOICE

	print("Exemplo Linux: /home/mendel/Desktop")
	print("Exemplo Windows: C:\\Users\\mendel\\Desktop")

	path = prompt(questions['path'], style=custom_style_3)['path']

	# DOWNLOAD PDF

	for problem in download_problems['problems']:
		pdf = session.get(JUDE_URL + "/contest/statement/" + problem)

		try:
			with open(f"{path}/{problem}.pdf", 'wb') as f:
				f.write(pdf.content)
			print(f"Problema {problem} baixado com sucesso ✔️")
		
		except IOError:
			print("error ao baixar")


	f.close()


if __name__ == '__main__':
    main()