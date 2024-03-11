from regex.regex import Regex

r9 = Regex('function')


def match(text: str, index: int, r: Regex):
        current_state = r.automaton.initial_state
        result = ''

        while index != len(text):
            current_state = current_state.goto(text[index])

            result += text[index]
            index += 1

            if current_state is None:
                return result, False
            if current_state.is_final:
                return result, len(result) != 0

        return result, False

print(match('foreach',0,r9))
  