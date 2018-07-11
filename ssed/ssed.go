package main

import (
	"os"
	"fmt"
	"github.com/julienschmidt/httprouter"
	"log"
	"strings"
	"net/http"
	kafka "github.com/confluentinc/confluent-kafka-go/kafka"
	// sarama "github.com/Shopify/sarama"
)

func SSE(rw http.ResponseWriter, r *http.Request, p httprouter.Params) {

	// Make sure that the writer supports flushing.
	//
	flusher, ok := rw.(http.Flusher)
	if !ok {
		http.Error(rw, "Streaming unsupported!", http.StatusInternalServerError)
		return
	}

	// Check topics parameter exist
	q := r.URL.Query()
	topics, ok := q["topics"]
	if !ok {
		topics = nil
	}

	rw.Header().Set("Content-Type", "text/event-stream")
	rw.Header().Set("Cache-Control", "no-cache")
	rw.Header().Set("Connection", "keep-alive")
	rw.Header().Set("Access-Control-Allow-Origin", "*")

	// Setup Kafka connection
	//
	bootstrapServers := os.Getenv("BOOTSTRAP_SERVERS")
	if bootstrapServers == "" {
	    bootstrapServers = "localhost:9092"
	}
	consumer, err := NewLogConsumer(bootstrapServers, topics)
	if err != nil {
		http.Error(rw, "Kafka connection failure!", http.StatusInternalServerError)
		return
	}
	consumer.topics = topics

	msgCh := make(chan *kafka.Message)
	errCh := make(chan error)
	sigCh := make(chan struct{})
	doneCh := make(chan struct{})

	log.Printf("Client connected. subscription %s", strings.Join(topics, ","))
	go consumer.Start(msgCh, errCh, sigCh, doneCh)

	// Listen to connection close and un-register messageChan
	closed := rw.(http.CloseNotifier).CloseNotify()


	for {

		// Write to the ResponseWriter
		// Server Sent Events compatible
		select {
		case msg := <-msgCh:
			fmt.Fprintf(rw, "data: %s\n\n", string(msg.Value))
		case err := <-errCh:
			fmt.Fprintf(rw, "err: %s\n\n", err.Error())
		case <-closed:
			sigCh <- struct{}{}
			<-doneCh
			log.Printf("Client disconnected. subscription %s", strings.Join(topics, ","))
		}

		// Flush the data immediatly instead of buffering it for later.
		flusher.Flush()
	}

}

func main() {
	router := httprouter.New()
	router.GET("/sse", SSE)

	host := os.Getenv("HOST")
	if host == "" {
	    host = "localhost:5002"
	}
	log.Fatal(http.ListenAndServe(host, router))
}
