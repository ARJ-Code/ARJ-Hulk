import importlib

test_modules = {
    'slr1': 'test',
    'lr1': 'test',
    'tableLR': 'test'
}

for module_name, method_name in test_modules.items():
    try:
        module = importlib.import_module(f"tests.{module_name}")

        getattr(module, method_name)()
        print(f"{module_name} test passed")
    except Exception as e:
        print(f"{module_name} test failed: {e}")
