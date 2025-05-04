def map_coloring():
    colors = ['Red', 'Green', 'Blue']
    regions = {
        'WA': ['NT', 'SA'],
        'NT': ['WA', 'SA', 'Q'],
        'SA': ['WA', 'NT', 'Q', 'NSW', 'V'],
        'Q': ['NT', 'SA', 'NSW'],
        'NSW': ['SA', 'Q', 'V'],
        'V': ['SA', 'NSW'],
        'T': []
    }

    def is_valid(assign, region, color):
        for neighbor in regions[region]:
            if neighbor in assign and assign[neighbor] == color:
                return False
        return True

    def backtrack(assign):
        if len(assign) == len(regions):
            return assign
        for region in regions:
            if region not in assign:
                for color in colors:
                    if is_valid(assign, region, color):
                        assign[region] = color
                        result = backtrack(assign)
                        if result:
                            return result
                        del assign[region]
                return None

    solution = backtrack({})
    print("Map Coloring Solution:")
    for region in sorted(solution):
        print(f"{region}: {solution[region]}")

map_coloring()
