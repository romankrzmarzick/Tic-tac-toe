for i in range(7):
    while True:
        display_board()
        move = (int(input("\n>>>\n")) - 1)
        output = make_move(move, "x")
        if output == "full" or output == "num":
            print("Invalid.")
        else:
            break
   