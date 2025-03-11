
package main

import "webserver/api"

func main() {  
    server := api.NewAPIWebServer(":8080")
	server.Run()
}    
    