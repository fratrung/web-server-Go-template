import yaml 
from dotenv import load_dotenv
import json
import os

def get_config():
    print(os.getcwd())
    load_dotenv(".env")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    
    with open("config.yaml","r") as file_yaml:
        config = yaml.safe_load(file_yaml)
    db_host = config['database']['host']
    db_port = config['database']['port']
    db_name = config['database']['name']
    web_port = config['web-server']['port']
    admin_port = config['admin-server']['port']
    return db_user, db_password, db_name,db_host, db_port, web_port, admin_port


def generate_api(addrs="127.0.0.1", port=8080):
    num_endpoints = int(input("How many enpoints you want? "))
    api_server = {
        "api-version": "1.0",
        "base_url": f"http://{addrs}:{port}",
        "endpoints": []
        }
    for i in range(num_endpoints):
        path = input("Enpoint path: ")
        method = input("Method: ")
        endpoint = {
            "path": path,
            "method":method
        }
        api_server['endpoints'].append(endpoint)
    with open("api-server.json","w") as api_file:
        json.dump(api_server,api_file,indent=4)


def generate_code_api_go(api_config):
    api = """
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
 
"""
        
    base_url = api_config['base_url']
    
    if "http://127.0.0.1:" in base_url:
        base_url =f":{base_url.split(":")[-1]}"
    
    endpoints = api_config['endpoints']
    for endpoint in endpoints:
        path = endpoint['path']
        method = endpoint['method']
        handler_string =  path[1:].capitalize()
        
        api += f"\n    router.HandleFunc(\"{method} {path}\", handler.Handle{handler_string})"
        
    api += """
    
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
    """
    
    with open("webserver/api/api.go","w") as file:
        file.write(api)


def generate_code_handlers_go(api_config):
    handler = """
package handler

import (
	"html/template"
	"net/http"
)

"""
    endpoints = api_config['endpoints']
    for endpoint in endpoints:
        path = endpoint['path']
        handler_string =  path[1:].capitalize()
        handler += f"\nfunc Handle{handler_string}(w http.ResponseWriter, r *http.Request) " + "{\n"
        handler += f"    tmpl, err := template.ParseFiles(\"templates{path}.html\")"
        handler += """
	if err != nil {
		http.Error(w, "Errore nel caricamento della pagina", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}
        """
        
    with open("webserver/handler/handler.go","w") as file:
        file.write(handler)
    

def generate_code_main_go(api_config):
    main ="""
package main

import "webserver/api"

func main() {  
"""   
    base_url = api_config['base_url']
    if "http://127.0.0.1:" in base_url:
        base_url =f":{base_url.split(":")[-1]}"

    main +=f"    server := api.NewAPIWebServer(\"{base_url}\")"
    main += """
	server.Run()
}    
    """
    with open("webserver/main.go","w") as file:
        file.write(main)
    

def generate_golang_code(api_config):
    
    generate_code_api_go(api_config)
    generate_code_handlers_go(api_config)
    generate_code_main_go(api_config)
    

def generate_docker_compose(db_user, db_password, db_name,db_host, db_port, web_port, admin_port):
    compose = {
        "services": {
            "web-server": {
                "build":"./webserver",
                "container_name":"web-server",
                "ports":[f"{web_port}:8080"],
                #"depends_on":["db"],
                "environment":{
                    "DB_HOST": db_host,
                    "DB_PORT": db_port,
                    "DB_USER": db_user,
                    "DB_PASSWORD": db_password,
                    "DB_NAME": db_name
                },
                "networks":["app-network"]
            },
            "admin-server": {
                "build": "./adminserver",
                "container_name": "admin-server",
                "ports": [f"{admin_port}:8081"],
                #"depends_on": ["db"],
                "environment": {
                    "DB_HOST": db_host,
                    "DB_PORT": db_port,
                    "DB_USER": db_user,
                    "DB_PASSWORD": db_password,
                    "DB_NAME": db_name
                },
                "networks": ["app-network"]
            },
            
        },
        "networks": {
            "app-network": {}
        },
        "volumes": {
            "pgdata": {}
        }
    }
    
    with open("docker-compose.yml","w") as file:
        yaml.dump(compose,file,default_flow_style=False)
    
    print("\n✅ `docker-compose.yml` generated!\n")


    
if __name__ == "__main__":    
    
    db_user, db_password, db_name,db_host, db_port, web_port, admin_port = get_config()
    generate_api(port=web_port)
    
    with open("api-server.json","r") as api_file:
        api_config = json.load(api_file)   
        
    generate_golang_code(api_config=api_config)
    generate_docker_compose(db_user, db_password, db_name,db_host, db_port, web_port, admin_port)
    