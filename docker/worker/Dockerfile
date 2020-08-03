FROM golang:1.14.4 as builder
WORKDIR /go/src/github.com/gitkado/QueueSubscribeWorker/
COPY src/go.mod .
RUN go mod download
COPY src .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

FROM alpine:3.12.0
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /go/src/github.com/gitkado/QueueSubscribeWorker/app .
CMD ["./app"]