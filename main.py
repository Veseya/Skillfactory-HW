print("*" * 8, "     Добро пожаловать в игру!    ", "*" * 8)
print("*" * 2, " Для выбора клетки используйте цифры от 1 до 9  ", "*" * 2)
print("*" * 8, "       Начинает Х, Удачи!        ", "*" * 8)

field = list(range(1, 10))


def game_board(field):
    print("-" * 13)
    for i in range(3):
        print("|", field[0+i*3], "|", field[1+i*3], "|", field[2+i*3], "|")
        print("-" * 13)


def ask(token):
    while True:
        answer = int(input("Выбирает ячейку " + token + ": "))
        if 1 <= answer <= 9:
            if str(field[answer-1]) not in "XO":
                field[answer-1] = token
            else:
                print("Клетка занята")
        else:
            print("Число вне диапазона")
        return answer


def check_win(field):
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if field[each[0]] == field[each[1]] == field[each[2]]:
            return field[each[0]]
    return False


def main(field):
    counter = 0
    win = False
    while not win:
        game_board(field)
        if counter % 2 == 0:
            ask("X")
        else:
            ask("O")
        counter += 1
        if counter > 4:
            tmp = check_win(field)
            if tmp:
                print(tmp, "выиграл!")
                win = True

                break
        if counter == 9:
            print("Ничья!")
            break


main(field)
