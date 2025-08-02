#!/usr/bin/env python3
"""
Test all Jarvis tools functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools.time import get_time
from tools.weather import get_weather
from tools.system_info import get_system_info, get_battery_status
from tools.file_manager import list_files, create_directory, get_file_info
from tools.calculator import calculate, convert_units
from tools.search import search_web, get_news_headlines

def test_all_tools():
    """Test all available tools"""
    print("🤖 Testing Jarvis Tools\n" + "="*50)
    
    # Test time tool
    print("\n1. 🕐 Time Tool:")
    print(get_time.invoke({"city": "new york"}))
    
    # Test calculator
    print("\n2. 🔢 Calculator:")
    print(calculate.invoke({"expression": "45 * 23 + 67"}))
    print(calculate.invoke({"expression": "sqrt(144)"}))
    
    # Test unit conversion
    print("\n3. 🔄 Unit Conversion:")
    print(convert_units.invoke({"value": 100, "from_unit": "fahrenheit", "to_unit": "celsius"}))
    print(convert_units.invoke({"value": 5, "from_unit": "feet", "to_unit": "meters"}))
    
    # Test system info
    print("\n4. 💻 System Information:")
    print(get_system_info.invoke({}))
    print(get_battery_status.invoke({}))
    
    # Test file manager
    print("\n5. 📁 File Manager:")
    print(list_files.invoke({"directory": "."}))
    
    # Test weather (will show config message)
    print("\n6. 🌤️ Weather Tool:")
    print(get_weather.invoke({"city": "London"}))
    
    # Test search
    print("\n7. 🔍 Search Tool:")
    print(search_web.invoke({"query": "python programming"}))
    
    print("\n" + "="*50)
    print("✅ All tools tested!")

if __name__ == "__main__":
    test_all_tools()
