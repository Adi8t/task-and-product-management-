from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
import logging
from core.models import Task

logger = logging.getLogger(__name__)

@shared_task
def send_task_reminder():
    try:
        # Get the current time
        current_time = now()\
        
        logger.info(f"Current Time: {current_time}")

        # Filter tasks due within the next 1 hour where reminder is not sent
        tasks_due_soon = Task.objects.filter(
            due_date__gte=current_time - timedelta(minutes=1), 
            due_date__lte=current_time + timedelta(hours=1),
            reminder_sent=False  
        )

        if not tasks_due_soon:
            logger.info("No tasks due within the next 1 hour.")
            return

        for task in tasks_due_soon:
            logger.info(f"Processing Task: {task.title}, Due: {task.due_date}, Reminder Sent: {task.reminder_sent}")
            try:
                send_mail(
                    'Task Reminder',
                    f'Reminder: Your task "{task.title}" is due soon.',
                    'noreply@myapp.com',
                    [task.assigned_user.email],
                )
                logger.info(f"Reminder email sent for Task: {task.title} to {task.assigned_user.email}")

                task.reminder_sent = True
                task.save(update_fields=['reminder_sent'])
            except Exception as email_error:
                logger.error(f"Failed to send email for Task: {task.title}. Error: {str(email_error)}")
    except Exception as e:
        logger.error(f"Error in send_task_reminder: {str(e)}")
