from magic_filter import MagicFilter
from magic_filter.operations.call import CallOperation as mf_call
from magic_filter.operations.function import FunctionOperation as mf_func
from magic_filter.operations.comparator import ComparatorOperation as mf_comparator

F = MagicFilter()


def filter_attrs(obj, *magic_args):
    try:
        for arg in magic_args:
                
            attr_last = None
            method_found = False

            operations = arg._operations
            if isinstance(operations[-1], mf_call):
                operations = operations[:len(operations)-2]
                method_found = True
            elif isinstance(operations[-1], mf_func):
                operations = operations[:len(operations)-1]
                method_found = True
            elif isinstance(operations[-1], mf_comparator):
                operations = operations[:len(operations)-1]

            for element in operations:
                if attr_last is None:
                    attr_last = getattr(obj, element.name)
                else:
                    attr_last = getattr(attr_last, element.name)

                    if attr_last is None:
                        break

            if isinstance(arg._operations[-1], mf_comparator):
                return attr_last == arg._operations[-1].right

            if not method_found:
                return bool(attr_last)
            
            if attr_last is None:
                return False
            
            if isinstance(arg._operations[-1], mf_func):
                func_operation: mf_func = arg._operations[-1]
                return func_operation.resolve(attr_last, attr_last)
            else:
                method = getattr(attr_last, arg._operations[-2].name)
                args = arg._operations[-1].args

                return method(*args)
    except Exception as e:
        ...