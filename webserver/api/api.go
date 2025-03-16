
package api

import (
	"log"
	"net/http"
	"webserver/handler"
	"webserver/middleware"
)

type APIWebServer struct {
	addr string
}

func NewAPIWebServer(addr string) *APIWebServer {
	return &APIWebServer{
		addr: addr,
	}
}

func (s *APIWebServer) Run() error {
	router := http.NewServeMux()
	fs := http.FileServer(http.Dir("static"))
	router.Handle("/static/", http.StripPrefix("/static/", fs))
 

    router.HandleFunc("GET /home", handler.HandleHome)
    router.HandleFunc("GET /products", handler.HandleProducts)
    
	middlewareChain := middleware.MiddlewareChain(
		middleware.RequestLoggerMiddleware,
	)

	server := http.Server{
		Addr:    s.addr,
		Handler: middlewareChain(router),
	}
	log.Printf("Server has started %s", s.addr)
	return server.ListenAndServe()

}    
    