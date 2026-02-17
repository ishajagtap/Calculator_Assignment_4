from abc import ABC, abstractmethod
from app.operation import Operation

class Calculation(ABC):
    def __init__(self, a:float,b:float)->None :
        self.a:float =a
        self.b:float=b


    @abstractmethod
    def execute(self) -> float:
        pass  # pragma: no cover

    def __str__(self) -> str:
        result = self.execute() 
        operation_name = self.__class__.__name__.replace('Calculation', '')
        return f"{self.__class__.__name__}: {self.a} {operation_name} {self.b} = {result}"
    
    def __repr__(self) -> str:
         return f"{self.__class__.__name__}(a={self.a}, b={self.b})"
    
class CalculationFactory:   
     _calculations = {}

     @classmethod
     def register_calculation(cls, calculation_type: str):
    
        def decorator(subclass):
            # Convert calculation_type to lowercase to ensure consistency.
            calculation_type_lower = calculation_type.lower()
            # Check if the calculation type has already been registered to avoid duplication.
            if calculation_type_lower in cls._calculations:
                raise ValueError(f"Calculation type '{calculation_type}' is already registered.")
            # Register the subclass in the _calculations dictionary.
            cls._calculations[calculation_type_lower] = subclass
            return subclass  # Return the subclass for chaining or additional use
        return decorator 
     

     @classmethod
     def create_calculation(cls, calculation_type: str, a: float, b: float) -> Calculation:
        
        calculation_type_lower = calculation_type.lower()
        calculation_class = cls._calculations.get(calculation_type_lower)
        # If the type is unsupported, raise an error with the available types.
        if not calculation_class:
            available_types = ', '.join(cls._calculations.keys())
            raise ValueError(f"Unsupported calculation type: '{calculation_type}'. Available types: {available_types}")
        # Create and return an instance of the requested calculation class with the provided operands.
        return calculation_class(a, b)
     
@CalculationFactory.register_calculation('add')
class AddCalculation(Calculation):
    
    def execute(self) -> float:
        return Operation.addition(self.a, self.b)


@CalculationFactory.register_calculation('subtract')
class SubtractCalculation(Calculation):
   

    def execute(self) -> float:
        return Operation.subtraction(self.a, self.b)


@CalculationFactory.register_calculation('multiply')
class MultiplyCalculation(Calculation):
   

    def execute(self) -> float:
        return Operation.multiplication(self.a, self.b)


@CalculationFactory.register_calculation('divide')
class DivideCalculation(Calculation):
    

    def execute(self) -> float:
        if self.b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return Operation.division(self.a, self.b)
