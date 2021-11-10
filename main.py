import json
import requests

url = "http://200.128.51.30"

s = requests.Session()

json_data = s.get(url + "/contest-list").content
contests = json.loads(json_data)["contests"]

contests.sort(key = lambda x : x['start_time'])
contests.sort(key = lambda x : x['end_time'], reverse=True)

for index, contest in enumerate(contests):
	print(f"[{index:2}] {contest['name']}")
	if index > 15:
		break

print("=" * 80, end="\n\n")

n = int(input("Contest: "))
print()

print("=" * 80, end="\n\n")
print("Auth - Contest:", contests[n]['name'])

login  = input("Login: ")
passwd = input("Password: ")

data = {
	"handle": login,
	"password": passwd,
	"contest": contests[n]['_id']
}

s.post(url + "/api-login", data=data)

problems = contests[n]['problems']

for i in range(len(problems)-1):
	print(f"[{i:2}] {problems[i]['letter']}")

print("=" * 80, end="\n\n")

inicio = int(input("Intervalo inicial: "))
fim    = int(input("Intervalo   final: "))
path   = input("Escolha o caminho a ser baixado: ")
print()

# DOWNLOAD PDF


for i in range(inicio, fim+1):
	pdf = s.get(url + "/contest/statement/" + problems[i]['letter'])

	with open(f"{path}/{problems[i]['letter']}.pdf", 'wb') as f:
		f.write(pdf.content)

f.close()
