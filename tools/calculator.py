# tools/calculator.py

from langchain.tools import tool
import math
import re

@tool
def calculate(expression: str) -> str:
    """Perform mathematical calculations. Supports basic arithmetic, trigonometry, and common functions."""
    try:
        # Clean the expression
        expression = expression.strip()
        
        # Replace common words with operators
        expression = re.sub(r'\bplus\b|\badd\b', '+', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\bminus\b|\bsubtract\b', '-', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\btimes\b|\bmultiply\b', '*', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\bdivide\b|\bdivided by\b', '/', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\bsquare root of\b|\bsqrt\b', 'sqrt', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\bpi\b', 'math.pi', expression, flags=re.IGNORECASE)
        expression = re.sub(r'\be\b', 'math.e', expression, flags=re.IGNORECASE)
        
        # Replace function names
        expression = re.sub(r'\bsin\b', 'math.sin', expression)
        expression = re.sub(r'\bcos\b', 'math.cos', expression)
        expression = re.sub(r'\btan\b', 'math.tan', expression)
        expression = re.sub(r'\blog\b', 'math.log10', expression)
        expression = re.sub(r'\bln\b', 'math.log', expression)
        expression = re.sub(r'\bsqrt\b', 'math.sqrt', expression)
        expression = re.sub(r'\babs\b', 'abs', expression)
        
        # Safety check - only allow math operations
        allowed_chars = set('0123456789+-*/().= mathsincotanlgqrbpe')
        if not all(c.lower() in allowed_chars for c in expression.replace(' ', '')):
            return "Invalid characters in expression. Only mathematical operations are allowed."
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}, "math": math, "abs": abs})
        
        # Format the result
        if isinstance(result, float):
            if result.is_integer():
                return f"{expression} = {int(result)}"
            else:
                return f"{expression} = {result:.6f}".rstrip('0').rstrip('.')
        else:
            return f"{expression} = {result}"
            
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Math error: {e}"
    except Exception as e:
        return f"Calculation error: {e}"

@tool
def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between common units (length, weight, temperature)."""
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()
        
        # Length conversions (to meters)
        length_units = {
            'mm': 0.001, 'millimeter': 0.001, 'millimeters': 0.001,
            'cm': 0.01, 'centimeter': 0.01, 'centimeters': 0.01,
            'm': 1, 'meter': 1, 'meters': 1,
            'km': 1000, 'kilometer': 1000, 'kilometers': 1000,
            'in': 0.0254, 'inch': 0.0254, 'inches': 0.0254,
            'ft': 0.3048, 'foot': 0.3048, 'feet': 0.3048,
            'yd': 0.9144, 'yard': 0.9144, 'yards': 0.9144,
            'mi': 1609.34, 'mile': 1609.34, 'miles': 1609.34
        }
        
        # Weight conversions (to grams)
        weight_units = {
            'mg': 0.001, 'milligram': 0.001, 'milligrams': 0.001,
            'g': 1, 'gram': 1, 'grams': 1,
            'kg': 1000, 'kilogram': 1000, 'kilograms': 1000,
            'oz': 28.3495, 'ounce': 28.3495, 'ounces': 28.3495,
            'lb': 453.592, 'pound': 453.592, 'pounds': 453.592
        }
        
        # Temperature conversion
        if from_unit in ['celsius', 'c'] and to_unit in ['fahrenheit', 'f']:
            result = (value * 9/5) + 32
            return f"{value}°C = {result:.2f}°F"
        elif from_unit in ['fahrenheit', 'f'] and to_unit in ['celsius', 'c']:
            result = (value - 32) * 5/9
            return f"{value}°F = {result:.2f}°C"
        elif from_unit in ['celsius', 'c'] and to_unit in ['kelvin', 'k']:
            result = value + 273.15
            return f"{value}°C = {result:.2f}K"
        elif from_unit in ['kelvin', 'k'] and to_unit in ['celsius', 'c']:
            result = value - 273.15
            return f"{value}K = {result:.2f}°C"
        
        # Length conversion
        if from_unit in length_units and to_unit in length_units:
            meters = value * length_units[from_unit]
            result = meters / length_units[to_unit]
            return f"{value} {from_unit} = {result:.6f} {to_unit}".rstrip('0').rstrip('.')
        
        # Weight conversion
        if from_unit in weight_units and to_unit in weight_units:
            grams = value * weight_units[from_unit]
            result = grams / weight_units[to_unit]
            return f"{value} {from_unit} = {result:.6f} {to_unit}".rstrip('0').rstrip('.')
        
        return f"Cannot convert from {from_unit} to {to_unit}. Supported: length (mm,cm,m,km,in,ft,yd,mi), weight (mg,g,kg,oz,lb), temperature (celsius,fahrenheit,kelvin)"
        
    except Exception as e:
        return f"Conversion error: {e}"
