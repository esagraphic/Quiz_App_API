FROM python:3.9

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
# install python dependencies
RUN pip install --upgrade pip
RUN pip install  -r requirements.txt
ENV GEMINI_API_KEY=‘AIzaSyB-nWf0PleMvOrcZB0gpiJPZQ3GfidXMBA’

COPY . .

RUN python manage.py collectstatic --noinput

RUN pip install gunicorn

EXPOSE 8000
# running migrations

# gunicorn
CMD ["gunicorn", "--workers","3", "--bind" ,"0.0.0.0:8000" , "core.wsgi:application"]

