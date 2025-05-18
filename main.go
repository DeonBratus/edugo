package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	_ "edugo/docs"

	httpSwagger "github.com/swaggo/http-swagger"
)

// @title Operation API
// @version 1.0
// @description API для математических и печатных операций.
// @host localhost:8000
// @BasePath /

type OperationUnit struct {
	Type string `json:"type"`
}

type MathOperation struct {
	OperationUnit
	Op    string      `json:"op"`
	Var   string      `json:"var"`
	Left  interface{} `json:"left"`
	Rignt interface{} `json:"rignt"`
}

type PrintOperation struct {
	OperationUnit
	Var string `json:"var"`
}

type ResultItem struct {
	Var   string      `json:"var"`
	Value interface{} `json:"value"`
}

// OperationRequestItem — структура для описания Swagger-документации входных операций
type OperationRequestItem struct {
	Type  string      `json:"type" example:"calc"` // "calc" или "print"
	Op    string      `json:"op,omitempty" example:"+"`
	Var   string      `json:"var" example:"x"`
	Left  interface{} `json:"left,omitempty" example:"2"`
	Rignt interface{} `json:"rignt,omitempty" example:"3"`
}

// @Summary Выполнить список операций
// @Description Принимает список математических и печатных операций, выполняет их и возвращает результат.
// @Accept json
// @Produce json
// @Param operations body []OperationRequestItem true "Список операций"
// @Success 200 {array} ResultItem
// @Failure 400 {string} string "Неверный запрос"
// @Failure 405 {string} string "Метод не поддерживается"
// @Router / [post]
func handlePost(writer http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		http.Error(writer, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var opers []json.RawMessage
	if err := json.NewDecoder(req.Body).Decode(&opers); err != nil {
		http.Error(writer, "Bad Request", http.StatusBadRequest)
		return
	}

	varsStorage := make(map[string]interface{})
	var items []ResultItem

	for _, op := range opers {
		var baseOp OperationUnit
		if err := json.Unmarshal(op, &baseOp); err != nil {
			http.Error(writer, "Invalid Operation", http.StatusBadRequest)
			return
		}

		switch baseOp.Type {
		case "calc":
			var mathOp MathOperation
			if err := json.Unmarshal(op, &mathOp); err != nil {
				http.Error(writer, "Invalid math operation", http.StatusBadRequest)
				return
			}
			calculate(mathOp, varsStorage)
		case "print":
			var printOp PrintOperation
			if err := json.Unmarshal(op, &printOp); err != nil {
				http.Error(writer, "Invalid print operation", http.StatusBadRequest)
				return
			}
			printValue(printOp, &items, varsStorage)
		}
	}
	writer.Header().Set("Content-Type", "application/json")
	json.NewEncoder(writer).Encode(items)
}

func calculate(op MathOperation, varsStorage map[string]interface{}) {
	left := getValue(op.Left, varsStorage)
	right := getValue(op.Rignt, varsStorage)

	switch op.Op {
	case "+":
		varsStorage[op.Var] = left.(float64) + right.(float64)
	case "*":
		varsStorage[op.Var] = left.(float64) * right.(float64)
	case "-":
		varsStorage[op.Var] = left.(float64) - right.(float64)
	}
}

func getValue(val interface{}, varsStorage map[string]interface{}) interface{} {
	switch v := val.(type) {
	case string:
		if value, exists := varsStorage[v]; exists {
			return value
		}
		return 0.0
	case float64:
		return v
	default:
		return 0.0
	}
}

func printValue(op PrintOperation, items *[]ResultItem, varsStorage map[string]interface{}) {
	value, exists := varsStorage[op.Var]
	if !exists {
		value = 0.0
	}
	*items = append(*items, ResultItem{
		Var:   op.Var,
		Value: value,
	})
}

func main() {
	http.HandleFunc("/", handlePost)
	http.Handle("/swagger/", httpSwagger.WrapHandler)

	fmt.Println("Server is running on http://127.0.0.1:8000")
	fmt.Println("Swagger UI:     http://127.0.0.1:8000/swagger/index.html")
	log.Fatal(http.ListenAndServe(":8000", nil))
}
