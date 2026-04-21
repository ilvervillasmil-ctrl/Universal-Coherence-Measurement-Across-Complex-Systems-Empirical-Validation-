#!/usr/bin/env python3
"""
Demo script for the Greeting System
Shows the multilingual greeting capability of the Universal Integration System
"""

from core.greetings import GreetingSystem


def main():
    """Demonstrate the greeting system"""
    gs = GreetingSystem()
    
    print("=" * 60)
    print(gs.welcome_message())
    print("=" * 60)
    print()
    
    # Demonstrate Hola (Spanish) - the main requirement
    print(">>> Main Feature: Spanish Greeting")
    print(f"{gs.greet('es')} - Spanish greeting")
    print(f"{gs.greet_world('es')} - Spanish 'Hello World'")
    print()
    
    # Demonstrate other languages
    print(">>> Multilingual Support:")
    for greeting in gs.get_all_greetings():
        print(f"  • {greeting}")
    print()
    
    # Demonstrate Hello World in multiple languages
    print(">>> 'Hello World' in Different Languages:")
    languages = ['en', 'es', 'fr', 'de']
    for lang in languages:
        print(f"  • {gs.greet_world(lang)}")
    print()
    
    print("=" * 60)
    print("Universal Integration System - Greetings Module")
    print("α + β = 1 | Order + Mystery = Totality")
    print("=" * 60)


if __name__ == "__main__":
    main()
