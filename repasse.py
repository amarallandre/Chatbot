import telebot
import datetime
import time
import threading

# Token do seu bot obtido no BotFather
bot_token = '6275773716:AAG-ECDpGoNMY3tCx6w_LVFpxtbBcuj6BFg'

# Criar uma instância do bot
bot = telebot.TeleBot(bot_token)

# Sala de destino para enviar os sinais
sala_destino =  -1001971572180  # ID da sala de destino

# Lista inicial de sinais
lista_sinais = []


# Comando para adicionar uma lista completa de sinais
@bot.message_handler(commands=['adicionarlista'])
def adicionar_lista(message):
    chat_id = message.chat.id
    sinais_texto = message.text.split('\n')[1:]  # Ignorar o comando '/adicionarlista'

    for linha in sinais_texto:
        campos = linha.split(';')
        if len(campos) == 4:  # Changed to 4 fields
            sinal = {
                'par': campos[0],
                'Ativo': campos[1],
                'hora': campos[2],
                'direcao': campos[3]
            }
            lista_sinais.append(sinal)

    bot.reply_to(message, 'Lista de sinais adicionada com sucesso.')



# Comando para visualizar a lista de sinais
@bot.message_handler(commands=['listasinais'])
def visualizar_lista(message):
    chat_id = message.chat.id

    if lista_sinais:
        lista_mensagem = '\n'.join([f'{i+1}. Ativo: {sinal["Ativo"]}, Hora: {sinal["hora"]}, Direção: {sinal["direcao"]}' for i, sinal in enumerate(lista_sinais)])
        bot.reply_to(message, lista_mensagem)
    else:
        bot.reply_to(message, 'A lista de sinais está vazia.')


# Comando para remover a lista de sinais
@bot.message_handler(commands=['removerlista'])
def remover_lista(message):
    chat_id = message.chat.id

    lista_sinais.clear()  # Limpar a lista de sinais

    bot.reply_to(message, 'Lista de sinais removida com sucesso.')


# Função para processar a lista de sinais e enviar cada sinal como um sinal ao vivo
def processar_sinais():
    while True:
        agora = datetime.datetime.now().time()
        sinais_removidos = []

        for sinal in lista_sinais:
            hora_sinal = datetime.datetime.strptime(sinal['hora'], '%H:%M').time()
            hora_sinal_delta = datetime.datetime.combine(datetime.date.today(), hora_sinal) - datetime.timedelta(minutes=3)

            if agora >= hora_sinal_delta.time():
                try:
                    enviar_sinal_ao_vivo(sinal)
                    sinais_removidos.append(sinal)
                except Exception as e:
                    print(f"Erro ao enviar sinal: {e}")

        for sinal in sinais_removidos:
            lista_sinais.remove(sinal)

        # Aguardar 1 minuto antes de verificar novamente
        time.sleep(60)


# Função para enviar um sinal ao vivo para a sala de destino
def enviar_sinal_ao_vivo(sinal):
    mensagem = f'''
    🚥  A N Á L I S E   A O   V I V O  🚥

📊 Par:  {sinal["Ativo"]}

↕️Direção: {sinal["direcao"]}

⏳Entrar para {sinal["par"]} às {sinal["hora"]}
    '''
    bot.send_message(sala_destino, mensagem)


# Iniciar o processamento de sinais em uma thread separada
thread_sinais = threading.Thread(target=processar_sinais)
thread_sinais.start()

# Iniciar o bot
bot.polling()