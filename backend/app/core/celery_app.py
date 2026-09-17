from celery import Celery
from backend.app.core.config import settings

celery_app = Celery(
    "worker",
    broker=f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}//",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",

)

celery_app.conf.update(

    # Task ko JSON format mein serialize karega.
    # Isse task message ko easily store/transmit kiya ja sakta hai.
    task_serializer="json",

    # Task start hote hi uska state STARTED track karega.
    # Useful hai jab hume pata karna ho ki task abhi execute ho raha hai ya nahi.
    task_track_started=True,

    # Task ke result ko JSON format mein serialize karega.
    result_serializer="json",

    # Sirf JSON content ko accept karega.
    # Security aur predictable data format ke liye useful hai.
    accept_content=["application/json"],

    # Result backend se result retrieve karte waqt maximum 10 retries allow karega
    # agar backend temporarily unavailable ho.
    result_backend_max_retries=10,

    # Celery task ke lifecycle events/events send karega.
    # Monitoring tools jaise Flower mein task events dekhne ke liye useful hai.
    task_send_sent_event=True,

    # Result backend mein task ke additional metadata/details bhi store karega.
    # Debugging aur monitoring ke liye useful.
    result_extended=True,

    # Result backend operation fail hone par automatically retry karega.
    # Temporary database/Redis/backend issues handle karne mein useful.
    result_backend_always_retry=True,

    # Task result ko 3600 seconds (1 hour) ke baad expire kar dega.
    # Old results ko indefinitely store hone se bachata hai.
    result_expires=3600,

    # Task ko maximum 5 minutes tak run hone dega.
    # 5 minutes cross hone par task terminate ho sakta hai.
    task_time_limit=5 * 60,

    # Task ko 5 minutes ka soft limit deta hai.
    # Time limit reach hone par Celery SoftTimeLimitExceeded exception raise kar sakta hai,
    # jise code ke andar gracefully handle kiya ja sakta hai.
    task_soft_time_limit=5 * 60,

    # Worker task-related events send karega.
    # Monitoring tools jaise Flower ko worker/task activity track karne mein help karta hai.
    worker_send_task_events=True,

    # Task ka acknowledgement task complete hone ke baad hoga.
    # Agar worker task ke beech mein crash ho jaye,
    # to task ko dobara process kiya ja sakta hai.
    tasks_acks_late=True,

    # Agar worker unexpectedly lost/crash ho jaye,
    # to task ko reject karke re-queue karne ki permission deta hai.
    # Isse task lost hone ka risk kam hota hai.
    task_reject_on_worker_lost=True,

    # Worker ek time par kitne tasks prefetch karega.
    # 1 ka matlab worker ek hi task ko pehle reserve karega.
    # Long-running tasks ke liye fair task distribution mein useful.
    worker_prefetch_multiplier=1,

    # Retry hone wale task ke liye default delay 300 seconds (5 minutes) hai.
    task_default_retry_delay=300,

    # Ek task maximum 3 baar retry ho sakta hai
    # (task ke retry mechanism ke according).
    task_max_retries=3,

    # Tasks ke liye default queue ka naam "nextgen_tasks" hoga.
    task_default_queue="nextgen_tasks",

    # Agar "nextgen_tasks" queue exist nahi karti,
    # to Celery automatically queue create kar sakta hai.
    task_create_missing_queues=True,

    # Ek worker child process maximum 1000 tasks execute karega.
    # Uske baad child process ko restart/recycle kiya jayega.
    # Memory leaks ko control karne mein useful.
    worker_max_tasks_per_child=1000,

    # Worker child process ko maximum memory limit deta hai.
    # Yahan value KB mein hoti hai.
    # 5000 KB ≈ 5 MB.
    # Is limit ko cross karne par child process recycle kiya ja sakta hai.
    worker_max_memory_per_child=5000,

    # Worker ke normal logs ka format define karta hai.
    # %(asctime)s      -> timestamp
    # %(levelname)s    -> log level (INFO, ERROR etc.)
    # %(processName)s  -> process ka naam
    # %(message)s      -> actual log message
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s]%(message)s",

    # Individual task ke logs ka format define karta hai.
    # %(task_name)s -> task ka naam
    # %(task_id)s   -> task ki unique ID
    # Isse specific task ko logs mein easily identify kar sakte hain.
    worker_task_log_format=(
        "[%(asctime)s: %(levelname)s/%(processName)s] "
        "[%(task_name)s(%(task_id)s)] %(message)s"
    ),
)

celery_app.autodiscover_tasks(
    packages=["backend.app.core.emails"],
    related_name="tasks",
    force=True,
)