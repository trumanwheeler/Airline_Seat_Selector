rows = 10 # number of rows
cols = 4 # number of columns
seats = open("seats.txt", "r")

# Reads through seats.txt and updates dictionary with formatted seat data per row
def build_seat_data(seats):
    global seats_dataset
    seats_dataset = {}
    i = 1
    for row_value in seats:
        if len(row_value) > 4:
            seats_dataset.update({i: row_value[:-1]})
        else:
            seats_dataset.update({i: row_value})
        i += 1
    return seats_dataset

# Checks to see if dataset has been built, then builds if necessary
def check_for_dataset():
    if 'seats_dataset' not in globals():
        build_seat_data(seats)

# Calls for data refresh and prints dictionary data by row
def display(seats):
    check_for_dataset()
    print("Seating chart:\n\n\tAB CD")
    for i in range(1, rows + 1):
        row_string = str(seats_dataset.get(i))
        print(f'{i}\t{row_string[:2]} {row_string[2:]}', end="\n")

# Locates seat from user input, verifies seat status, and allows for purchase of seat
def purchase(seats):
    check_for_dataset()
    while True:
        purchase_input = input("Enter your row number and column letter <ex. 1A> : ")
        row = int(purchase_input[:-1])
        column_input = purchase_input[-1]
        if column_input == "A":
            column = 0
        elif column_input == "B":
            column = 1
        elif column_input == "C":
            column = 2
        elif column_input == "D":
            column = 3
        if row not in seats_dataset.keys():
            print("Invalid row - please try again\n")
        elif column_input not in ["A", "B", "C", "D"]:
            print("Invalid column - please try again\n")
        else:
            if not assign_seat(seats, row, column):
                print(f"Seat {purchase_input} is not available.")
                nearest_neighbor(seats, row, column)
            else:
                break

# Checks availability of given seat and reserves it if possible
def assign_seat(seats, row, column):
    selected_row = seats_dataset.get(row)
    selected_seat = selected_row[column]
    if selected_seat == "X":
        return False
    else:
        appended_row = selected_row[:column] + 'X' + selected_row[column + 1:]
        seats_dataset.update({row: appended_row})
        with open("seats.txt", "w") as update_seats:
            for i in seats_dataset:
                if i == rows:
                    update_seats.write(seats_dataset.get(i))
                else:
                    update_seats.write(seats_dataset.get(i) + "\n")
        seats = open("seats.txt", "r")
        return True

# Locates and recommends alternative seat if given seat is reserved
def nearest_neighbor(seats, row, column):
    if row == 1:
        row_range = range(row, row + 2)
    elif row == rows:
        row_range = range(row - 1, row + 1)
    else:
        row_range = range(row - 1, row + 2)
    for i in row_range:
        selected_row = seats_dataset.get(i)
        if column == 0:
            column_range = range(column, column + 2)
        elif column == 3:
            column_range = range(column - 1, column + 1)
        else:
            column_range = range(column - 1, column + 2)
        for j in column_range:
            selected_seat = selected_row[j]
            if selected_seat == ".":
                if j == 0:
                    free_seat = str(i) + "A"
                elif j == 1:
                    free_seat = str(i) + "B"
                elif j == 2:
                    free_seat = str(i) + "C"
                elif j == 3:
                    free_seat = str(i) + "D"
                print(f"A free seat is available for purchase at {free_seat}. Would you like to purchase it?")
                return

# Calculates percentage occupancy of plane
def statistics(seats):
    check_for_dataset()
    seats = rows * cols
    taken_seats = 0
    for row_number in seats_dataset:
        for seat in seats_dataset[row_number]:
            if seat == 'X':
                taken_seats += 1
    occupancy = (taken_seats / seats) * 100
    print(f"Aircraft occupancy is {occupancy:.2f}%")

if __name__ == "__main__":
    while True:
        menu_input = input("\nSelect choice from menu:\nD to display seat chart\nP to purchase a seat\nS to compute statistics\nQ to quit\n\n")
        if menu_input == "Q" or menu_input == "q":
            break
        elif menu_input == "D" or menu_input == "d":
            display(seats)
        elif menu_input == "P" or menu_input == "p":
            purchase(seats)
        elif menu_input == "S" or menu_input == "s":
            statistics(seats)
        else:
            print("Please enter a valid input.")