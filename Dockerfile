FROM golang:1.24-alpine as builder

RUN apk add --no-cache git

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM alpine:3.18
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /app
COPY --from=builder /app/main /app/main
RUN chown appuser:appgroup /app/main
USER appuser

EXPOSE 8000
CMD ["/app/main"]