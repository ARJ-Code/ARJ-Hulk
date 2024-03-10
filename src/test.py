import importlib

test_modules = [
    'slr1',
    'lr1',
    'tableLR',
    'regex',
    'lexer',
    'automaton',
]

for module_name in test_modules:
    try:
        module = importlib.import_module(f"tests.{module_name}")

        getattr(module, 'test')()
        print(f"{module_name} test passed")
    except Exception as e:
        print(f"{module_name} test failed: {e}")
