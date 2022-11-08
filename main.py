import json
import requests
import questionary

from colorama import Fore

JUDE_URL = 'http://200.128.51.30'

custom_style = questionary.Style([
	('selected', 'bg:#fc0'),
	('selected', 'fg:#333'),
	('highlighted', 'bg:#222 bold'),
])

def login(session, main_contest):
	user = questionary.text('Login: ').ask()
	password = questionary.password('Password: ').ask()

	data = {
		"handle": user,
		"password": password,
		"contest": main_contest['_id']
	}

	response = session.post(JUDE_URL + "/api-login", data=data)

	try:
		response.raise_for_status()
		return data

	except requests.exceptions.RequestException as e:
		if e.response.status_code == 401:
			print(Fore.RED + 'Login incorreto, tente novamente!')
			login(session)
		
		print(Fore.RED + 'Error ' + str(e))
		exit()


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

	contests = []

	for name, contest in dict_contests.items():
		contests.append(contest['name'])

	main_name = questionary.select(
		'Selecione o Contest: ', 
		choices = contests,
		style=custom_style
	).ask()

	main_contest = dict_contests[main_name]

	list_problems = main_contest['problems']
	problems = []

	for problem in list_problems:
		letter = problem['letter']
		problems.append(letter)

	download_problems = questionary.checkbox(
		'Problemas para Download: ', 
		choices = problems,
		validate = lambda a : (
            True if len(a) > 0 else "Você precisa selecionar pelo menos um problema!"
        ),
		style=custom_style
	).ask()

	# AUTH
	login(session, main_contest)

	# PATH CHOICE
	path = questionary.path(
		'Diretório para Download dos PDFs:', 
		only_directories=True, 
		complete_style='MULTI_COLUMN',
		style=custom_style
	).ask()

	if path.endswith('/') or path.endswith('\\'):
		path.pop(len(path)-1)


	# DOWNLOAD PDF

	for problem in download_problems:
		pdf = session.get(JUDE_URL + "/contest/statement/" + problem)

		try:
			with open(f"{path}/{problem}.pdf", 'wb') as f:
				f.write(pdf.content)
			print(f"Problema {problem} baixado com sucesso ✔️")
		
		except IOError:
			print(f"Erro ao baixar arquivos ❌")
			return


if __name__ == '__main__':
    main()