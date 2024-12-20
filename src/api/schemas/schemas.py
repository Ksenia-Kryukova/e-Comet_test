from pydantic import BaseModel


class Base(BaseModel):
    pass


class Top100Model(Base):
    repo: str           # название репозитория
    owner: str          # владелец репозитория
    position_cur: int   # текущая позиция в топе
    position_prev: int  # предыдущая позиция в топе
    stars: int          # количество звёзд
    watchers: int       # количество просмотров
    forks: int          # количество форков
    open_issues: int    # количество открытых issues
    language: str       # язык


class ActivityModel(Base):
    date: Date
    commits: int        # количество коммитов за конкретный день
    authors: list[str]  # список разработчиков, которые выполняли коммиты

