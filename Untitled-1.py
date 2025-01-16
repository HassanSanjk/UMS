with open("users.txt", 'r') as file:
            next(file)
            data = []
            for line in file:
                data.append(line.strip().split(","))


print(data)