FROM archlinux

WORKDIR /app

COPY . .

RUN  pacman -Sy python python-pip ffmpeg --noconfirm --verbose && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x gunicorn.sh

ENTRYPOINT  ["./gunicorn.sh"]