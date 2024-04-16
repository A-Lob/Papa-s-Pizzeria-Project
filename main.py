import pygetwindow as gw
import cv2 as cv
import pyautogui as pg
import keyboard as kb
import time
import os
from classes import *


def main():
    for i in range(0, 35):
        print(str(35 - i))
        time.sleep(1)
    numOrd = 1
    orders_in_furnace = [0, 0, 0, 0]
    furnace_points = []
    furnace_status = [[0, False], [0, False], [0, False], [0, False]]
    height_thread = 0
    start_thread = 0
    thread = ()
    thread_points = []



    while not kb.is_pressed("q"):
        numreq = 1
        if 0 in orders_in_furnace:
            orderMark = pg.locateOnScreen("imgsReference/orderStates/orderMark.png", confidence=0.7)
            reqs = []
            ingredient1 = None
            ingredient2 = None

            if orderMark != None:
                ingredients = []
                print(orderMark)
                pg.moveTo(orderMark)
                pg.click()
                time.sleep(1)
                orderTaked = pg.locateOnScreen("imgsReference/orderStates/orderTaked.png", confidence=0.7)
                while orderTaked == None:
                    print(orderTaked)
                    if numreq == 1 and os.path.exists(f"data/order{numOrd}") == False:
                        os.mkdir(f"data/order{numOrd}")
                        numOrd += 1
                    pg.screenshot(f"data/order{numOrd - 1}/orderReq{numreq}.png")
                    numreq += 1
                    time.sleep(1.8)
                    orderTaked = pg.locateOnScreen("imgsReference/orderStates/orderTaked.png", confidence=0.7)

                pause_button = pg.locateOnScreen("imgsReference/actions/pause_button.png", confidence=0.7)
                if pause_button != None:
                    pg.moveTo(pause_button)
                    pg.click()
                
                
                for file in os.listdir(f"data/order{numOrd-1}"):
                    img = cv.imread(f"data/order{numOrd-1}/{file}")
                    cv.imshow(file, img)
                    gw.getWindowsWithTitle(file)[0].activate()
                    cv.waitKey(300)
                    if pg.locateOnWindow("imgsReference/order/conditions/time_flag.png", file, confidence=0.7) != None:
                        for req in os.listdir("imgsReference/order/time"):
                            if pg.locateOnWindow("imgsReference/order/time/" + req, file, confidence=0.9) != None:
                                reqs.append(req)
                                print(req)
                    elif pg.locateOnWindow("imgsReference/order/conditions/cut_flag.png", file, confidence=0.7) != None:
                        for req in os.listdir("imgsReference/order/cuts"):
                            if pg.locateOnWindow("imgsReference/order/cuts/" + req, file, confidence=0.9) != None:
                                reqs.append(req)
                                print(req)
                    elif pg.locateOnWindow("imgsReference/order/conditions/ingredient_flag.png", file, confidence=0.7) != None:
                        list_aux = []
                        for dir in os.listdir("imgsReference/ingredients"):
                            for req in os.listdir(f"imgsReference/ingredients/" + dir):
                                if pg.locateOnWindow("imgsReference/ingredients/" + dir + "/" + req, file, confidence=0.9) != None:
                                    list_aux.append(req)
                                    print(req)
                                    break
                        reqs.append(list_aux)
                    time.sleep(1)
                    cv.destroyAllWindows()
                print(reqs)


                for index_req in range(len(reqs)):
                    if isinstance(reqs[index_req], list):
                        elements = []
                        for i in range(len(reqs[index_req])):
                            thing, _ = reqs[index_req][i].split(".")
                            if i == 0:
                                elements.append(int(thing))
                            elif i == 2:
                                if thing == "full":
                                    elements.append([1, 2, 3, 4])
                                elif thing == "halfRight":
                                    elements.append([2, 4])
                                elif thing == "halfLeft":
                                    elements.append([1, 3])
                                elif thing == "halfUp":
                                    elements.append([1, 2])
                                elif thing == "halfDown":
                                    elements.append([3, 4])
                                elif thing == "threeQuarterTwo":
                                    elements.append([1, 3, 4])
                                else:
                                    elements.append([int(thing)])
                            else:
                                elements.append(thing)
                        if index_req == 0:
                            print(elements)
                            ingredient1 = Ingredient(elements[0], elements[1], elements[2])
                            ingredients.append(ingredient1)
                        if index_req == 1:
                            print(elements)
                            ingredient2 = Ingredient(elements[0], elements[1], elements[2])
                            ingredients.append(ingredient2)
                    else: 
                        break
                
                order = Order(ingredients, int(reqs[-2].split(".")[0]), int(reqs[-1].split(".")[0]))
                time.sleep(1)

                unpause_button = pg.locateOnScreen("imgsReference/actions/unpause_button.png", confidence=0.6)
                if unpause_button != None:
                    pg.moveTo(unpause_button)
                    pg.click()


                print(order)
                time.sleep(1)
                
                start_thread, height_thread = order.topping_station()
                thread = (start_thread - 225, height_thread)
                thread_points = [thread, (thread[0] - 200, thread[1]), (thread[0] - 400, thread[1]), (thread[0] - 600, thread[1])]
                note = (start_thread, height_thread + 300)
                time.sleep(0.5)
                furnace_points, furnace_status, orders_in_furnace = order.baking_station_in(numOrd-1, furnace_points, furnace_status, note, thread_points, orders_in_furnace)
            
            
            for i in range(len(furnace_status)):
                if furnace_status[i][1]:
                    if time.time() > (furnace_status[i][0]):
                        furnace_status[i][1] = False
                        pg.moveTo(thread_points[i])
                        pg.mouseDown(button="left")
                        pg.moveTo(note)
                        pg.mouseUp(button="left")
                        orders_in_furnace[i].baking_station_out(furnace_points, furnace_status, i)
                        time.sleep(1)
                        orders_in_furnace[i].cutting_station()
                        orders_in_furnace[i] = 0
                        time.sleep(0.5)
                        finish = pg.locateOnScreen("imgsReference/actions/finish.png", confidence=0.7)
                        pg.moveTo(finish)
                        pg.click()
                        time.sleep(9)

            order_station = pg.locateOnScreen("imgsReference/actions/order_station.png", confidence=0.7)
            pg.moveTo(order_station)
            pg.click()
            

        
        reqs = []

    for dir in os.listdir("data"):
        for file in os.listdir(f"data/{dir}"):
            os.remove(f"data/{dir}/{file}")
        os.rmdir(f"data/{dir}")

if __name__ == "__main__":
    main()