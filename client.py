import requests



response = requests.post("http://127.0.0.1:5000/api/advertisements",json={'title': 'Коржики вперед!', 'description': 'Самые сладкие коржики Сева, Лапа и Мишель', 'owner': 'мама Влада'})

#response = requests.get("http://127.0.0.1:5000/api/advertisements/4")

#response = requests.delete("http://127.0.0.1:5000/api/advertisements/1")
print(response.json())
print(response.status_code)


