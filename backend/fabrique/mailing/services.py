import datetime
import os
import pytz
import requests

from dotenv import load_dotenv
from celery.utils.log import get_task_logger
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q

from .models import Message, Client, Mailing
from backend.fabrique.fabrique.celery import app

logger = get_task_logger(__name__)

load_dotenv()
API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")


@app.task(bind=True, retry_backoff=True)
def send_message(
        self,
        data,
        client_id,
        mailing_id,
        url=API_URL,
        token=API_TOKEN
):
    mailing = Mailing.objects.get(pk=mailing_id)
    client = Client.objects.get(pk=client_id)
    timezone = pytz.timezone(client.timezone)
    now = datetime.datetime.now(timezone)

    if mailing.time_start <= now.time() <= mailing.time_end:
        header = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'}
        try:
            requests.post(url=url + str(data['id']), headers=header, json=data)
        except requests.exceptions.RequestException as exc:
            logger.error(f"Message if: {data['id']} is error")
            raise self.retry(exc=exc)
        else:
            logger.info(f"Message id: {data['id']}, Sending status: 'Sent'")
            Message.objects.filter(pk=data['id']).update(sending_status='Sent')
    else:
        time = 24 - (int(now.time().strftime('%H:%M:%S')[:2]) -
                     int(mailing.time_start.strftime('%H:%M:%S')[:2]))
        logger.info(f"Message id: {data['id']}, "
                    f"The current time is not for sending the message,"
                    f"restarting task after {60 * 60 * time} seconds")
        return self.retry(countdown=60 * 60 * time)


@receiver(post_save, sender=Mailing, dispatch_uid="create_message")
def create_message(sender, instance, created, **kwargs):
    if created:
        mailing = Mailing.objects.filter(id=instance.id).first()
        clients = Client.objects.filter(
            Q(phone_code=mailing.mobile_operator_code) |
            Q(tag=mailing.tag)).all()

        for client in clients:
            Message.objects.create(
                sending_status="No sent",
                client_id=client.id,
                mailing_id=instance.id
            )
            message = Message.objects.filter(mailing_id=instance.id,
                                             client_id=client.id).first()
            data = {
                'id': message.id,
                "phone": client.phone_number,
                "text": mailing.text
            }
            client_id = client.id
            mailing_id = mailing.id

            if instance.to_send:
                send_message.apply_async((data, client_id, mailing_id),
                                         expires=mailing.date_end)
            else:
                send_message.apply_async((data, client_id, mailing_id),
                                         eta=mailing.date_start,
                                         expires=mailing.date_end)
