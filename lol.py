import sys

if __name__ == '__main__':
    print_status_code = False
    if len(sys.argv) >= 3:
        number_of_threads, number_of_iterations = sys.argv[1:3]
        number_of_threads = int(number_of_threads)
        number_of_iterations = int(number_of_iterations)
        if len(sys.argv) == 4:
            if sys.argv[3] == '/O':
                print_status_code = True
    else:
        print('main.py M N [/O]')
        print('M - threads, N - iterations, /O - необязательный ключ Output status code')
        sys.exit()
    print(number_of_threads,
        number_of_threads, print_status_code)