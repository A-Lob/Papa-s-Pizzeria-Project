import pyautogui as pg
import keyboard as kb
import time

class Ingredient:
    TIPOS_VALIDOS = ["pepperoni", "anchovies", "champignones", "peppers", "olives", "sausage", "onions"]
    CANTIDADES_VALIDAS = [2, 3, 4, 6, 8]
    ZONAS_VALIDAS = list(range(4))
    def __init__(self, quantity, type, zones):
        self.set_quantity(quantity)
        self.set_type(type)
        self.set_zones(zones)
    
    def set_type(self, type):
        if type in self.TIPOS_VALIDOS:
            self.type = type
        else:
            raise ValueError("The ingredient type is not valid")
    
    def set_quantity(self, quantity):
        if quantity in self.CANTIDADES_VALIDAS:
            self.quantity = quantity
        else:
            raise ValueError("The quantity is not valid")
    
    def set_zones(self, zones):
        for zone in zones:
            if zone in self.ZONAS_VALIDAS:
                self.zones = zones
    
    def __str__(self):
        return f"Ingredient: \n  Type: {self.type}, \n  Quantity: {self.quantity}, \n  Zones: {self.zones}"

class Order:
    def __init__(self, ingredients, time, cut):
        self.set_ingredients(ingredients)
        self.set_time(time)
        self.set_cut(cut)

    def set_time(self, time):
        if isinstance(time, int) and 0 < time < 8:
            self.time = time
        else:
            raise ValueError("The cooking time must be an integer between 0 and 8")
        
    def set_cut(self, cut):
        if isinstance(cut, int) and 2 <= cut <= 4:
            self.cut = cut
        else:
            raise ValueError("The cut must be an integer between 1 and 5")
        
    def set_ingredients(self, ingredients):
        for ingrediente in ingredients:
            if isinstance(ingrediente, Ingredient):
                self.ingredients = ingredients
            else:
                raise ValueError("Ingredients must be of type Ingredient")
            
    def topping_station(self):
        station_button = pg.locateOnScreen("imgsReference/actions/topping_station.png", confidence=0.7)
        left, top, width, height = station_button
        if station_button != None:
            pg.moveTo(station_button)
            pg.click()
            time.sleep(0.5)
            make_pizza = pg.locateOnScreen("imgsReference/actions/topping_station/make_pizza.png", confidence=0.7)
            if make_pizza != None:
                pg.moveTo(make_pizza)
                pg.click()
                time.sleep(0.3)
                base_pizza = pg.locateOnScreen("imgsReference/actions/topping_station/base_pizza.png",confidence=0.7)
                if base_pizza != None:
                    q1, q2, q3, q4 = self.quadrant_division(base_pizza)
                    _, q1_1, q1_2, q1_3 = self.quadrant_division(q1)
                    q2_1, _, q2_2, q2_3 = self.quadrant_division(q2)
                    q3_1, q3_2, _, q3_3 = self.quadrant_division(q3)
                    q4_1, q4_2, q4_3, _ = self.quadrant_division(q4)
                    quadrants1 = [q1_1, q1_2, q1_3]
                    quadrants2 = [q2_1, q2_3, q2_2]
                    quadrants3 = [q3_1, q3_3, q3_2]
                    quadrants4 = [q4_2, q4_3, q4_1]
                
                for ingredient in self.ingredients:
                    quantite_per_quadrant = ingredient.quantity // len(ingredient.zones)
                    ingredient_bowl = pg.locateOnScreen("imgsReference/actions/topping_station/" + ingredient.type + ".png", confidence=0.9)
                    if 1 in ingredient.zones:
                        for index_point in range(len(quadrants1)):
                            if index_point + 1 > quantite_per_quadrant:
                                break
                            self.set_ingredient( quadrants1[index_point], ingredient_bowl)
                        if quantite_per_quadrant == 4:
                            self.set_ingredient(quadrants1[0], ingredient_bowl)
                    
                    if 2 in ingredient.zones:
                        for index_point in range(len(quadrants2)):
                            if index_point + 1 > quantite_per_quadrant:
                                break
                            self.set_ingredient(quadrants2[index_point], ingredient_bowl)
                        if quantite_per_quadrant == 4:
                            self.set_ingredient(quadrants2[0], ingredient_bowl)

                    if 3 in ingredient.zones:
                        for index_point in range(len(quadrants3)):
                            if index_point + 1 > quantite_per_quadrant:
                                break
                            self.set_ingredient(quadrants3[index_point], ingredient_bowl)
                        if quantite_per_quadrant == 4:
                            self.set_ingredient(quadrants3[0], ingredient_bowl)
                    
                    if 4 in ingredient.zones:
                        for index_point in range(len(quadrants4)):
                            if index_point + 1 > quantite_per_quadrant:
                                break
                            self.set_ingredient(quadrants4[index_point], ingredient_bowl)
                        if quantite_per_quadrant == 4:
                            self.set_ingredient(quadrants4[0], ingredient_bowl)
            return left, top
                        
    def baking_station_in(self,num_ord, furnace_points, furnace_status, note, thread_points, orders):
        station_button = pg.locateOnScreen("imgsReference/actions/baking_station_in.png", confidence=0.7)
        cooking_time = self.time * 24
        if station_button != None:
            pg.moveTo(station_button)
            pg.click()
            time.sleep(1)
            for i_status in range(len(furnace_status)):
                if not furnace_status[i_status][1]:
                    furnace_status[i_status][1] = True
                    furnace_status[i_status][0] = time.time() + cooking_time
                    orders[i_status] = self
                    pg.moveTo(note)
                    pg.mouseDown(button="left")
                    pg.moveTo(thread_points[i_status])
                    pg.mouseUp(button="left")
                    break
            if num_ord == 1:
                make_pizza = pg.locateOnScreen("imgsReference/actions/baking_station/pizza_base.png", confidence=0.5)
                if make_pizza != None:
                    center_mp = pg.center(make_pizza)
                    furnace_points = [center_mp, (center_mp[0] + make_pizza[2] + (make_pizza[2] // 3), center_mp[1]),
                                      (center_mp[0], center_mp[1] + make_pizza[3]), (center_mp[0] + make_pizza[2] + (make_pizza[2] // 3), center_mp[1] + make_pizza[3])]
                
                return furnace_points, furnace_status, orders
            
        return furnace_points, furnace_status, orders
    
    def baking_station_out(self, furnace_points, furnace_status, index):
        station_button = pg.locateOnScreen("imgsReference/actions/baking_station_out.png", confidence=0.7)
        if station_button != None:
            pg.moveTo(station_button)
            pg.click()
            pg.moveTo(furnace_points[index])
            time.sleep(0.5)
            pg.click()
    
    def cutting_station(self):
        pizza = pg.locateOnScreen("imgsReference/actions/cutting_station/pizza_base.png", confidence=0.5)
        if pizza != None:
            left, top, width , height = pizza
            print(pizza)
        else:
            pizza = pg.locateOnScreen("imgsReference/actions/cutting_station/pizza_base2.png", confidence=0.5)
            if pizza != None:
                left, top, width, height = pizza

        if self.cut == 2:
            cut1_p1 = [left + 50, top + height // 2]
            cut1_p2 = [left + width - 50, (top - 5) + height // 2]
            cut2_p1 = [left + width // 2, top]
            cut2_p2 = [(left - 5) + width // 2, top + height]
            pg.moveTo(cut1_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut1_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut2_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut2_p2)
            pg.mouseUp(button="left")
        elif self.cut == 3:
            cut1_p1 = [left + width // 2, top]
            cut1_p2 = [(left - 5) + width // 2, top + height]
            cut2_p1 = [left + 100, top + height - 100]
            cut2_p2 = [left + width, top]
            cut3_p1 = [left, top]
            cut3_p2 = [left + width, top + height]

            pg.moveTo(cut1_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut1_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut2_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut2_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut3_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut3_p2)
            pg.mouseUp(button="left")
            
        elif self.cut ==4:
            cut1_p1 = [left + width // 2, top]
            cut1_p2 = [(left - 5) + width // 2, top + height]
            cut2_p1 = [left + 100, top + height - 100]
            cut2_p2 = [left + width, top]
            cut3_p1 = [left, top]
            cut3_p2 = [left + width, top + height]
            cut4_p1 = [left + 50, top + height // 2]
            cut4_p2 = [left + width - 50, (top - 5) + height // 2]

            pg.moveTo(cut1_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut1_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut2_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut2_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut3_p1)
            pg.mouseDown(button="left")
            pg.moveTo(cut3_p2)
            pg.mouseUp(button="left")

            pg.moveTo(cut4_p1)
            pg.mouseDown(button='left')
            pg.moveTo(cut4_p2)
            pg.mouseUp(button='left')

    def quadrant_division(self, box):
        left, top, width, height = box

        middle_x = left + width // 2
        middle_y = top + height // 2

        top_left = (left, top, middle_x - left, middle_y - top)
        top_right = (middle_x, top, left + width - middle_x, middle_y - top)
        bottom_left = (left, middle_y, middle_x - left, top + height - middle_y)
        bottom_right = (middle_x, middle_y, left + width - middle_x, top + height - middle_y)

        return top_left, top_right, bottom_left, bottom_right

    def set_ingredient(self, point, ingredient_bowl):
        pg.moveTo(ingredient_bowl)
        pg.mouseDown(button="left")

        pg.moveTo(point)
        pg.mouseUp(button="left")
        

    def __str__(self):
        ingredientes_str = " \n ".join([str(ingrediente) for ingrediente in self.ingredients])
        return f"Order: \n Time: {self.time}, \n Cut: {self.cut}, \n {ingredientes_str}"

    
if __name__ == "__main__":
    ingrediente1 = Ingredient(8, "pepperoni",[1, 2, 3, 4])
    ingrediente2 = Ingredient(6, "onions", [2, 4])
    ingrediente3 = Ingredient(4, "peppers", [1, 3])
    ingrediente4 = Ingredient(4, "anchovies", [1,2])
    pedido1 = Order([ingrediente1], 1, 3)
    pedido2 = Order([ingrediente2], 2, 4)
    pedido3 = Order([ingrediente3], 3, 2)
    pedido4 = Order([ingrediente4], 3, 2)
    pedidos = [pedido1, pedido2, pedido3, pedido4]
    num_order = 1
    furnace_points = []
    furnace_status = [[0 , False], [0, False], [0, False], [0, False]]
    waiting_orders = []
    thread_points = []
    height_thread = 0
    start_thread = 0
    thread = ()
    note = ()

    while not kb.is_pressed("q"):
        print(pedidos[num_order])
        start_thread, height_thread = pedidos[num_order].topping_station()
        thread = (start_thread - 225, height_thread)
        thread_points = [thread, (thread[0] - 200, thread[1]), (thread[0] - 400, thread[1]), (thread[0] - 600, thread[1])]
        note = (start_thread, height_thread + 300)
        time.sleep(1)
        furnace_points, furnace_status = pedidos[num_order].baking_station_in(num_order, furnace_points, furnace_status, note, thread_points)
        print(furnace_points)
        print(furnace_status)
        time.sleep(1)
        pedidos[num_order].cutting_station()
        num_order += 1
        for i in range(len(furnace_status)):
            if furnace_status[i][1]:
                print(time.time(), "  -  " ,furnace_status[i][0])
                if time.time() > furnace_status[i][0]:
                    print("Sacando")
                    furnace_status[i][1] = False
                    pg.moveTo(thread_points[i])
                    pg.mouseDown(button="left")
                    time.sleep(1)
                    pg.moveTo(note)
                    pg.mouseUp(button="left")
                    time.sleep(1)
                    pedidos[i].baking_station_out(furnace_points, furnace_status, i)
                    time.sleep(1)
                    pedidos[i].cutting_station()
        time.sleep(6)

        if num_order == 4:
            num_order = 0
                    