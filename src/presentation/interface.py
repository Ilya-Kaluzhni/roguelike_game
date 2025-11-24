import curses


class InterfaceBackpack:
    def __init__(self, stdscr, height=15, width=20, begin_y=0, begin_x=0):
        self.window = curses.newwin(height, width, begin_y, begin_x)
        self.w_backpack = (1, 1)
        self.w_weapon = (self.w_backpack[0] + 1, self.w_backpack[1])
        self.w_food = (self.w_weapon[0] + 1, self.w_weapon[1])
        self.w_elixir = (self.w_food[0] + 1, self.w_food[1])
        self.w_scroll = (self.w_elixir[0] + 1, self.w_elixir[1])
        # self.show_panel()

    def show_panel(self):
        self.window.clear()
        self.window.addstr(self.w_backpack[0], self.w_backpack[1], 'Рюкзак')
        self.window.addstr(self.w_weapon[0], self.w_weapon[1], 'Оружие (h)')
        self.window.addstr(self.w_food[0], self.w_food[1], 'Еда (j)')
        self.window.addstr(self.w_elixir[0], self.w_elixir[1], 'Эликсир (k)')
        self.window.addstr(self.w_scroll[0], self.w_scroll[1], 'Свиток (e)')
        self.window.border()
        self.window.refresh()

    def show_current_items(self, item_type, items_list):
        if item_type == 'weapon':
            start_y, start_x = self.w_weapon
            start_index = 0
        else:
            if item_type == 'food':
                start_y, start_x = self.w_food
            elif item_type == 'elixir':
                start_y, start_x = self.w_elixir
            elif item_type == 'scroll':
                start_y, start_x = self.w_scroll
            start_index = 1
        self.window.move(start_y + 1, start_x)
        self.window.clrtobot()
        for i, item in enumerate(items_list, start=start_index):
            y = start_y + i + 1 - start_index
            self.window.addstr(y, start_x, f"{i}. {item}")
        self.window.border()
        self.window.refresh()

# def main(stdscr):
#     interface = InterfaceBackpack(stdscr, height=15, width=40, begin_y=2, begin_x=2)
#     weapons = ['Кинжал', 'Меч', 'Лук']
#     foods = ['Хлеб', 'Яблоко']
#     elixirs = ['Зелье здоровья', 'Зелье маны']
#     scrolls = ['Свиток огня', 'Свиток телепорта']
#
#     interface.show_panel()
#
#     while True:
#         c = stdscr.getch()
#         interface.show_panel()
#         if c == ord('h'):
#             interface.show_current_items('weapon', weapons)
#         elif c == ord('j'):
#             interface.show_current_items('food', foods)
#         elif c == ord('k'):
#             interface.show_current_items('elixir', elixirs)
#         elif c == ord('e'):
#             interface.show_current_items('scroll', scrolls)
#         elif c == ord('q'):
#             break
#
#
# curses.wrapper(main)
