from src.interface import login

client = login()
print(client.fetch_student_data())
