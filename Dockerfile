# Билд стадии
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Копируем файлы модулей и скачиваем зависимости
COPY go.mod go.sum ./
RUN go mod download

# Копируем исходный код
COPY . .

# Собираем бинарник с отключенным CGO и статической линковкой
RUN CGO_ENABLED=0 GOOS=linux go build -o /server

# Финальная стадия
FROM alpine:latest

WORKDIR /app

# Копируем бинарник из билдера
COPY --from=builder /server /app/server

# Открываем порт
EXPOSE 8000

# Запускаем сервер
CMD ["/app/server"]