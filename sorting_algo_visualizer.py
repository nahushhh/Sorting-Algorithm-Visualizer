from matplotlib.pyplot import draw
import pygame
import math
import random
import time
pygame.init()

#setting up the pygame window

class Draw:
    BLACK = 0,0,0
    WHITE = 255,255,255
    RED = 255,0,0
    GREEN = 0,255,0
    GREY = 128,128,128
    DARK_GREY = 160,160,160
    LIGHT_GREY = 192,192,192
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [GREY, DARK_GREY, LIGHT_GREY]
    SIDE_PAD = 100 #provides left and right padding(50 from left and 50 from right)
    TOP_PAD = 150 #provides padding from the top
    CONTROLFONT = pygame.font.SysFont('ariel', 25)
    TITLEFONT =   pygame.font.SysFont('ariel',35)

    def __init__(self, width, height, nums):
        self.width = width #setting the width of the window
        self.height = height #setting the height of the window

        """we need to set up a pygame window on which we draw content
           and we need to access it almost everywhere so we define it inside the class"""
        
        self.window = pygame.display.set_mode((width,height)) #creating the window
        pygame.display.set_caption("Sorting Algorithm Visualizer") #setting title for the window
        self.visualize_list(nums)

    def visualize_list(self,nums):
        self.nums = nums
        self.min_val = min(nums)
        self.max_val = max(nums)
        self.bar_width = round((self.width-self.SIDE_PAD)/len(nums)) #offset for width
        self.bar_height = math.floor((self.height-self.TOP_PAD)/(self.max_val-self.min_val)) #offset for height
        self.origin_X = self.SIDE_PAD//2

# generating the list that is to be sorted
def generate_list(n, small, large):
    nums = []
    for _ in range(n):
        rand_val = random.randint(small, large)
        nums.append(rand_val)
    return nums

# fill colour to main window and display the list
def fill_window(draws, algo_name, ascending, speed, times):
    draws.window.fill(draws.BACKGROUND_COLOR)

    #displaying text onto the screen
    
    title = draws.TITLEFONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draws.BLACK)
    draws.window.blit(title,(draws.width/2-title.get_width()/2, 17))

    controls = draws.CONTROLFONT.render('R: RESET | H: HARD RESET| SPACE: START | A: ASCENDING | D: DESCENDING', 1, draws.BLACK)
    draws.window.blit(controls,(draws.width/2-controls.get_width()/2, 45))

    other = draws.CONTROLFONT.render('UP ARROW: INCREASE SPEED | DOWN ARROW: DECREASE SPEED', 1, draws.BLACK)
    draws.window.blit(other,(draws.width/2-other.get_width()/2, 95))

    rate = draws.CONTROLFONT.render(f'SPEED - {speed}', 1, draws.BLACK)
    draws.window.blit(rate,(draws.width/2-rate.get_width()/2, 115))

    timing = draws.CONTROLFONT.render(f'TIME - {times}', 1, draws.BLACK)
    draws.window.blit(timing,(draws.width/2-timing.get_width()/2, 135))

    sort = draws.CONTROLFONT.render('B: BUBBLE SORT | I: INSERTION SORT | S: SELECTION SORT', 1, draws.BLACK)
    draws.window.blit(sort,(draws.width/2 - sort.get_width()/2,70))
    draw_list(draws)
    pygame.display.update()

