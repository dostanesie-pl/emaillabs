import base64
import dataclasses
import typing
from functools import cached_property

import requests


@dataclasses.dataclass
class Recipient:
    email: str
    variables: dict[str, typing.Any] | None = None
    message_id: str | None = None

    def get_data(self) -> typing.Generator[tuple[str, typing.Any], None, None]:
        yield f'to[{self.email}]', ''
        if self.message_id:
            yield f'to[{self.email}][message_id]', f'{self.message_id}@dostanesie.pl'
        if self.variables:
            for variable_name, variable_value in self.variables.items():
                yield f'to[{self.email}][vars][{variable_name}]', variable_value


class Client:
    def __init__(self, api_key: str, api_secret: str, smtp_server: str, dry_run: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.smtp_server = smtp_server
        self.dry_run = dry_run

    @cached_property
    def mail_auth(self) -> str:
        return f'Basic {base64.b64encode((self.api_key + ":" + self.api_secret).encode()).decode()}'

    @cached_property
    def session(self) -> requests.Session:
        session = requests.Session()
        session.headers['Authorization'] = self.mail_auth
        return session

    def template_mailing(
            self, *,
            template_id: str,
            from_address: str,
            from_name: str,
            subject: str,
            to_data: list[Recipient],
    ) -> requests.Response | None:
        data = {
            'smtp_account': self.smtp_server,
            'template_id': template_id,
            'from': from_address,
            'from_name': from_name,
            'subject': subject,
        }
        for r in to_data:
            for key, value in r.get_data():
                data[key] = value
        if self.dry_run:
            return None
        else:
            response = self.session.post(
                url='https://api.emaillabs.net.pl/api/sendmail_templates',
                data=data,
            )
            return response

    def send_email(
            self, *,
            to: Recipient,
            from_address: str,
            from_name: str,
            text: str,
            html: str,
            subject: str,
    ) -> requests.Response | None:
        if self.dry_run:
            return None
        else:
            response = self.session.post(
                url='https://api.emaillabs.net.pl/api/new_sendmail',
                data={
                    f'to[{to.email}]': '',
                    'from': from_address,
                    'from_name': from_name,
                    'smtp_account': self.smtp_server,
                    'text': text,
                    'html': html,
                    'subject': subject,
                },
            )
            return response
