FROM golang:alpine3.19 as builder

ENV GOOS="linux"
ENV CGO_ENABLED="0"
ARG GOARCH="amd64"

ARG CMD="http"

COPY app /app

WORKDIR /app

RUN go build -o main ./cmd/${CMD}/main.go

EXPOSE 8001

FROM alpine:3.19 as prod
COPY --from=builder /app/main /bin/
COPY --from=builder /app/cmd/http/tartu_stops.csv /bin/tartu_stops.csv

WORKDIR /bin
ENTRYPOINT  ["/bin/main"]