package handler

import (
	"html/template"
	"net/http"
)

func HandleHome(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/home.html")
	if err != nil {
		http.Error(w, "Error loading the page", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}

func HandleContact(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/contact.html")
	if err != nil {
		http.Error(w, "Error loading the page", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}

func HandleProducts(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/products.html")
	if err != nil {
		http.Error(w, "Error loading the page", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}

func HandleServices(w http.ResponseWriter, r *http.Request) {
	tmpl, err := template.ParseFiles("templates/services.html")
	if err != nil {
		http.Error(w, "Error loading the page", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}
