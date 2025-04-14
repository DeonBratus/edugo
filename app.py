from fastapi import FastAPI, APIRouter
import uvicorn
from pydantic import BaseModel

api = APIRouter()

class PrintModel(BaseModel):
    type: str
    var: str


class CalcModel(PrintModel):
    op: str | None = None
    left: int | str = None
    right: int | str = None

    def __init__(self,
                type: str,
                var: str,
                op: str | None = None,
                left: int | None = None,
                right: int | None = None):
        
        super().__init__(type=type, var=var)

        self.op = op
        self.left = left
        self.right = right

    def calculate(self):
        if self.op == "+":
            return self.left + self.right
        elif self.op == "-":
            return self.left - self.right
        elif self.op == "*":
            return self.left * self.right
        else:
            return None


class GettingCalcModel(CalcModel):

    def determine_model(self):
        if self.op is None and self.left is None and self.right is None:
            return PrintModel(type=self.type, var=self.var)
        else:
            return CalcModel(type=self.type, op=self.op, var=self.var, left=self.left, right=self.right)
        

@api.post("/")
def post(ops: list[GettingCalcModel]):

    validated_ops = [op.determine_model() for op in ops]

    vars = {}
    output_vars = {"items": []}

    for op in validated_ops:
        if isinstance(op, CalcModel):

            if type(op.left) == int and type(op.right) == int:
                vars[op.var] = op.calculate()

            elif type(op.left) == str or type(op.right) == str: 
                if type(op.left) == str:
                    op.left = vars[op.left] 
                if type(op.right) == str:
                    op.right = vars[op.right]

                vars[op.var] = op.calculate()
                op.var = op.calculate()

        elif isinstance(op, PrintModel):
            output_vars["items"].append({"var": op.var, "value": vars[op.var]})
            
    return output_vars


app = FastAPI()
app.include_router(api)
if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=8000, reload=True )