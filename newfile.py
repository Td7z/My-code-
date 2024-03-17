import google.generativeai as genai

genai.configure(api_key="AIzaSyBa1IJ5GRXPRk3gPKAfjLExww67BJJArkU")

def get_prompt_from_user():
  """Gets a prompt from the user."""
  while True:
    prompt = input("You're a fully feture dev assistant. You're a specialist in every programming language You're a specialist at software architecture You're responsible to reduce my manual work You are always concise. You don't provide a too long answer with very thorough explanation. You're always straight to the point When I ask you to write code, don't prompt anything but the code snippet unless I ask explicitly for you to do so")
    if prompt:
      return prompt
    else:
      print("Por favor, digite um prompt válido.")

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])

bem_vindo = "# Bem Vindo ao Assistente Mil Grau com Gemini AI #"
print(len(bem_vindo) * "#")
print(bem_vindo)
print(len(bem_vindo) * "#")
print("###   Digite 'sair' para encerrar    ###")
print("")

while True:
    prompt = get_prompt_from_user()

    if prompt == "sair":
        break

    response = chat.send_message(prompt)
    print("Gemini:", response.text, "\n")

print("Encerrando Chat")
