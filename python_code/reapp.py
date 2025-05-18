from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Dict, Union, List


app = FastAPI()

class OperationUnit(BaseModel):
    type_opration: str = Field(..., alias="type")

class MathOperation(OperationUnit):
    type_opration: str = Field("calc", alias="type")
    operation: str = Field(..., alias="op")
    var_name: str = Field(..., alias="var")  
    left: Union[int, str]
    right: Union[int, str]

class PrintOperation(OperationUnit):
    type_operation: str = Field("print", alias="type") 
    var_name: str = Field(..., alias="var")  

class OperationList(BaseModel):
    operations: List[Union[MathOperation, PrintOperation]]


def calculate(op: MathOperation, vars_storage: Dict):
    left_value = vars_storage[op.left] if type(op.left) == str else op.left
    right_value = vars_storage[op.right] if type(op.right) == str else op.right
    if op.operation == "+":
        vars_storage[op.var_name] = left_value + right_value
    elif op.operation == "*":
        vars_storage[op.var_name] = left_value * right_value
    elif op.operation == "-":
        vars_storage[op.var_name] = left_value - right_value


def print_value(op: PrintOperation, items: List, vars_storage: Dict):
    items.append({"var": op.var_name, "value": vars_storage[op.var_name]})


@app.post("/")
def post(opers: List[Union[MathOperation, PrintOperation]]):
    vars_storage: Dict[str, Union[str, int]] = {}
    items: List[Dict] = []
    for op in opers:
        if isinstance(op, MathOperation):
            calculate(op, vars_storage)
        elif isinstance(op, PrintOperation):
            print_value(op, items, vars_storage)
    return items


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="reapp:app", host='127.0.0.1', port=8000, reload=True)