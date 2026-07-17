import time

# Tharavik velenusar alert denar
def schedule_task(task_time, task_name):
    print("Scheduler chalu zala. Task vel:", task_time)
    while True:
        current_time = time.strftime("%H:%M")  # tas:minute
        if current_time == task_time:
            print("\n!!! ALERT !!!")
            print("Time zala! Task kara:", task_name)
            break
        time.sleep(10)  # 10 second ne check kar