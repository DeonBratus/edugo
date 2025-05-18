# Используем официальный образ Go
FROM golang:1.21-alpine as builder

# Устанавливаем зависимости
RUN apk add --no-cache git

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы модулей и загружаем зависимости
COPY go.mod go.sum ./
RUN go mod download

# Копируем исходный код
COPY . .

# Собираем приложение
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Финальный образ
FROM alpine:latest

# Копируем бинарный файл из builder
COPY --from=builder /app/main /main

# Открываем порт
EXPOSE 8000

# Запускаем приложение
CMD ["/main"]