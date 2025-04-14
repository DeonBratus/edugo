package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type LeftAndRight interface{}

type InputData struct {
	Type  string       `json:"type"`
	Op    string       `json:"op,omitempty"`
	Var   string       `json:"var"`
	Left  LeftAndRight `json:"left,omitempty"`
	Right LeftAndRight `json:"right,omitempty"`
}

func parseInputData(jsonData []byte) (InputData, error) {
	var rawData map[string]json.RawMessage
	if err := json.Unmarshal(jsonData, &rawData); err != nil {
		return InputData{}, err
	}

	var inputData InputData
	if err := json.Unmarshal(jsonData, &inputData); err != nil {
		return InputData{}, err
	}

	if rawleft, ok := rawData["left"]; ok {
		inputData.Left = parseLeftAndRight(rawleft)
	}
	if rawright, ok := rawData["right"]; ok {
		inputData.Right = parseLeftAndRight(rawright)
	}
	return inputData, nil
}

func parseLeftAndRight(raw json.RawMessage) LeftAndRight {
	var num int
	if err := json.Unmarshal(raw, &num); err != nil {
		return num
	}

	var str string
	if err := json.Unmarshal(raw, &str); err != nil {
		return str
	}

	return nil
}

type PrintData struct {
	Var string `json:"var"`
}

type CalcData struct {
	Op    string       `json:"op,omitempty"`
	Var   string       `json:"var"`
	Left  LeftAndRight `json:"left,omitempty"`
	Right LeftAndRight `json:"right,omitempty"`
}

// func (clcdata *CalcData) calucate() int {
// 	var res int
// 	switch clcdata.Op {
// 	case "+":
// 		res = clcdata.Left + clcdata.Right
// 		return res
// 	case "-":
// 		res = clcdata.Left - clcdata.Right
// 		return res
// 	case "*":
// 		res = clcdata.Left * clcdata.Right
// 		return res
// 	default:
// 		return 0
// 	}
// }

func typeSelect(indata InputData) interface{} {
	switch indata.Type {
	case "calc":
		return CalcData{
			Var:   indata.Var,
			Op:    indata.Op,
			Left:  indata.Left,
			Right: indata.Right,
		}

	case "print":
		return PrintData{
			Var: indata.Var,
		}
	default:
		return nil
	}
}

func handlePost(writer http.ResponseWriter, req *http.Request) {
	if req.Method != http.MethodPost {
		http.Error(writer, "Method is not supported", http.StatusMethodNotAllowed)
		return
	}

	body, err := io.ReadAll(req.Body)
	if err != nil {
		http.Error(writer, "Reading request error", http.StatusBadRequest)
	}

	defer req.Body.Close()

	// var ops []InputData
	res, err := parseInputData(body)
	if err != nil {

	}
	fmt.Print(res)
	// for _, op := range ops {
	// 	currop := typeSelect(op)
	// 	switch restype := currop.(type) {
	// 	case CalcData:
	// 		// res := restype.calucate()
	// 		// fmt.Println(res)
	// 	case PrintData:
	// 		fmt.Printf("OutputData: %+v\n", restype)
	// 	default:
	// 		fmt.Println("Неизвестный тип операции")
	// 	}
	// }
}

func main() {
	http.HandleFunc("/post", handlePost)
	fmt.Println("Server is running on http://127.0.0.1:8080")
	if err := http.ListenAndServe("127.0.0.1:8080", nil); err != nil {
		fmt.Printf("Error in running server: %s\n", err)
	}
}
