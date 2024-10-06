import smtplib
from aiosmtpd.controller import Controller
from .controller import SMTPHandler
from core.config import settings
from loguru import logger


async def send_mailing(email: str, msg: str = ""):
    try:
        controller = Controller(SMTPHandler())
        controller.start()

        with smtplib.SMTP(host=settings.SMTP_HOST, port=settings.SMTP_PORT) as server:

            if settings.SMTP_FROM_PASSWORD is not None:
                server.login(
                    user=settings.SMTP_FROM_ADDRESS,
                    password=settings.SMTP_FROM_PASSWORD,
                )
            server.sendmail(
                from_addr=settings.SMTP_FROM_ADDRESS, to_addrs=email, msg=msg
            )

        controller.stop()
    except Exception as e:
        logger.error(e)
