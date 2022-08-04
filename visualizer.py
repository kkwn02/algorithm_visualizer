import pygame
import random

pygame.init()

class VisualizerConfigurations:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE

    GRADIENTS = [(128,128,128), (160, 160, 160), (192,192,192)]

    SIDE_PADDING = 100
    TOP_PADDING = 150

    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    def __init__(self, width, height, data):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_data(data)

    def set_data(self, data):
        self.data = data
        self.max_value = max(data)
        self.min_value = min(data)
        #calculate the width of each block
        self.block_width = int((self.width - self.SIDE_PADDING) / len(data))
        #calculate the height per unit for each block
        self.block_height = int((self.height - self.TOP_PADDING) / (self.max_value - self.min_value))
        self.left = self.SIDE_PADDING // 2

class AlgorithmSettings:
    def __init__(self, n, min_val, max_val, ascending):
        self.n = n
        self.min_val = min_val
        self.max_val = max_val
        self.ascending = ascending

def generate_data(algoSettings):
    data = []
    for _ in range(algoSettings.n):
        data.append(random.randint(algoSettings.min_val, algoSettings.max_val))

    return data

def draw_canvas(canvas, cur_sort):
    #Overwrite all previous drawings
    canvas.window.fill(canvas.BACKGROUND_COLOR)
    control_desc = canvas.FONT.render("R - Reset | SPACE - Start Sorting | A - Toggle Sort Order", 1, canvas.BLACK)
    canvas.window.blit(control_desc, (canvas.width/2 - control_desc.get_width()/2 , 5))
    sort_options = canvas.FONT.render(cur_sort, 1, canvas.BLACK)
    canvas.window.blit(sort_options, (canvas.width/2 - sort_options.get_width()/2 , 35))
    draw_data(canvas)
    pygame.display.update()

def draw_data(canvas, color_pos={}, clear=False):
    if clear:
        clear_data = (canvas.SIDE_PADDING // 2, canvas.TOP_PADDING, 
            canvas.width - canvas.SIDE_PADDING, canvas.height - canvas.TOP_PADDING)
        pygame.draw.rect(canvas.window, canvas.BACKGROUND_COLOR, clear_data)

    data = canvas.data
    for i, val in enumerate(data):
        x = canvas.left + (i * canvas.block_width)
        #subtract by min_value to account for negative values
        y = canvas.height - ((val-canvas.min_value) * canvas.block_height)
        #create color difference between adjacent blocks
        color = canvas.GRADIENTS[i%3]
        if i in color_pos:
            color = color_pos[i]
        pygame.draw.rect(canvas.window, color, 
            (x, y, canvas.block_width, canvas.height))

    if clear:
        pygame.display.update()

def bubble_sort(canvas, ascending=True):
    data = canvas.data
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            num1 = data[j]
            num2 = data[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(canvas, {j: canvas.RED, j+1: canvas.GREEN}, True)
                #pause the sorting every step 
                yield True

    return data

def insertion_sort(canvas, ascending=True):
	data = canvas.data

	for i in range(1, len(data)):
		current = data[i]

		while True:
			ascending_sort = i > 0 and data[i - 1] > current and ascending
			descending_sort = i > 0 and data[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			data[i] = data[i - 1]
			i = i - 1
			data[i] = current
			draw_data(canvas, {i - 1: canvas.GREEN, i: canvas.RED}, True)
			yield True
	return data

def merge(canvas, data, l, r, m, ascending):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * (n1)
    R = [0] * (n2)
 
    for i in range(0, n1):
        L[i] = data[l + i]
 
    for j in range(0, n2):
        R[j] = data[m + 1 + j]
 
    i = 0    
    j = 0     
    k = l     
 
    while i < n1 and j < n2:
        if L[i] <= R[j]:
            data[k] = L[i]
            i += 1
        else:
            data[k] = R[j]
            j += 1
        draw_data(canvas, {k: canvas.GREEN}, True)
        k += 1
 
    while i < n1:
        data[k] = L[i]
        draw_data(canvas, {k: canvas.GREEN}, True)
        i += 1
        k += 1
 
    while j < n2:
        data[k] = R[j]
        draw_data(canvas, {k: canvas.GREEN}, True)
        j += 1
        k += 1

def merge_helper(canvas, data, l, r, ascending):
    if (l < r):
        m = (r-l)//2 + l
        merge_helper(canvas, data, l, m, ascending)
        merge_helper(canvas, data, m+1, r, ascending)
        merge(canvas, data,l, r, m, ascending)

def merge_sort(canvas, ascending=True):
    data = canvas.data
    merge_helper(canvas, data, 0, len(data)-1, ascending)
    yield True
    return data

def main():
    run = True
    clock = pygame.time.Clock()

    algoSettings = AlgorithmSettings(100, 0, 100, True)
    data = generate_data(algoSettings)
    canvas = VisualizerConfigurations(800, 600, data)
    sort = False

    algorithm_generator = None
    algorithms = [bubble_sort, insertion_sort, merge_sort]
    algorithms_str = ["Bubble Sort", "Insertion Sort", "Merge Sort"]
    cur = 0
    algorithm = algorithms[cur]
    algorithm_str = algorithms_str[cur]

    while run:
        clock.tick(30)
        ascending = algoSettings.ascending
        #render window
        draw_canvas(canvas, algorithm_str)

        if sort:
            try:
                next(algorithm_generator)
            except StopIteration:
                algorithm_generator = None
                sort = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                data = generate_data(algoSettings)
                canvas.set_data(data)
                sort = False
            elif event.key == pygame.K_SPACE and not sort:
                sort = True
                algorithm_generator = algorithm(canvas, ascending)
            elif event.key == pygame.K_a and not sort:
                algoSettings.ascending = not algoSettings.ascending
            elif event.key == pygame.K_s and not sort:
                cur = (cur+1)%len(algorithms)
                algorithm = algorithms[cur]
                algorithm_str = algorithms_str[cur]

    pygame.quit()

if __name__ == "__main__":
	main()