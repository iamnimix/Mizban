from pydantic import BaseModel, HttpUrl


class RequestUrl(BaseModel):
    url: HttpUrl


class ResponseUrl(BaseModel):
    short_url: str
