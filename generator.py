
if __name__ == '__main__':

    for i in range(1, 26):
        day_str = str(i).rjust(2, '0')
        with open(f"inputs/day_{day_str}.txt", 'w') as input_file:
            input_file.write("")
        with open(f"solutions/day_{day_str}.py", 'w') as solution_file:
            template = f"""
def part_1():
    with open(f"../inputs/day_{day_str}.txt", 'r') as input_file:
        pass
        
        
def part_2():
    with open(f"../inputs/day_{day_str}.txt", 'r') as input_file:
        pass
        
        
if __name__ == '__main__':
    part_1()
    part_2()
"""
            solution_file.write(template)
