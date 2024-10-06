import asyncio


class SMTPHandler:
    async def handle_RCPT(self, server, session, envelope, address: str, rcpt_options):
        envelope.rcpt_tos.append(address)
        return "250 OK"

    async def handle_DATA(self, server, session, envelope):
        print("Message from %s" % envelope.mail_from)
        print("Message for %s" % envelope.rcpt_tos)
        print("Message data: \n")
        for ln in envelope.content.decode("utf8", errors="replace").splitlines():
            print(f"> {ln}".strip())
        print()
        print("End of message")
        return "250 Message accepted for delivery"
