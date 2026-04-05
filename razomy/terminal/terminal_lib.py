def terminal_listener(cb):
    while True:
        print('send "q" to stop:')
        user_text = input()
        if user_text.lower() == 'q':
            break

        result = cb(user_text)
        print(result)
