FROM golang:1.23.1

WORKDIR /app

COPY . /app/

RUN go mod download

RUN go build -o webserver .

CMD [ "./webserver" ]