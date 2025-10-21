import prompt

def welcome():
    print('***')
    print('<command> exit - выйти из программы')
    print('<command> help - справочная информация')

    while True:
        command = prompt.string('Введите команду: ').strip().lower()

        if command == 'exit':
            print('До свидания!')
            break
        elif command == 'help':
            print('<command> exit - выйти из программы')
            print('<command> help - справочная информация')
        else:
            print(f'Команда "{command}" не распознана. Попробуйте снова.')
