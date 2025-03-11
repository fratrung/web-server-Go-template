
package handler

import (
	"html/template"
	"net/http"
)


func HandleHome(w http.ResponseWriter, r *http.Request) {
    tmpl, err := template.ParseFiles("templates/home.html")
	if err != nil {
		http.Error(w, "Errore nel caricamento della pagina", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}
        
func HandleProducts(w http.ResponseWriter, r *http.Request) {
    tmpl, err := template.ParseFiles("templates/products.html")
	if err != nil {
		http.Error(w, "Errore nel caricamento della pagina", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}
        
func HandleContacts(w http.ResponseWriter, r *http.Request) {
    tmpl, err := template.ParseFiles("templates/contacts.html")
	if err != nil {
		http.Error(w, "Errore nel caricamento della pagina", http.StatusInternalServerError)
		return
	}
	tmpl.Execute(w, nil)
}
        