# draws the list
def draw_list(draws, color_pos={}, clear_bg=False):
    nums = draws.nums

    if clear_bg:
        clear_rectangle = (draws.SIDE_PAD//2, draws.TOP_PAD, draws.width-draws.SIDE_PAD, draws.height-draws.TOP_PAD)
        pygame.draw.rect(draws.window, draws.BACKGROUND_COLOR, clear_rectangle)
    for index, value in enumerate(nums):
        w = draws.origin_X + index*draws.bar_width # drawing actual width
        h = draws.height - (value-draws.min_val)*draws.bar_height #drawing actual height

        color = draws.GRADIENTS[index % 3] #provides one of the three shades of grey to represent each bar

        if index in color_pos:
            color = color_pos[index] 

        pygame.draw.rect(draws.window, color, (w,h,draws.bar_width, draws.height))

    if clear_bg:
        pygame.display.update()

def bubble_sort(draws, ascending = True):
    nums = draws.nums
    length = len(nums)
    if ascending:
        for i in range(length-1):
            for j in range(length-i-1):
                if nums[j]>nums[j+1]:
                    temp = nums[j+1]
                    nums[j+1] = nums[j]
                    nums[j] = temp
                    draw_list(draws, color_pos={j: draws.GREEN, j+1: draws.RED}, clear_bg=True)
                    yield True 

    if not ascending:
        for i in range(length-1):
            for j in range(length-i-1):
                if nums[j]<nums[j+1]:
                    temp = nums[j+1]
                    nums[j+1] = nums[j]
                    nums[j] = temp
                    draw_list(draws, color_pos={j: draws.GREEN, j+1: draws.RED}, clear_bg=True)
                    yield True
    return nums

def insertion_sort(draw_info, ascending=True):
	nums = draw_info.nums

	for i in range(1, len(nums)):
		current = nums[i]

		while True:
			ascending_sort = i > 0 and nums[i - 1] > current and ascending
			descending_sort = i > 0 and nums[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			nums[i] = nums[i - 1]
			i = i - 1
			nums[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return nums

def selection_sort(draw_info, ascending=True):
    nums = draw_info.nums
    length = len(nums)  
    
    if ascending:
        for i in range(length-1):  
            minIndex = i  
            
            for j in range(i+1, length):  
                if nums[j]<nums[minIndex]:  
                    minIndex = j
                    draw_list(draw_info, color_pos={j: draw_info.GREEN, j+1: draw_info.RED}, clear_bg=True) 
                    yield True 
                    
            nums[i], nums[minIndex] = nums[minIndex], nums[i]  
    
    if not ascending:
        for i in range(length-1):  
            minIndex = i  
            
            for j in range(i+1, length):  
                if nums[j]>nums[minIndex]:  
                    minIndex = j
                    draw_list(draw_info, color_pos={j: draw_info.GREEN, j+1: draw_info.RED}, clear_bg=True) 
                    yield True 
                    
            nums[i], nums[minIndex] = nums[minIndex], nums[i] 
                    

    return nums      


# Main event loop
def main():
    run = True
    clock = pygame.time.Clock() #regulates how quickly the loop will run
    sorting = False
    ascending = False
    n = 50
    small = 0
    large = 100
    speed = 60
    times = 0
    nums = generate_list(n, small, large)
    draws = Draw(800,600,nums)
    sorting_algorithm_name = 'Select Algorithm'
    sorting_algorithm_generator = None
    while run:
        clock.tick(speed) #fps. max times this loop will run per second
        
        if sorting:
            try:
                next(sorting_algorithm_generator)
                end = time.time()
                times = end-start
                fill_window(draws, sorting_algorithm_name, ascending, speed, times)
            except StopIteration:
                sorting = False
        else:
            fill_window(draws, sorting_algorithm_name, ascending, speed, times)

        for event in pygame.event.get(): # pygame.event.get(): gives all the events that have occured
            if event.type==pygame.QUIT:
                run = False

            # if no key is pressed            
            if event.type != pygame.KEYDOWN:
                continue
            
            # if 'r' is pressed then reset the list
            if event.key == pygame.K_r:
                nums = generate_list(n, small, large)
                draws.visualize_list(nums)
                sorting = False
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                start = time.time()
                if sorting_algorithm_name == 'Bubble Sort':
                    sorting_algorithm_generator = bubble_sort(draws, ascending)
                elif sorting_algorithm_name == 'Insertion Sort':
                    sorting_algorithm_generator = insertion_sort(draws, ascending)
                elif sorting_algorithm_name == 'Selection Sort':
                    sorting_algorithm_generator = selection_sort(draws, ascending)
                
            
            elif event.key == pygame.K_i:
                sorting_algorithm_name = 'Insertion Sort'
            
            elif event.key == pygame.K_s:
                sorting_algorithm_name = 'Selection Sort'
            
            elif event.key == pygame.K_b:
                sorting_algorithm_name = 'Bubble Sort'
            
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            
            elif event.key == pygame.K_UP:
                speed+=10
                fill_window(draws, sorting_algorithm_name, ascending, speed, times)
            
            elif event.key == pygame.K_DOWN:
                speed-=10
                fill_window(draws, sorting_algorithm_name, ascending, speed, times)

    pygame.quit()


if __name__=='__main__':
    main()
