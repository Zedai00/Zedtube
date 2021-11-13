FROM archlinux

WORKDIR /app

COPY . .

RUN patched_glibc=glibc-linux4-2.33-4-x86_64.pkg.tar.zst && \
    curl -LO "https://repo.archlinuxcn.org/x86_64/$patched_glibc" && \
    bsdtar -C / -xvf "$patched_glibc"

RUN  pacman -Sy python python-pip ffmpeg --noconfirm --verbose && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    chmod +x gunicorn.sh

ENTRYPOINT  ["./gunicorn.sh"]