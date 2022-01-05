from object_detection_classification import get_fruit_recognition
import queue
import threading

if __name__ == '__main__':
    # return params
    q_cant = queue.Queue()
    q_type = queue.Queue()
    q_cant_ripe = queue.Queue()
    q_cant_unripe = queue.Queue()
    t1 = threading.Thread(target=get_fruit_recognition,name=get_fruit_recognition,args=(q_cant,q_type,q_cant_ripe,q_cant_unripe))
    t1.start()
    params = []
    while True:
        value_cant = q_cant.get()
        value_type = q_type.get()
        value_cant_ripe = q_cant_ripe.get()
        value_cant_unripe = q_cant_unripe.get()


        print("Fruit cant: ",value_cant, "Fruit type: ", value_type,"Ripe cant", value_cant_ripe, "Unripe cant", value_cant_unripe)

