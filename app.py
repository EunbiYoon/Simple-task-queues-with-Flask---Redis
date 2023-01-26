from flask import Flask,request
import redis
from rq import Queue
import time
import os
child_pid = os.fork() if hasattr(os, 'fork') else None

app=Flask(__name__)

r=redis.Redis()
q=Queue(connection=r)

def backgroud_task(n):
    delay=2
    print("Task running")
    print(f"Simulating {delay} second delay")
    time.sleep(delay)
    print(len(n))
    print("Task Complete")
    return len(n)

@app.route("/task")
def add_task():
    if request.args.get("n"):
        job=q.enqueue(backgroud_task, request.args.get('n'))
        q_len=len(q)
        return f"Task {job.id} added to queue at {job.enqueued_at}. {q_len} tasks in the queue" 
    return "No value for n"

if __name__=="__main__":
    app.run()

