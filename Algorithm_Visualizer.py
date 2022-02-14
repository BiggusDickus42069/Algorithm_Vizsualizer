import pygame
import random as rand
import math

pygame.init()



class DrawInfo:
    Bg_Color = 223, 223, 223  # White
    Font_Color = 0, 0, 0  # Pure Black
    Near_Color = 180, 0, 0  # Red
    Selected_Color = 0, 180, 0  # Green
    Mid_Color = 0, 0, 255  # Blue

    Gradients = [
        (157, 157, 157), (123, 123, 123), (80, 80, 80), (50, 50, 50)
    ]
    Font = pygame.font.SysFont('comicsans', 30)

    X_Pad = 100
    Y_Pad = 150

    def __init__(self, width, height, arr):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Visualized')
        self.Set_List(arr)

    def Set_List(self, arr):
        self.arr = arr
        self.min_value = min(arr)
        self.max_value = max(arr)

        self.B_Width = round((self.width - self.X_Pad) / len(arr))
        self.B_Height = math.floor((self.height - self.Y_Pad) / (self.max_value - self.min_value))
        self.start_x = self.X_Pad // 2


def Draw(draw_info, algo, ascending, x):
    draw_info.window.fill(draw_info.Bg_Color)

    title = draw_info.Font.render(f"{algo} - {'Ascending' if ascending else 'Descending'}", 1,
                                  draw_info.Selected_Color)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.Font.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending "
                                     "| + - Increase Size of Array | - - Decrease Size of Array",
                                     1, draw_info.Font_Color)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 45))
    controls = draw_info.Font.render("S - Sine Function"
                                     "", 1, draw_info.Font_Color)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 75))

    sorting = draw_info.Font.render("N - Binary Search | B - Bubble Sort", 1, draw_info.Font_Color)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 105))

    searching = draw_info.Font.render("Searching for " + str(x), 1, draw_info.Font_Color)
    draw_info.window.blit(searching, (draw_info.width / 2 - searching.get_width() / 2, 135))

    draw_arr(draw_info)
    pygame.display.update()


def draw_arr(draw_info, color_pos={}, clear_bg=False):
    arr = draw_info.arr

    if clear_bg:
        clear_rect = (draw_info.X_Pad // 2, draw_info.Y_Pad,
                      draw_info.width - draw_info.X_Pad, draw_info.height - draw_info.Y_Pad)
        pygame.draw.rect(draw_info.window, draw_info.Bg_Color, clear_rect)

    for i, val in enumerate(arr):
        x = draw_info.start_x + i * draw_info.B_Width
        y = draw_info.height - (val - draw_info.min_value) * draw_info.B_Height

        color = draw_info.Gradients[i % 3]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.B_Width, draw_info.height))

    if clear_bg:
        pygame.display.update()


def Random_Arr(n, min_value, max_value, sine):
    arr = []
    for _ in range(n):
        if sine:
            val = math.sin(rand.randint(min_value, max_value))
        else:
            val = rand.randint(min_value, max_value)
        arr.append(val)
    return arr


def Bubble_Sort(draw_info, ascending=True):
    arr = draw_info.arr
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            num1 = arr[j]
            num2 = arr[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                draw_arr(draw_info, {j: draw_info.Selected_Color, j + 1: draw_info.Near_Color}, True)
                yield True

    return arr

# Literally to god damm fast
# Fails to continue highlighting on last block


def B_Search(draw_info, x, ascending=True):
    arr = draw_info.arr

    low = 0
    high = len(arr) - 1
    mid = None

    while low <= high:
        mid = (high + low) // 2
        draw_arr(draw_info, {mid: draw_info.Mid_Color}, True)
        if arr[mid] < x:
            low = mid + 1
            draw_arr(draw_info, {low: draw_info.Selected_Color, high: draw_info.Near_Color}, True)
            yield True
        elif arr[mid] > x:
            high = mid - 1
            draw_arr(draw_info, {high: draw_info.Selected_Color, low: draw_info.Near_Color}, True)
            yield True
        elif arr[mid] == x:
            draw_arr(draw_info, {mid: draw_info.Selected_Color}, True)
            draw_info.Font.render("Found on Position" + str(mid), 1, draw_info.Font_Color)
            yield True
            return arr[mid]
    return -1


def main():
    run = True
    clock = pygame.time.Clock()

    x = 0

    n = 50
    min_value = 0
    max_value = 100
    sine = False

    arr = Random_Arr(n, min_value, max_value, sine)
    draw_info = DrawInfo(1280, 720, arr)

    sorting = False
    ascending = True

    sorting_algo = Bubble_Sort
    algo_name = "Bubble Sort"
    Arr_Gen = None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(Arr_Gen)
            except StopIteration:
                sorting = False
        else:
            Draw(draw_info, algo_name, ascending, x)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_PLUS:
                n += 10
                lst = Random_Arr(n, min_value, max_value, sine)
                draw_info.Set_List(lst)
                sorting = False
            if event.key == pygame.K_MINUS:
                n -= 10
                lst = Random_Arr(n, min_value, max_value, sine)
                draw_info.Set_List(lst)
                sorting = False
            if event.key == pygame.K_s:
                sine = True
                lst = Random_Arr(n, min_value, max_value, sine)
                draw_info.Set_List(lst)
                sorting = False
            if event.key == pygame.K_r:
                lst = Random_Arr(n, min_value, max_value, sine)
                draw_info.Set_List(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                if sorting_algo == B_Search:
                    Arr_Gen = sorting_algo(draw_info, x, ascending)
                else:
                    Arr_Gen = sorting_algo(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_n and not sorting:
                x = rand.choice(arr)
                arr.sort()
                sorting_algo = B_Search
                algo_name = "Binary Search"
            elif event.key == pygame.K_b and not sorting:
                sorting_algo = Bubble_Sort
                algo_name = "Bubble Sort"


if __name__ == '__main__':
    main()
