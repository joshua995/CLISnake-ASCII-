def sevenSegmentLogic(num: int):
    if num == 0:
        return [" _ ", "| |", "|_|"]
    elif num == 1:
        return ["   ", "  |", "  |"]
    elif num == 2:
        return [" _ ", " _|", "|_ "]
    elif num == 3:
        return [" _ ", " _|", " _|"]
    elif num == 4:
        return ["   ", "|_|", "  |"]
    elif num == 5:
        return [" _ ", "|_ ", " _|"]
    elif num == 6:
        return [" _ ", "|_ ", "|_|"]
    elif num == 7:
        return [" _ ", "  |", "  |"]
    elif num == 8:
        return [" _ ", "|_|", "|_|"]
    elif num == 9:
        return [" _ ", "|_|", " _|"]


def multi7SegmentLogic(num, rgb, spaces):
    results, numbers, currentNum = ["", "", ""], [], num
    while currentNum > 9:
        numbers.append(currentNum % 10)
        currentNum //= 10
    numbers.append(currentNum)
    tempResults = []
    for n in reversed(numbers):
        res = sevenSegmentLogic(n)
        tempResults.append(res) if res != None else ""

    for tmpRes in tempResults:
        results[0] += str(tmpRes[0])
        results[1] += str(tmpRes[1])
        results[2] += str(tmpRes[2])
    [print(" " * spaces + f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m" + r) for r in results]
